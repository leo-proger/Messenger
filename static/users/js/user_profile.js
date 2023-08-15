document.getElementById('create-post__select-image-icon').addEventListener('click', function () {
    document.getElementById('create-post__select-image').click();
});

const postInputText = document.getElementById('create-post__input-text');
autoExpandTextArea(postInputText);

const deleteImageButton = document.querySelector('.delete-uploaded-image-button');

document.getElementById('create-post__select-image').addEventListener('change', function (event) {
    const output = document.querySelector('.preview-image');
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function () {
        URL.revokeObjectURL(output.src)
    }
    deleteImageButton.classList.remove('d-none');
    deleteImageButton.setAttribute('data-filename', output.src);

    // Сохраняем изображение в LocalStorage
    const reader = new FileReader();
    reader.onload = function (event) {
        localStorage.setItem('image', event.target.result);
    };
    reader.readAsDataURL(event.target.files[0]);
});

// При загрузке страницы
window.addEventListener('load', function () {
    // Проверяем, есть ли изображение в LocalStorage
    const savedImage = localStorage.getItem('image');

    if (savedImage) {
        // Если есть, устанавливаем его как источник изображения
        document.querySelector('.preview-image').src = savedImage;
        deleteImageButton.classList.remove('d-none');
        deleteImageButton.setAttribute('data-filename', savedImage);
    }
});

deleteImageButton.addEventListener('click', function () {
    const filename = this.getAttribute('data-filename');
    const previewImage = document.querySelector(`img[src="${filename}"]`);

    const inputFile = document.getElementById('create-post__select-image');

    if (previewImage) {
        previewImage.src = '';
        deleteImageButton.classList.add('d-none')

        // Очистить input-поле
        inputFile.value = '';

        // Удалить изображение из LocalStorage
        localStorage.removeItem('image');
    }
});

const publishPostButton = document.getElementById('create-post__publish-button');
publishPostButton.addEventListener('click', function () {
    // Удалить изображение из LocalStorage
    localStorage.removeItem('image');
});




