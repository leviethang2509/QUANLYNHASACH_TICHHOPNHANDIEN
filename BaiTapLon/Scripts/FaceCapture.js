;(function () {
    function byId(id) {
        return document.getElementById(id);
    }

    function setStatus(element, message, isError) {
        if (!element) return;
        element.textContent = message || '';
        element.className = isError ? 'text-danger' : 'text-success';
    }

    function startCamera(videoElement, statusElement) {
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            setStatus(statusElement, 'Trình duyệt không hỗ trợ camera.', true);
            return Promise.reject(new Error('Camera is not supported'));
        }

        return navigator.mediaDevices.getUserMedia({ video: true })
            .then(function (stream) {
                videoElement.srcObject = stream;
                return videoElement.play().then(function () {
                    setStatus(statusElement, 'Camera đã sẵn sàng.', false);
                    return stream;
                });
            })
            .catch(function (error) {
                setStatus(statusElement, 'Không thể mở camera. Vui lòng cấp quyền camera.', true);
                throw error;
            });
    }

    function stopCamera(stream) {
        if (!stream) return;
        stream.getTracks().forEach(function (track) {
            track.stop();
        });
    }

    function requestCameraPermission(statusElement) {
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            setStatus(statusElement, 'Trinh duyet khong ho tro camera.', true);
            return Promise.reject(new Error('Camera is not supported'));
        }

        return navigator.mediaDevices.getUserMedia({ video: true })
            .then(function (stream) {
                stopCamera(stream);
                setStatus(statusElement, 'Quyen camera da san sang.', false);
                return true;
            })
            .catch(function (error) {
                setStatus(statusElement, 'Vui long cap quyen camera de xac thuc khuon mat.', true);
                throw error;
            });
    }

    function captureBlob(videoElement) {
        return new Promise(function (resolve, reject) {
            if (!videoElement.videoWidth || !videoElement.videoHeight) {
                reject(new Error('Camera frame is not ready'));
                return;
            }

            var canvas = document.createElement('canvas');
            canvas.width = videoElement.videoWidth;
            canvas.height = videoElement.videoHeight;
            canvas.getContext('2d').drawImage(videoElement, 0, 0);
            canvas.toBlob(function (blob) {
                if (!blob) {
                    reject(new Error('Cannot capture image'));
                    return;
                }
                resolve(blob);
            }, 'image/jpeg', 0.9);
        });
    }

    function uploadFace(url, blob, extraFields) {
        var form = new FormData();
        form.append('file', blob, 'face.jpg');

        Object.keys(extraFields || {}).forEach(function (key) {
            if (extraFields[key] !== undefined && extraFields[key] !== null) {
                form.append(key, extraFields[key]);
            }
        });

        return fetch(url, {
            method: 'POST',
            body: form,
            credentials: 'same-origin'
        }).then(function (response) {
            var contentType = response.headers.get('content-type') || '';
            if (contentType.indexOf('application/json') >= 0) {
                return response.json();
            }

            if (!response.ok) {
                return { success: false, error: response.statusText || 'Upload failed' };
            }

            return { success: true };
        });
    }

    function init(options) {
        var video = byId(options.videoId);
        var button = byId(options.buttonId);
        var status = options.statusId ? byId(options.statusId) : null;
        var stream = null;

        startCamera(video, status).then(function (cameraStream) {
            stream = cameraStream;
        });

        button.addEventListener('click', function () {
            button.disabled = true;
            setStatus(status, 'Đang gửi ảnh khuôn mặt...', false);

            captureBlob(video)
                .then(function (blob) {
                    return uploadFace(options.uploadUrl, blob, options.fields || {});
                })
                .then(function (result) {
                    if (typeof options.onResult === 'function') {
                        options.onResult(result);
                    } else if (result && result.success !== false) {
                        setStatus(status, 'Xác thực thành công.', false);
                    } else {
                        setStatus(status, (result && result.error) || 'Xác thực thất bại.', true);
                    }
                })
                .catch(function (error) {
                    setStatus(status, error.message || 'Không thể chụp ảnh.', true);
                })
                .then(function () {
                    button.disabled = false;
                });
        });

        window.addEventListener('beforeunload', function () {
            stopCamera(stream);
        });
    }

    window.FaceCapture = {
        init: init,
        startCamera: startCamera,
        stopCamera: stopCamera,
        captureBlob: captureBlob,
        uploadFace: uploadFace,
        requestCameraPermission: requestCameraPermission
    };
})();
