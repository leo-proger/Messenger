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