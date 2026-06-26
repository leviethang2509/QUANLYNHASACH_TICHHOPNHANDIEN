;(function () {
    var storageKey = 'qlnhasach.localFavorites.v1';

    function readLocalFavorites() {
        try {
            var value = JSON.parse(localStorage.getItem(storageKey) || '[]');
            return Array.isArray(value) ? value.map(String) : [];
        } catch (e) {
            return [];
        }
    }

    function writeLocalFavorites(ids) {
        localStorage.setItem(storageKey, JSON.stringify(ids.map(String)));
    }

    function toggleLocalFavorite(productId) {
        var ids = readLocalFavorites();
        var id = String(productId);
        var index = ids.indexOf(id);
        var isFavorite = index < 0;
        if (isFavorite) {
            ids.unshift(id);
        } else {
            ids.splice(index, 1);
        }
        writeLocalFavorites(ids);
        return isFavorite;
    }

    function postFavorite(productId) {
        var form = new FormData();
        form.append('productId', productId);
        return fetch('/Users/ToggleFavorite', {
            method: 'POST',
            body: form,
            credentials: 'same-origin'
        }).then(function (response) { return response.json(); });
    }

    function syncLocalFavorites() {
        var ids = readLocalFavorites();
        if (!ids.length) return Promise.resolve(false);

        var form = new FormData();
        ids.forEach(function (id) { form.append('productIds', id); });
        return fetch('/Users/SyncLocalFavorites', {
            method: 'POST',
            body: form,
            credentials: 'same-origin'
        }).then(function (response) { return response.json(); })
            .then(function (result) {
                if (!result || !result.success) return false;
                localStorage.removeItem(storageKey);
                return true;
            }).catch(function () {
                return false;
            });
    }

    function setButtonState(button, isFavorite) {
        button.classList.toggle('is-favorite', isFavorite);
        if (button.tagName.toLowerCase() === 'button' && button.getAttribute('data-icon-only') !== 'true') {
            var icon = button.querySelector('i');
            button.textContent = isFavorite ? 'Bỏ yêu thích' : 'Thêm vào yêu thích';
            if (icon) {
                button.insertBefore(icon, button.firstChild);
                icon.classList.add('mr-2');
            }
        }
        button.setAttribute('title', isFavorite ? 'Bỏ yêu thích' : 'Thêm vào yêu thích');
    }

    function removeFavoriteCard(button) {
        if (window.location.pathname.indexOf('/yeu-thich') !== 0) return;
        var card = button.closest('.js-favorite-row') || button.closest('.js-local-favorite-card') || button.closest('.col-sm-6');
        if (card) card.parentNode.removeChild(card);
    }

    function formatPrice(price) {
        return (price || 0).toLocaleString('vi-VN') + 'đ';
    }

    function loadLocalFavoritePage() {
        var container = document.getElementById('localFavoriteList');
        if (!container) return;

        var ids = readLocalFavorites();
        var empty = document.getElementById('localFavoriteEmpty');
        if (!ids.length) {
            if (empty) empty.style.display = 'block';
            return;
        }

        var form = new FormData();
        ids.forEach(function (id) { form.append('productIds', id); });
        fetch('/Users/LocalFavoriteProducts', {
            method: 'POST',
            body: form,
            credentials: 'same-origin'
        }).then(function (response) { return response.json(); })
            .then(function (result) {
                if (!result || !result.success || !result.products || !result.products.length) {
                    if (empty) empty.style.display = 'block';
                    return;
                }

                container.innerHTML = result.products.map(function (item) {
                    var url = '/chi-tiet/' + item.metaTitle + '-' + item.id;
                    return '<div class="col-sm-6 col-lg-4 mb-5 js-local-favorite-card">' +
                        '<div class="border h-100 p-3">' +
                        '<a href="' + url + '" class="d-block text-center mb-3"><img src="' + item.image + '" width="120" height="180" class="img-fluid" alt="' + item.name + '" /></a>' +
                        '<h2 class="font-size-3 text-height-2 crop-text-2"><a class="text-dark" href="' + url + '">' + item.name + '</a></h2>' +
                        '<div class="font-size-2 text-gray-700 mb-2">' + (item.author || '') + '</div>' +
                        '<div class="font-weight-medium mb-3">' + formatPrice(item.price) + '</div>' +
                        '<button type="button" class="btn btn-outline-danger rounded-0 js-favorite-toggle is-favorite" data-local-only="true" data-product-id="' + item.id + '">Bỏ yêu thích</button>' +
                        '</div></div>';
                }).join('');
            }).catch(function () {
                if (empty) empty.style.display = 'block';
            });
    }

    document.addEventListener('DOMContentLoaded', function () {
        var ids = readLocalFavorites();
        document.querySelectorAll('.js-favorite-toggle').forEach(function (button) {
            if (ids.indexOf(String(button.getAttribute('data-product-id'))) >= 0) {
                setButtonState(button, true);
            }
        });
        syncLocalFavorites().then(function (synced) {
            if (synced && window.location.pathname.indexOf('/yeu-thich-') === 0) {
                window.location.reload();
                return;
            }
            loadLocalFavoritePage();
        });
    });

    document.addEventListener('click', function (event) {
        var button = event.target.closest('.js-favorite-toggle');
        if (!button) return;
        event.preventDefault();

        var productId = button.getAttribute('data-product-id');
        if (!productId) return;

        if (button.getAttribute('data-local-only') === 'true') {
            var localState = toggleLocalFavorite(productId);
            setButtonState(button, localState);
            if (!localState) removeFavoriteCard(button);
            return;
        }

        button.disabled = true;
        postFavorite(productId)
            .then(function (result) {
                if (result && result.useLocal) {
                    var isLocalFavorite = toggleLocalFavorite(productId);
                    setButtonState(button, isLocalFavorite);
                    if (!isLocalFavorite) removeFavoriteCard(button);
                    return;
                }

                if (!result || !result.success) {
                    alert((result && result.message) || 'Không thể cập nhật yêu thích.');
                    return;
                }

                setButtonState(button, result.isFavorite);
                if (!result.isFavorite) removeFavoriteCard(button);
            })
            .catch(function () {
                var isLocalFavorite = toggleLocalFavorite(productId);
                setButtonState(button, isLocalFavorite);
            })
            .then(function () {
                button.disabled = false;
            });
    });
})();
