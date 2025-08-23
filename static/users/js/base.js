function scrollDown(tag, note = null) {
    if (note === 'sharp') {
        tag.scrollTo({
            top: tag.scrollHeight,
            behavior: 'auto',
        });
    } else {
        tag.scrollTo({
            top: tag.scrollHeight,
            behavior: 'smooth',
        });
    }
}

function getTimeNow() {
    const currentDate = new Date();
    let hours = currentDate.getHours();
    let minutes = currentDate.getMinutes();

    return hours + ":" + minutes;
}

function autoExpandTextArea(element) {
    element.addEventListener('input', function () {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
}

function markMessagesAsRead(chatUUID) {
    const markAsReadUrl = `/inbox/notifications/mark-all-as-read/`;
    const xhr = new XMLHttpRequest();
    xhr.open('GET', markAsReadUrl, true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            const chatElement = document.getElementById(chatUUID).querySelector('.unread-messages-count');
            if (chatElement !== null) {
                chatElement.remove();
            }
        }
    };
    xhr.send();
}