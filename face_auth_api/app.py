import json
import os
import re
import unicodedata
import uuid
from pathlib import Path

import cv2
import numpy as np
from flask import Flask, jsonify, request

try:
    import mediapipe as mp
except ImportError:
    mp = None

try:
    import pytesseract
    if os.environ.get("TESSERACT_CMD"):
        pytesseract.pytesseract.tesseract_cmd = os.environ["TESSERACT_CMD"]
except ImportError:
    pytesseract = None


APP_VERSION = "1.0.0-v4"
BASE_DIR = Path(__file__).resolve().parent
PROFILE_DIR = BASE_DIR / "face_profiles"
MODEL_DIR = BASE_DIR / "models"
FACE_LANDMARKER_MODEL = MODEL_DIR / "face_landmarker.task"
PROFILE_DIR.mkdir(parents=True, exist_ok=True)

MAX_UPLOAD_BYTES = int(os.environ.get("FACE_AUTH_MAX_UPLOAD_BYTES", 5 * 1024 * 1024))
ACTION_FLIP_HORIZONTAL = os.environ.get("FACE_ACTION_FLIP_HORIZONTAL", "false").lower() in ("1", "true", "yes")

TURN_YAW_DEGREES = float(os.environ.get("FACE_ACTION_TURN_YAW_DEGREES", 14))
LOOK_PITCH_DEGREES = float(os.environ.get("FACE_ACTION_LOOK_PITCH_DEGREES", 12))
MOUTH_OPEN_RATIO = float(os.environ.get("FACE_ACTION_MOUTH_OPEN_RATIO", 0.055))
SMILE_RATIO = float(os.environ.get("FACE_ACTION_SMILE_RATIO", 1.18))

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_BYTES

FACE_MESH = None
FACE_LANDMARKER = None
MEDIAPIPE_BACKEND = "missing"

if mp is not None and hasattr(mp, "solutions"):
    mp_face_mesh = mp.solutions.face_mesh
    FACE_MESH = mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=2,
        refine_landmarks=True,
        min_detection_confidence=0.5,
    )
    MEDIAPIPE_BACKEND = "solutions.face_mesh"
elif mp is not None:
    try:
        from mediapipe.tasks import python
        from mediapipe.tasks.python import vision

        if FACE_LANDMARKER_MODEL.exists():
            base_options = python.BaseOptions(model_asset_path=str(FACE_LANDMARKER_MODEL))
            options = vision.FaceLandmarkerOptions(
                base_options=base_options,
                running_mode=vision.RunningMode.IMAGE,
                num_faces=2,
                output_face_blendshapes=False,
                output_facial_transformation_matrixes=False,
            )
            FACE_LANDMARKER = vision.FaceLandmarker.create_from_options(options)
            MEDIAPIPE_BACKEND = "tasks.face_landmarker"
        else:
            MEDIAPIPE_BACKEND = "tasks.model_missing"
    except Exception:
        FACE_LANDMARKER = None
        MEDIAPIPE_BACKEND = "tasks.load_failed"


def request_id():
    return uuid.uuid4().hex


def read_user_id():
    user_id = (request.form.get("user_id") or request.form.get("userId") or "").strip()
    user_id_alt = (request.form.get("userId") or "").strip()
    if user_id and user_id_alt and user_id != user_id_alt:
        return None, error_response("USER_ID_MISMATCH", "user_id and userId do not match", user_id=user_id)
    return user_id, None


def error_response(error_code, error_message, status=200, user_id=None, confidence=0.0, purpose=None, action_code=None):
    payload = {
        "success": False,
        "confidence": float(confidence),
        "user_id": str(user_id or ""),
        "liveness_passed": False,
        "error_code": error_code,
        "error_message": error_message,
        "request_id": request_id(),
        "purpose": purpose or request.form.get("purpose", ""),
    }
    if action_code:
        payload.update(
            {
                "action_matched": False,
                "action_code": action_code,
                "action_message": error_message,
            }
        )
    return jsonify(payload), status


def decode_upload():
    uploaded_file = request.files.get("file")
    if uploaded_file is None:
        return None, error_response("FILE_MISSING", "File field 'file' is required", status=400)

    data = uploaded_file.read()
    if not data:
        return None, error_response("FILE_EMPTY", "Uploaded file is empty", status=400)

    if len(data) > MAX_UPLOAD_BYTES:
        return None, error_response("FILE_TOO_LARGE", "Uploaded file is too large", status=400)

    image = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        return None, error_response("IMAGE_INVALID", "Cannot decode uploaded image", status=400)

    return image, None


def decode_named_upload(*names):
    uploaded_file = None
    for name in names:
        uploaded_file = request.files.get(name)
        if uploaded_file is not None:
            break

    if uploaded_file is None:
        return None, None

    data = uploaded_file.read()
    if not data:
        return None, error_response("FILE_EMPTY", "Uploaded file is empty", status=400)

    if len(data) > MAX_UPLOAD_BYTES:
        return None, error_response("FILE_TOO_LARGE", "Uploaded file is too large", status=400)

    image = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        return None, error_response("IMAGE_INVALID", "Cannot decode uploaded image", status=400)

    return image, None


def decode_identity_uploads():
    front_image, front_error = decode_named_upload("front_file", "frontFile", "front", "file")
    if front_error:
        return None, None, front_error

    back_image, back_error = decode_named_upload("back_file", "backFile", "back")
    if back_error:
        return None, None, back_error

    if front_image is None and back_image is None:
        return None, None, error_response("FILE_MISSING", "Identity front_file or back_file is required", status=400)

    return front_image, back_image, None


def detect_landmarks(image):
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height, width = image.shape[:2]

    if FACE_MESH is not None:
        result = FACE_MESH.process(rgb)
        faces = result.multi_face_landmarks or []
        if len(faces) == 0:
            return None, error_response("NO_FACE_DETECTED", "No face detected")
        if len(faces) > 1:
            return None, error_response("MULTIPLE_FACES", "Multiple faces detected")

        points = []
        for landmark in faces[0].landmark:
            points.append(np.array([landmark.x * width, landmark.y * height, landmark.z * width], dtype=np.float64))
        return points, None

    if FACE_LANDMARKER is not None:
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(rgb))
        result = FACE_LANDMARKER.detect(mp_image)
        faces = result.face_landmarks or []
        if len(faces) == 0:
            return None, error_response("NO_FACE_DETECTED", "No face detected")
        if len(faces) > 1:
            return None, error_response("MULTIPLE_FACES", "Multiple faces detected")

        points = []
        for landmark in faces[0]:
            points.append(np.array([landmark.x * width, landmark.y * height, landmark.z * width], dtype=np.float64))
        return points, None

    if MEDIAPIPE_BACKEND == "tasks.model_missing":
        return None, error_response("FACE_MODEL_MISSING", f"Missing model file: {FACE_LANDMARKER_MODEL}")

    return None, error_response("FACE_MESH_NOT_AVAILABLE", "MediaPipe Face Mesh/Face Landmarker is not available")


def distance(points, first, second):
    return float(np.linalg.norm(points[first][:2] - points[second][:2]))


def head_pose(points, image_shape):
    height, width = image_shape[:2]
    image_points = np.array(
        [
            points[1][:2],    # Nose tip
            points[152][:2],  # Chin
            points[33][:2],   # Left eye outer corner
            points[263][:2],  # Right eye outer corner
            points[61][:2],   # Left mouth corner
            points[291][:2],  # Right mouth corner
        ],
        dtype=np.float64,
    )

    model_points = np.array(
        [
            (0.0, 0.0, 0.0),
            (0.0, -63.6, -12.5),
            (-43.3, 32.7, -26.0),
            (43.3, 32.7, -26.0),
            (-28.9, -28.9, -24.1),
            (28.9, -28.9, -24.1),
        ],
        dtype=np.float64,
    )

    focal_length = width
    camera_matrix = np.array(
        [[focal_length, 0, width / 2], [0, focal_length, height / 2], [0, 0, 1]],
        dtype=np.float64,
    )
    dist_coeffs = np.zeros((4, 1))
    success, rotation_vector, _ = cv2.solvePnP(
        model_points,
        image_points,
        camera_matrix,
        dist_coeffs,
        flags=cv2.SOLVEPNP_ITERATIVE,
    )
    if not success:
        return 0.0, 0.0, 0.0

    rotation_matrix, _ = cv2.Rodrigues(rotation_vector)
    _, _, _, _, _, _, angles = cv2.decomposeProjectionMatrix(
        np.hstack((rotation_matrix, np.zeros((3, 1))))
    )
    pitch = float(angles[0][0])
    yaw = float(angles[1][0])
    roll = float(angles[2][0])
    if ACTION_FLIP_HORIZONTAL:
        yaw = -yaw
    return pitch, yaw, roll


def action_metrics(points, image_shape):
    pitch, yaw, roll = head_pose(points, image_shape)
    eye_distance = max(distance(points, 33, 263), 1.0)
    face_height = max(distance(points, 10, 152), 1.0)
    mouth_width = distance(points, 61, 291)
    mouth_open = distance(points, 13, 14)

    nose_x = points[1][0]
    eye_mid_x = (points[33][0] + points[263][0]) / 2.0
    nose_offset = (nose_x - eye_mid_x) / eye_distance
    if ACTION_FLIP_HORIZONTAL:
        nose_offset = -nose_offset

    return {
        "pitch": pitch,
        "yaw": yaw,
        "roll": roll,
        "nose_offset": nose_offset,
        "mouth_open_ratio": mouth_open / face_height,
        "smile_ratio": mouth_width / eye_distance,
    }


def classify_action(metrics):
    horizontal_score = metrics["yaw"]
    if abs(metrics["yaw"]) < TURN_YAW_DEGREES and abs(metrics["nose_offset"]) >= 0.18:
        horizontal_score = 100.0 if metrics["nose_offset"] > 0 else -100.0

    if horizontal_score >= TURN_YAW_DEGREES:
        return "turn_right"
    if horizontal_score <= -TURN_YAW_DEGREES:
        return "turn_left"
    if metrics["pitch"] <= -LOOK_PITCH_DEGREES:
        return "look_up"
    if metrics["pitch"] >= LOOK_PITCH_DEGREES:
        return "look_down"
    if metrics["mouth_open_ratio"] >= MOUTH_OPEN_RATIO:
        return "mouth_open"
    if metrics["smile_ratio"] >= SMILE_RATIO:
        return "smile"
    return "neutral"


def action_confidence(action_code, metrics, matched):
    if action_code in ("turn_left", "turn_right"):
        value = min(abs(metrics["yaw"]) / max(TURN_YAW_DEGREES, 1.0), 1.0)
        value = max(value, min(abs(metrics["nose_offset"]) / 0.18, 1.0))
    elif action_code in ("look_up", "look_down"):
        value = min(abs(metrics["pitch"]) / max(LOOK_PITCH_DEGREES, 1.0), 1.0)
    elif action_code == "mouth_open":
        value = min(metrics["mouth_open_ratio"] / MOUTH_OPEN_RATIO, 1.0)
    elif action_code == "smile":
        value = min(metrics["smile_ratio"] / SMILE_RATIO, 1.0)
    else:
        value = 0.0
    return round(max(value, 0.35 if matched else 0.0), 3)


def face_descriptor(image, points):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    x1, x2 = max(int(min(xs)) - 20, 0), min(int(max(xs)) + 20, image.shape[1])
    y1, y2 = max(int(min(ys)) - 20, 0), min(int(max(ys)) + 20, image.shape[0])
    face = image[y1:y2, x1:x2]
    if face.size == 0:
        return None

    resized = cv2.resize(face, (96, 96))
    hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv], [0, 1], None, [32, 32], [0, 180, 0, 256])
    cv2.normalize(hist, hist)
    return hist.flatten().astype(float).tolist()


def profile_path(user_id):
    safe_user_id = "".join(ch for ch in str(user_id) if ch.isalnum() or ch in ("-", "_"))
    return PROFILE_DIR / f"{safe_user_id}.json"


def descriptor_similarity(first, second):
    if not first or not second:
        return 0.0
    first = np.array(first, dtype=np.float64)
    second = np.array(second, dtype=np.float64)
    denom = float(np.linalg.norm(first) * np.linalg.norm(second))
    if denom <= 0:
        return 0.0
    return max(0.0, min(float(np.dot(first, second) / denom), 1.0))


def normalize_ocr_text(text):
    return re.sub(r"[ \t]+", " ", (text or "").replace("\r", "\n")).strip()


def fold_text(text):
    normalized = unicodedata.normalize("NFD", text or "")
    return "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn").lower()


def value_after_label(line):
    if ":" in line:
        return line.split(":", 1)[-1].strip(" :-")

    pattern = (
        r"\b(?:ho va ten|full name|name|ngay sinh|date of birth|gioi tinh|sex|"
        r"quoc tich|nationality|que quan|place of origin|place of birth|"
        r"noi thuong tru|place of residence|address|ngay cap|date of issue|"
        r"noi cap|place of issue|co gia tri den|date of expiry|expiry)\b"
    )
    parts = re.split(pattern, fold_text(line), maxsplit=1)
    if len(parts) <= 1:
        return ""
    return line[-len(parts[-1]):].strip(" :-")


def first_labeled_value(lines, labels):
    for index, line in enumerate(lines):
        folded = fold_text(line)
        if any(label in folded for label in labels):
            value = value_after_label(line)
            if value:
                return value
            if index + 1 < len(lines):
                return lines[index + 1].strip(" :-")
    return ""


def first_labeled_date(lines, labels):
    for line in lines:
        folded = fold_text(line)
        if any(label in folded for label in labels):
            match = re.search(r"\d{1,2}[/-]\d{1,2}[/-]\d{4}", line)
            if match:
                return match.group(0).replace("/", "-")
    return ""


def parse_identity_fields(text):
    normalized = normalize_ocr_text(text)
    lines = [line.strip(" :-") for line in normalized.splitlines() if line.strip()]
    compact = " ".join(lines)

    digits_compact = re.sub(r"(?<=\d)\s+(?=\d)", "", compact)
    number_match = re.search(r"\b(?:\d{9}|\d{12})\b", digits_compact)
    dob_match = re.search(r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{4})\b", compact)
    dates = re.findall(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{4}\b", compact)

    issue_date = first_labeled_date(lines, ("ngay cap", "date of issue"))
    if not issue_date and len(dates) >= 2:
        issue_date = dates[-1].replace("/", "-")

    return {
        "identity_number": number_match.group(0) if number_match else "",
        "full_name": first_labeled_value(lines, ("ho va ten", "full name", "name")),
        "date_of_birth": dob_match.group(1).replace("/", "-") if dob_match else "",
        "place_of_birth": first_labeled_value(lines, ("que quan", "place of origin", "place of birth")),
        "gender": first_labeled_value(lines, ("gioi tinh", "sex")),
        "nationality": first_labeled_value(lines, ("quoc tich", "nationality")),
        "address": first_labeled_value(lines, ("noi thuong tru", "place of residence", "address")),
        "issue_date": issue_date,
        "issue_place": first_labeled_value(lines, ("noi cap", "place of issue")),
        "expiry_date": first_labeled_date(lines, ("co gia tri den", "date of expiry", "expiry")),
        "issuing_authority": first_labeled_value(lines, ("cuc canh sat", "issuing authority", "noi cap", "place of issue")),
    }

    number_match = re.search(r"\b(?:\d{9}|\d{12})\b", compact)
    dob_match = re.search(r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{4})\b", compact)

    full_name = ""
    address = ""
    issue_date = ""
    issue_place = ""
    for index, line in enumerate(lines):
        lower = line.lower()
        if not full_name and any(key in lower for key in ("ho va ten", "họ và tên", "full name", "name")):
            full_name = line.split(":", 1)[-1].strip()
            if not full_name and index + 1 < len(lines):
                full_name = lines[index + 1]
        if not address and any(key in lower for key in ("noi thuong tru", "nơi thường trú", "address", "que quan", "quê quán")):
            address = line.split(":", 1)[-1].strip()
            if not address and index + 1 < len(lines):
                address = lines[index + 1]
        if not issue_date and any(key in lower for key in ("ngay cap", "ngày cấp", "date of issue")):
            match = re.search(r"\d{1,2}[/-]\d{1,2}[/-]\d{4}", line)
            issue_date = match.group(0) if match else ""
        if not issue_place and any(key in lower for key in ("noi cap", "nơi cấp", "place of issue")):
            issue_place = line.split(":", 1)[-1].strip()

    return {
        "identity_number": number_match.group(0) if number_match else "",
        "full_name": full_name,
        "date_of_birth": dob_match.group(1).replace("/", "-") if dob_match else "",
        "address": address,
        "issue_date": issue_date.replace("/", "-") if issue_date else "",
        "issue_place": issue_place,
    }


def run_identity_ocr(image):
    if pytesseract is None:
        return "", "PYTESSERACT_NOT_AVAILABLE"

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 7, 50, 50)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    config = "--psm 6"
    try:
        text = pytesseract.image_to_string(gray, lang=os.environ.get("CMND_OCR_LANG", "vie+eng"), config=config)
    except Exception as exc:
        return "", f"OCR_FAILED: {exc}"
    return normalize_ocr_text(text), None


def compare_identity_face(image, user_id):
    if not user_id:
        return False, 0.0, "USER_ID_MISSING"
    path = profile_path(user_id)
    if not path.exists():
        return False, 0.0, "FACE_PROFILE_NOT_FOUND"

    points, detection_error = detect_landmarks(image)
    if detection_error:
        return False, 0.0, "NO_FACE_ON_ID_CARD"

    descriptor = face_descriptor(image, points)
    if descriptor is None:
        return False, 0.0, "LOW_ID_FACE_QUALITY"

    profile = json.loads(path.read_text(encoding="utf-8"))
    confidence = round(descriptor_similarity(profile.get("descriptor"), descriptor), 3)
    return confidence >= 0.75, confidence, None


@app.get("/api/face/health")
def health():
    return jsonify(
        {
            "status": "ok",
            "service": "face-auth-api",
            "model_loaded": FACE_MESH is not None or FACE_LANDMARKER is not None,
            "landmark_backend": MEDIAPIPE_BACKEND,
            "storage_ready": PROFILE_DIR.exists(),
            "version": APP_VERSION,
        }
    )


@app.post("/api/face/action-check")
def action_check():
    purpose = request.form.get("purpose", "")
    action_code = (request.form.get("action_code") or request.form.get("actionCode") or "").strip()
    user_id, user_error = read_user_id()
    if user_error:
        return user_error
    if not action_code:
        return error_response("ACTION_CODE_MISSING", "action_code is required", user_id=user_id, purpose=purpose)

    image, upload_error = decode_upload()
    if upload_error:
        return upload_error
    points, detection_error = detect_landmarks(image)
    if detection_error:
        return detection_error

    metrics = action_metrics(points, image.shape)
    detected_action = classify_action(metrics)
    matched = detected_action == action_code
    confidence = action_confidence(action_code, metrics, matched)
    message = "Action matched" if matched else f"Detected {detected_action}; waiting for {action_code}"

    return jsonify(
        {
            "success": True,
            "action_matched": matched,
            "action_code": action_code,
            "action_message": message,
            "detected_action": detected_action,
            "confidence": confidence,
            "user_id": str(user_id or ""),
            "liveness_passed": True,
            "request_id": request_id(),
            "purpose": purpose,
            "metrics": {key: round(float(value), 4) for key, value in metrics.items()},
        }
    )


@app.post("/api/face/register")
def register():
    purpose = request.form.get("purpose", "Register")
    user_id, user_error = read_user_id()
    if user_error:
        return user_error
    if not user_id:
        return error_response("USER_ID_MISSING", "user_id is required", purpose=purpose, status=400)

    image, upload_error = decode_upload()
    if upload_error:
        return upload_error
    points, detection_error = detect_landmarks(image)
    if detection_error:
        return detection_error

    descriptor = face_descriptor(image, points)
    if descriptor is None:
        return error_response("LOW_IMAGE_QUALITY", "Cannot create face descriptor", user_id=user_id, purpose=purpose)

    profile_path(user_id).write_text(
        json.dumps({"user_id": str(user_id), "descriptor": descriptor}, ensure_ascii=True),
        encoding="utf-8",
    )
    return jsonify(
        {
            "success": True,
            "confidence": 0.95,
            "user_id": str(user_id),
            "external_user_id": f"face-profile-{user_id}",
            "liveness_passed": True,
            "request_id": request_id(),
            "purpose": purpose,
        }
    )


@app.post("/api/face/verify")
@app.post("/api/face/authenticate")
def verify():
    purpose = request.form.get("purpose", "Verify")
    user_id, user_error = read_user_id()
    if user_error:
        return user_error
    if not user_id:
        return error_response("USER_ID_MISSING", "user_id is required", purpose=purpose, status=400)

    path = profile_path(user_id)
    if not path.exists():
        return error_response("FACE_PROFILE_NOT_FOUND", "Face profile not found", user_id=user_id, purpose=purpose)

    image, upload_error = decode_upload()
    if upload_error:
        return upload_error
    points, detection_error = detect_landmarks(image)
    if detection_error:
        return detection_error

    descriptor = face_descriptor(image, points)
    profile = json.loads(path.read_text(encoding="utf-8"))
    confidence = round(descriptor_similarity(profile.get("descriptor"), descriptor), 3)
    matched = confidence >= 0.75
    return jsonify(
        {
            "success": matched,
            "confidence": confidence,
            "user_id": str(user_id),
            "external_user_id": f"face-profile-{user_id}",
            "liveness_passed": True,
            "error_code": None if matched else "FACE_NOT_MATCHED",
            "error_message": None if matched else "Face does not match registered user",
            "request_id": request_id(),
            "purpose": purpose,
        }
    )


@app.post("/api/face/ocr-cmnd")
@app.post("/api/face/qcr-cmnd")
@app.post("/api/face/cmnd-ocr")
def ocr_cmnd():
    purpose = request.form.get("purpose", "IdentityCard")
    user_id, user_error = read_user_id()
    if user_error:
        return user_error

    front_image, back_image, upload_error = decode_identity_uploads()
    if upload_error:
        return upload_error

    front_text, front_ocr_error = run_identity_ocr(front_image) if front_image is not None else ("", None)
    back_text, back_ocr_error = run_identity_ocr(back_image) if back_image is not None else ("", None)
    text = normalize_ocr_text("\n".join(part for part in (front_text, back_text) if part))
    fields = parse_identity_fields(text)
    face_image = front_image if front_image is not None else back_image
    face_matched, face_confidence, face_error = compare_identity_face(face_image, user_id)
    has_fields = any(fields.values())
    ocr_error = front_ocr_error or back_ocr_error

    return jsonify(
        {
            "success": has_fields or face_matched,
            "fields": fields,
            "raw_text": text,
            "front_raw_text": front_text,
            "back_raw_text": back_text,
            "ocr_error": ocr_error,
            "face_matched": face_matched,
            "face_confidence": face_confidence,
            "face_error": face_error,
            "user_id": str(user_id or ""),
            "request_id": request_id(),
            "purpose": purpose,
            "message": "Identity card processed" if has_fields or face_matched else "Cannot read identity card",
        }
    )


if __name__ == "__main__":
    app.run(host=os.environ.get("FACE_AUTH_HOST", "0.0.0.0"), port=int(os.environ.get("FACE_AUTH_PORT", "8000")))
