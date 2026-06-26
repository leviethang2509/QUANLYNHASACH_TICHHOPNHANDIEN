function notificationService() {
    if (typeof toastr === 'undefined') {
        var fallback = function (message) {
            alert(message);
        };
        return {
            displaySuccess: fallback,
            displayError: fallback,
            displayWarning: fallback,
            displayInfo: fallback
        };
    }

    toastr.options = {
        "debug": false,
        "positionClass": "toast-top-right",
        "onclick": null,
        "fadeIn": 300,
        "fadeOut": 1000,
        "timeOut": 3000,
        "extendedTimeOut": 1000
    }

    function displaySuccess(message) {
        toastr.success(message);


    }
    function displayError(error) {
        if (Array.isArray(error)) {
            error.forEach(function (err) {
                toastr.error(err);
            });
        } else {
            toastr.error(error);
        }
    }

    function displayWarning(message) {
        toastr.warning(message);
    }
    function displayInfo(message) {
        toastr.info(message);
    }
    return {
        displaySuccess: displaySuccess,
        displayError: displayError,
        displayWarning: displayWarning,
        displayInfo: displayInfo
    }
};
function validateFormBeforeAjax(formSelector) {
    var form = document.querySelector(formSelector);
    if (!form) {
        notificationService().displayError("Không tìm thấy form đăng ký.");
        return false;
    }

    if (typeof form.checkValidity === 'function' && !form.checkValidity()) {
        if (typeof form.reportValidity === 'function') {
            form.reportValidity();
        } else {
            notificationService().displayError("Vui lòng nhập đầy đủ các trường bắt buộc.");
        }
        return false;
    }

    return true;
}
function setSignupStatus(statusSelector, message, isError) {
    var element = document.querySelector(statusSelector);
    if (!element) return;

    element.textContent = message || '';
    element.className = isError ? 'font-size-2 mt-2 text-danger' : 'font-size-2 mt-2 text-success';
}
function setSignupLoading(statusSelector, message) {
    var element = document.querySelector(statusSelector);
    if (!element) return;

    element.className = 'font-size-2 mt-2 text-gray-600';
    element.innerHTML = '<span class="spinner-border spinner-border-sm mr-2" role="status" aria-hidden="true"></span>' + (message || 'Đang xử lý...');
}
function normalizeIdentityDateInput(value) {
    if (!value) return '';
    var text = String(value).trim();
    if (/^\d{4}-\d{2}-\d{2}$/.test(text)) return text;

    var match = text.match(/^(\d{1,2})[\/.-](\d{1,2})[\/.-](\d{4})$/);
    if (!match) return text;

    return match[3] + '-' + String(match[2]).padStart(2, '0') + '-' + String(match[1]).padStart(2, '0');
}
function parseRegisterResult(result) {
    if (typeof result === 'string') {
        try {
            return JSON.parse(result);
        } catch (error) {
            return { code: 0, message: result || "Đăng ký thất bại. Server không trả JSON hợp lệ." };
        }
    }

    return result || { code: 0, message: "Đăng ký thất bại. Server không trả dữ liệu." };
}
function handleRegisterSuccess(result, statusSelector) {
    result = parseRegisterResult(result);
    var code = typeof result === 'object' ? result.code : result;
    var message = typeof result === 'object' ? result.message : null;

    if (code == 1) {
        message = message || "Đăng ký thành công.";
        setSignupStatus(statusSelector, message, false);
        notificationService().displaySuccess(message);
        setTimeout(function () {
            window.location.href = "/Home/TrangChu";
        }, 800);
        return;
    }

    if (code == 2) {
        message = message || "Thông tin hợp lệ. Đang mở xác thực khuôn mặt...";
        setSignupStatus(statusSelector, message, false);
        notificationService().displaySuccess(message);
        openRegisterFacePopup(result.faceUserId);
        return;
    }

    if (code == -3) {
        message = message || "Số điện thoại không hợp lệ.";
    } else if (code == -1) {
        message = message || "Email này đã có người đăng ký.";
    } else if (code == -2) {
        message = message || "Người dùng này đã tồn tại.";
    } else if (code == -4) {
        message = message || "Định dạng email sai.";
    } else if (code == -5) {
        message = message || "Mật khẩu không trùng khớp.";
    } else {
        message = message || "Đăng ký thất bại. Vui lòng kiểm tra lại thông tin.";
    }

    setSignupStatus(statusSelector, message, true);
    notificationService().displayError(message);
}
function setSignupIdentityStep(formSelector, statusSelector, showIdentity) {
    var form = document.querySelector(formSelector);
    if (!form) return;

    if (showIdentity && !validateFormBeforeAjax(formSelector)) return;

    var identityBlocks = form.querySelectorAll('.signup-identity-step');
    var firstIdentityBlock = identityBlocks.length ? identityBlocks[0] : null;
    var content = firstIdentityBlock ? firstIdentityBlock.parentNode : null;

    if (content) {
        Array.prototype.forEach.call(content.children, function (element) {
            if (element.classList.contains('signup-identity-step')) return;
            if (statusSelector && element.id === statusSelector.replace('#', '')) return;

            if (!element.getAttribute('data-signup-original-display')) {
                element.setAttribute('data-signup-original-display', element.style.display || '');
            }
            element.style.display = showIdentity ? 'none' : element.getAttribute('data-signup-original-display');
        });
    }

    Array.prototype.forEach.call(identityBlocks, function (element) {
        element.style.display = showIdentity ? '' : 'none';
    });

    setSignupStatus(
        statusSelector,
        showIdentity
            ? 'Thông tin CMND/CCCD không bắt buộc. Có thể nhập tay, đọc ảnh, hoặc bấm tiếp theo để xác thực khuôn mặt.'
            : '',
        false
    );
}
window.ShowSignupIdentityStep = function (formSelector, statusSelector) {
    setSignupIdentityStep(formSelector, statusSelector, true);
};
window.ShowSignupGeneralStep = function (formSelector, statusSelector) {
    setSignupIdentityStep(formSelector, statusSelector, false);
};
document.addEventListener('click', function (event) {
    var link = event.target && event.target.closest ? event.target.closest('.js-animation-link') : null;
    if (!link) return;

    var target = link.getAttribute('data-target');
    if (target === '#login' || target === '#login1' || target === '#signup' || target === '#signup1') {
        setSignupIdentityStep('#Sigup', '#signupStatus', false);
        setSignupIdentityStep('#Sigup1', '#signupStatusMobile', false);
    }
});
function openRegisterFacePopup(userId) {
    var panel = document.getElementById('registerFacePanel');
    var video = document.getElementById('registerFaceVideo');
    var button = document.getElementById('registerFaceButton');
    var closeButton = document.getElementById('closeRegisterFace');
    var status = document.getElementById('registerFaceStatus');

    if (!panel || !video || !button || !closeButton || !window.FaceCapture || !userId) {
        window.location.href = "/Users/RegisterFace";
        return;
    }

    var initialized = panel.getAttribute('data-initialized') === 'true';

    function setFaceStatus(message, isError) {
        if (!status) return;
        status.textContent = message || '';
        status.className = isError ? 'font-size-2 mt-2 text-danger' : 'font-size-2 mt-2 text-success';
    }

    function closePanel() {
        FaceCapture.stopCamera(panel._registerFaceStream);
        panel._registerFaceStream = null;
        panel.hidden = true;
        document.body.classList.remove('face-auth-modal-open');
    }

    function startCamera() {
        setFaceStatus('Đang mở camera...', false);
        FaceCapture.startCamera(video, status).then(function (cameraStream) {
            panel._registerFaceStream = cameraStream;
            setFaceStatus('Camera đã sẵn sàng. Vui lòng nhìn thẳng và bấm xác thực.', false);
        }).catch(function () {
            setFaceStatus('Không thể mở camera. Vui lòng cấp quyền camera.', true);
        });
    }

    panel.hidden = false;
    document.body.classList.add('face-auth-modal-open');
    panel.setAttribute('data-user-id', userId);
    startCamera();

    if (initialized) return;
    panel.setAttribute('data-initialized', 'true');

    closeButton.addEventListener('click', closePanel);
    panel.addEventListener('click', function (event) {
        if (event.target === panel || event.target.getAttribute('data-face-close') === 'closeRegisterFace') {
            closePanel();
        }
    });

    button.addEventListener('click', function () {
        var currentUserId = panel.getAttribute('data-user-id');
        button.disabled = true;
        setFaceStatus('Đang gửi ảnh khuôn mặt...', false);

        FaceCapture.captureBlob(video)
            .then(function (blob) {
                return FaceCapture.uploadFace('/FaceAuth/RegisterFace', blob, {
                    userId: currentUserId,
                    user_id: currentUserId,
                    purpose: 'Register'
                });
            })
            .then(function (result) {
                if (result && result.success === true) {
                    setFaceStatus(result.message || 'Đăng ký tài khoản và khuôn mặt thành công.', false);
                    FaceCapture.stopCamera(panel._registerFaceStream);
                    panel._registerFaceStream = null;
                    setTimeout(function () {
                        window.location.href = '/Home/TrangChu';
                    }, 900);
                    return;
                }

                setFaceStatus((result && (result.error || result.message)) || 'Xác thực khuôn mặt thất bại. Vui lòng thử lại.', true);
            })
            .catch(function () {
                setFaceStatus('Không thể chụp hoặc gửi ảnh khuôn mặt.', true);
            })
            .then(function () {
                button.disabled = false;
            });
    });
}
var login = function () {
    var data = $('#loginForm').serialize();
    $.ajax({
        type: "POST",
        url: "/dang-nhap",
        data: data,
        success: function (result) {
            if (result == 1) {
                notificationService().displaySuccess("Đăng nhập thành công.");
                setTimeout(function () {
                    window.location.href = "/Home/TrangChu"
                }, 2000);
            }
            else if (result == 10) {
                notificationService().displaySuccess("Đăng nhập quản trị thành công.");
                setTimeout(function () {
                    window.location.href = "/Admin/Homes/Index"
                }, 800);
            }
            else if (result == 2) {
                notificationService().displayInfo("Vui lòng xác thực khuôn mặt.");
                setTimeout(function () {
                    window.location.href = "/Users/LoginMFA"
                }, 800);
            }
            else if (result == -3) {
                notificationService().displayError("Tài khoản này không có quyền truy cập");
            }
            else if (result == -1) {
                notificationService().displayError("Tài khoản đã bị khóa");
            }
            else if (result == -2) {
                notificationService().displayError("Mật khẩu sai.");
            }
            else if (result == 0) {
                notificationService().displayError("Tài khoản không tồn tại.");
            }
            else {
                notificationService().displayError("Đăng nhập không thành công");
            }
        }
    })

}
var loginMobile = function () {
    var data = $('#loginFormMobile').serialize();
    $.ajax({
        type: "POST",
        url: "/dang-nhap",
        data: data,
        success: function (result) {
            if (result == 1) {
                notificationService().displaySuccess("Đăng nhập thành công.");
                setTimeout(function () {
                    window.location.href = "/Home/TrangChu"
                }, 2000);
            }
            else if (result == 10) {
                notificationService().displaySuccess("Đăng nhập quản trị thành công.");
                setTimeout(function () {
                    window.location.href = "/Admin/Homes/Index"
                }, 800);
            }
            else if (result == 2) {
                notificationService().displayInfo("Vui lòng xác thực khuôn mặt.");
                setTimeout(function () {
                    window.location.href = "/Users/LoginMFA"
                }, 800);
            }
            else if (result == -3) {
                notificationService().displayError("Tài khoản này không có quyền truy cập.");
            }
            else if (result == -1) {
                notificationService().displayError("Tài khoản đã bị khóa.");
            }
            else if (result == -2) {
                notificationService().displayError("Mật khẩu sai.");
            }
            else if (result == 0) {
                notificationService().displayError("Tài khoản không tồn tại.");
            }
            else {
                notificationService().displayError("Đăng nhập không thành công.");
            }
        }
    })

}
window.Sigup = function () {
    if (!validateFormBeforeAjax('#Sigup')) return;

    var data = $('#Sigup').serialize();
    setSignupStatus('#signupStatus', 'Đang gửi thông tin đăng ký...', false);
    $.ajax({
        type: "POST",
        url: "/Users/RegisterUser",
        dataType: "json",
        data: data,
        success: function (result) {
            handleRegisterSuccess(result, '#signupStatus');
        },
        error: function (xhr) {
            var message = (xhr.responseJSON && xhr.responseJSON.message) || xhr.responseText || "Không thể gửi yêu cầu đăng ký.";
            setSignupStatus('#signupStatus', message, true);
            notificationService().displayError(message);
        }
    })

}
window.SigupMobile = function () {
    if (!validateFormBeforeAjax('#Sigup1')) return;

    var data = $('#Sigup1').serialize();
    setSignupStatus('#signupStatusMobile', 'Đang gửi thông tin đăng ký...', false);
    $.ajax({
        type: "POST",
        url: "/Users/RegisterUser",
        dataType: "json",
        data: data,
        success: function (result) {
            handleRegisterSuccess(result, '#signupStatusMobile');
        },
        error: function (xhr) {
            var message = (xhr.responseJSON && xhr.responseJSON.message) || xhr.responseText || "Không thể gửi yêu cầu đăng ký.";
            setSignupStatus('#signupStatusMobile', message, true);
            notificationService().displayError(message);
        }
    })

}
window.signup = window.Sigup;
window.Signup = window.Sigup;
window.signUp = window.Sigup;
window.signupMobile = window.SigupMobile;
window.SignupMobile = window.SigupMobile;
window.signUpMobile = window.SigupMobile;
window.UploadSignupIdentityCard = function (formSelector, statusSelector) {
    var form = document.querySelector(formSelector);
    if (!form) return;

    var frontInput = form.querySelector('[name="IdentityOcrFrontFile"]') || form.querySelector('[name="IdentityOcrFile"]');
    var backInput = form.querySelector('[name="IdentityOcrBackFile"]');
    var hasFront = frontInput && frontInput.files && frontInput.files.length;
    var hasBack = backInput && backInput.files && backInput.files.length;
    if (!hasFront && !hasBack) {
        setSignupStatus(statusSelector, 'Vui lòng chọn ảnh CMND/CCCD mặt trước hoặc mặt sau để đọc dữ liệu.', true);
        return;
    }

    var data = new FormData();
    if (hasFront) data.append('front_file', frontInput.files[0]);
    if (hasBack) data.append('back_file', backInput.files[0]);
    var button = findSignupOcrButton(form);
    if (button) button.disabled = true;
    setSignupLoading(statusSelector, 'Đang đọc CMND/CCCD...');
    $.ajax({
        type: "POST",
        url: "/FaceAuth/OcrCmndDraft",
        data: data,
        processData: false,
        contentType: false,
        success: function (result) {
            if (!result || !result.success) {
                var failedMessage = (result && (result.message || result.error || result.ocr_error || result.ocrError)) || 'Không thể đọc CMND/CCCD.';
                setSignupStatus(statusSelector, failedMessage, true);
                notificationService().displayError(failedMessage);
                return;
            }

            var fields = result.fields || {};
            if (fields.identityNumber) $(form).find('[name="IdentityNumber"]').val(fields.identityNumber);
            if (fields.fullName) $(form).find('[name="IdentityFullName"]').val(fields.fullName);
            if (fields.fullName) $(form).find('[name="Name"]').val(fields.fullName);
            if (fields.address) $(form).find('[name="IdentityAddress"]').val(fields.address);
            if (fields.placeOfBirth) $(form).find('[name="IdentityPlaceOfBirth"]').val(fields.placeOfBirth);
            if (fields.gender) $(form).find('[name="IdentityGender"]').val(fields.gender);
            if (fields.nationality) $(form).find('[name="IdentityNationality"]').val(fields.nationality);
            if (fields.issuePlace) $(form).find('[name="IdentityIssuePlace"]').val(fields.issuePlace);
            if (fields.dateOfBirth) $(form).find('[name="IdentityDateOfBirth"]').val(normalizeIdentityDateInput(fields.dateOfBirth));
            if (fields.issueDate) $(form).find('[name="IdentityIssueDate"]').val(normalizeIdentityDateInput(fields.issueDate));
            if (fields.expiryDate) $(form).find('[name="IdentityExpiryDate"]').val(normalizeIdentityDateInput(fields.expiryDate));
            if (fields.issuingAuthority) $(form).find('[name="IdentityIssuingAuthority"]').val(fields.issuingAuthority);
            lockSignupIdentityFields(form);
            setSignupStatus(statusSelector, 'Đã đọc CMND/CCCD thành công. Vui lòng kiểm tra lại dữ liệu trước khi tiếp tục.', false);
            notificationService().displaySuccess('Đã đọc CMND/CCCD thành công.');
        },
        error: function () {
            setSignupStatus(statusSelector, 'Không thể đọc CMND/CCCD.', true);
            notificationService().displayError('Không thể đọc CMND/CCCD.');
        }
    }).always(function () {
        if (button) button.disabled = false;
    });
}
function findSignupOcrButton(form) {
    var buttons = form.querySelectorAll('button');
    for (var index = 0; index < buttons.length; index++) {
        if ((buttons[index].getAttribute('onclick') || '').indexOf('UploadSignupIdentityCard') >= 0) {
            return buttons[index];
        }
    }
    return null;
}
function lockSignupIdentityFields(form) {
    var names = [
        'Name',
        'IdentityNumber',
        'IdentityFullName',
        'IdentityDateOfBirth',
        'IdentityAddress',
        'IdentityIssueDate',
        'IdentityIssuePlace'
    ];

    names.forEach(function (name) {
        var input = form.querySelector('[name="' + name + '"]');
        if (input && input.value) {
            input.readOnly = true;
            input.classList.add('bg-light');
        }
    });
}
function bindIdentityPreviewInputs(scope) {
    var root = scope || document;
    var inputs = root.querySelectorAll('.js-identity-preview');
    Array.prototype.forEach.call(inputs, function (input) {
        input.addEventListener('change', function () {
            var file = input.files && input.files[0];
            var preview = document.querySelector(input.getAttribute('data-preview'));
            var placeholder = document.querySelector(input.getAttribute('data-placeholder'));
            if (!file || !preview) return;

            var reader = new FileReader();
            reader.onload = function (event) {
                preview.src = event.target.result;
                preview.classList.remove('d-none');
                if (placeholder) placeholder.classList.add('d-none');
            };
            reader.readAsDataURL(file);
        });
    });
}
bindIdentityPreviewInputs(document);
var retestPass = function () {
    var data = $('#retesPass').serialize();
    $.ajax({
        type: "POST",
        url: "/Users/RetestPassWord",
        data: data,
        success: function (result) {
            if (result == 1) {
                notificationService().displaySuccess("Đã gửi mật khẩu mới đến Email.");
                setTimeout(function () {
                    window.location.reload(1)
                }, 2000);
            }
            else if (result == -3) {
                notificationService().displayError("Email nhập không đúng định đạng.");
            }
            else if (result == -1) {
                notificationService().displayError("Không cấp được mật khẩu.");
            }
            else if (result == -2) {
                notificationService().displayError("Không tìm thấy tài khoản nào.");
            }

            else if (result == 0) {
                notificationService().displayError("Yêu cầu nhập đầy đủ các trường.");
            }

        }
    })

}
var retestPassMobile = function () {
    var data = $('#retesPass1').serialize();
    $.ajax({
        type: "POST",
        url: "/Users/RetestPassWord",
        data: data,
        success: function (result) {
            if (result == 1) {
                notificationService().displaySuccess("Đã gửi mật khẩu mới đến Email.");
                setTimeout(function () {
                    window.location.reload(1)
                }, 2000);
            }
            else if (result == -3) {
                notificationService().displayError("Email nhập không đúng định đạng.");
            }
            else if (result == -1) {
                notificationService().displayError("Không cấp được mật khẩu.");
            }
            else if (result == -2) {
                notificationService().displayError("Không tìm thấy tài khoản nào.");
            }

            else if (result == 0) {
                notificationService().displayError("Yêu cầu nhập đầy đủ các trường.");
            }

        }
    })

}
