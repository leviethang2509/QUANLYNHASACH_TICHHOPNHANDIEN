function notificationService() {
    toastr.options = {
        "debug": false,
        "positionClass": "toast-top-right",
        "onclick": null,
        "fadeIn": 300,
        "fadeOut": 1000,
        "timOut": 3000,
        "extendedTimOut": 1000
    }

    function displaySuccess(message) {
        toastr.success(message);


    }
    function displayError(error) {
        if (Array.isArray(error)) {
            error.each(function (err) {
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
        displayWarning: displayError,
        displayInfo: displayInfo
    }
};
window.ChangeUserProfile = function () {
    var profileForm = document.getElementById('ChangeUserProfile');
    if (profileForm && profileForm.getAttribute('data-identity-locked') === 'true') {
        notificationService().displayInfo("Thông tin đã được khóa sau khi có đủ ảnh CMND/CCCD hai mặt. Bạn chỉ có thể cập nhật lại ảnh CMND/CCCD.");
        return;
    }

    var data = $('#ChangeUserProfile').serialize();
    $.ajax({
        type: "POST",
        url: "/sua-thong-tin",
        data: data,
        success: function (result) {
            if (result == 1) {
                notificationService().displaySuccess("Cập nhật thông tin thành công.");
                setTimeout(function () {
                    window.location.reload(1)
                }, 2000);
            }

            else if (result == -1) {
                notificationService().displayError("Định dạng số điện thoại không hợp lệ");
            }
            else if (result == -2) {
                notificationService().displayError("Định dạng email không hợp lệ.");
            }
            else if (result == 0) {
                notificationService().displayError("Cập nhật thông tin không thành công.");
            }

        }
    })

}
window.ChangePass = function () {
    var data = $('#changePass').serialize();
    $.ajax({
        type: "POST",
        url: "/doi-mat-khau",
        data: data,
        success: function (result) {
            if (result == 1) {
                notificationService().displaySuccess("Đổi mật khẩu thành công.");
                setTimeout(function () {
                    window.location.reload(1)
                }, 2000);
            }
            else if (result == -3) {
                notificationService().displayError("Mật khẩu hiện tại không chính xác");
            }
            else if (result == -4) {
                notificationService().displayError("Mật khẩu mới và xác nhận không được để trống");
            }
            else if (result == -1) {
                notificationService().displayError("Mật khẩu không được để trống");
            }
            else if (result == -2) {
                notificationService().displayError("Xác nhận mật khẩu không trùng khớp");
            }
            else if (result == 0) {
                notificationService().displayError("Lỗi không thể cập nhật mật khẩu.");
            }

        }
    })

}

window.UploadIdentityCard = function () {
    var form = document.getElementById('IdentityCardUploadForm');
    var status = document.getElementById('identityCardUploadStatus');
    var button = document.getElementById('profileIdentityOcrBtn');
    if (!form) return;

    var data = new FormData(form);
    if (!hasIdentityUploadFile(form)) {
        setProfileIdentityStatus(status, 'Vui lòng chọn ảnh CMND/CCCD mặt trước hoặc mặt sau.', true);
        return;
    }

    if (status) {
        status.className = 'font-size-2 mt-3 text-gray-600';
        status.innerHTML = '<span class="spinner-border spinner-border-sm mr-2" role="status" aria-hidden="true"></span>Đang tải CMND/CCCD và đọc thông tin...';
    }
    if (button) button.disabled = true;

    $.ajax({
        type: "POST",
        url: "/FaceAuth/OcrCmnd",
        data: data,
        processData: false,
        contentType: false,
        success: function (result) {
            if (result && result.success) {
                var fields = result.fields || {};
                $('[name="IdentityNumber"]').val(fields.identityNumber || $('[name="IdentityNumber"]').val());
                $('[name="IdentityFullName"]').val(fields.fullName || $('[name="IdentityFullName"]').val());
                if (fields.fullName) $('[name="Name"]').val(fields.fullName);
                $('[name="IdentityAddress"]').val(fields.address || $('[name="IdentityAddress"]').val());
                $('[name="IdentityPlaceOfBirth"]').val(fields.placeOfBirth || $('[name="IdentityPlaceOfBirth"]').val());
                $('[name="IdentityGender"]').val(fields.gender || $('[name="IdentityGender"]').val());
                $('[name="IdentityNationality"]').val(fields.nationality || $('[name="IdentityNationality"]').val());
                $('[name="IdentityIssuePlace"]').val(fields.issuePlace || $('[name="IdentityIssuePlace"]').val());
                if (fields.dateOfBirth) $('[name="IdentityDateOfBirth"]').val(normalizeIdentityDateInput(fields.dateOfBirth));
                if (fields.issueDate) $('[name="IdentityIssueDate"]').val(normalizeIdentityDateInput(fields.issueDate));
                if (fields.expiryDate) $('[name="IdentityExpiryDate"]').val(normalizeIdentityDateInput(fields.expiryDate));
                if (fields.issuingAuthority) $('[name="IdentityIssuingAuthority"]').val(fields.issuingAuthority);
                notificationService().displaySuccess("Đã đọc thông tin CMND/CCCD.");
                if (status) {
                    status.className = 'font-size-2 mt-3 text-success';
                    status.textContent = result.faceMatched
                        ? 'Đã đọc thông tin và khuôn mặt trên CMND/CCCD khớp tài khoản.'
                        : 'Đã đọc thông tin. Hồ sơ đã được cập nhật từ ảnh CMND/CCCD.';
                }
                lockProfileIdentityFields();
            } else {
                var message = (result && (result.message || result.error || result.ocr_error || result.ocrError)) || 'Không thể đọc CMND/CCCD.';
                notificationService().displayError(message);
                if (status) {
                    status.className = 'font-size-2 mt-3 text-danger';
                    status.textContent = message;
                }
            }
        },
        error: function () {
            notificationService().displayError("Không thể tải CMND/CCCD.");
            if (status) {
                status.className = 'font-size-2 mt-3 text-danger';
                status.textContent = 'Không thể tải CMND/CCCD.';
            }
        }
    }).always(function () {
        if (button) button.disabled = false;
    });
};

function setProfileIdentityStatus(status, message, isError) {
    if (!status) return;
    status.className = isError ? 'font-size-2 mt-3 text-danger' : 'font-size-2 mt-3 text-success';
    status.textContent = message || '';
}

function hasIdentityUploadFile(form) {
    var front = form.querySelector('[name="front_file"]');
    var back = form.querySelector('[name="back_file"]');
    return (front && front.files && front.files.length) || (back && back.files && back.files.length);
}

function lockProfileIdentityFields() {
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
        var input = document.querySelector('#ChangeUserProfile [name="' + name + '"]');
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
lockProfileWhenIdentityImagesExist();

function normalizeIdentityDateInput(value) {
    if (!value) return '';
    var text = String(value).trim();
    if (/^\d{4}-\d{2}-\d{2}$/.test(text)) return text;

    var match = text.match(/^(\d{1,2})[\/.-](\d{1,2})[\/.-](\d{4})$/);
    if (!match) return text;

    return match[3] + '-' + String(match[2]).padStart(2, '0') + '-' + String(match[1]).padStart(2, '0');
}

function lockProfileWhenIdentityImagesExist() {
    var form = document.getElementById('ChangeUserProfile');
    if (!form || form.getAttribute('data-identity-locked') !== 'true') return;

    var inputs = form.querySelectorAll('input, textarea, select');
    Array.prototype.forEach.call(inputs, function (input) {
        if (input.type === 'hidden') return;
        input.readOnly = true;
        input.classList.add('bg-light');
    });
}


var giaohanghoanthanh = {
    init: function () {
        giaohanghoanthanh.registerEvents();
    },
    registerEvents: function (e) {
        $('.success_order').off('click').on('click', function (e)// off tất cả rồi on khi ấn click 1 hoạt động nó chỉ on cái đó thôi
        {
            e.preventDefault();
            var btn = $(this);

            var id = btn.data('id'); // lấy được id vì nút btn mình nhấn vào , lấy ra thuộc tính data và đăng sau là id data-id
            $.ajax(
                {
                    url: "/Users/ChangeSuccessOrder",
                    data: { id: id },// truyền vào tham số của cái id đấy id chính là id truyền vào
                    dataType: "json",// có cái datatype truyền lên rồi ko cần contentType nữa
                    type: "POST",// trên controler dăt post,

                    success: function (response) {
                        if (response.NhanHang == 1) {
                            notificationService().displaySuccess("Đã nhận hàng thành công.")

                            setTimeout(function () {
                                window.location.reload(1)
                            }, 2000);
                        }
                    }
                });
        });

    }
}
giaohanghoanthanh.init();
