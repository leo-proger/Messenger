const socket = new WebSocket(`ws://${window.location.host}/ws/online/`);

socket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    const {user_id: receivedUserID, online_status: userOnlineStatus} = data;

    if (receivedUserID !== currentUserID) {
        updateOnlineStatus(userOnlineStatus, receivedUserID);
    }
}

socket.onopen = function (event) {
    socket.send(JSON.stringify({
        'online_status': true,
        'user_id': currentUserID,
    }))
}

socket.onclose = function (event) {
}

function updateOnlineStatus(userOnlineStatus, receivedUserID) {
    const onlineClass = 'online';
    const offlineClass = 'offline';
    const chatListClass = 'online-status-chat-list';
    const chatHeaderClass = 'online-status-chat-header';

    const statusClassName = userOnlineStatus ? onlineClass : offlineClass;

    document.querySelectorAll(`.online-status-${receivedUserID} .${chatListClass}, .online-status-${receivedUserID} .${chatHeaderClass}`).forEach(el => {
        if (el.classList.contains(chatListClass)) {
            el.className = `${statusClassName} ${chatListClass}`;
        }
        if (el.classList.contains(chatHeaderClass)) {
            el.className = `${statusClassName} ${chatHeaderClass}`;
        }
    });
}
