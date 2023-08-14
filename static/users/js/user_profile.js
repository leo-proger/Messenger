document.getElementById('create-post__image-icon').addEventListener('click', function () {
    document.getElementById('create-post__image').click();
});

document.getElementById('create-post__image').addEventListener('change', function () {
    const output = document.getElementById('preview_image');
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function () {
        URL.revokeObjectURL(output.src)
    }
});

const postTextInput = document.getElementById('create-post__text');
postTextInput.addEventListener('input', function() {
  postTextInput.style.height = Math.min(postTextInput.scrollHeight, 200) + 'px';
});
