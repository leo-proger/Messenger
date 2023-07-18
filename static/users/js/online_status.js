const socket = new WebSocket(`ws://${window.location.host}/ws/online/`);

socket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    const {user_id: receivedUserID, online_status: userOnlineStatus} = data;

    if (receivedUserID !== currentUserID) {
        const onlineStatusChatList = document?.querySelector(`.online-status-${receivedUserID} .online-status-chat-list`);
        const onlineStatusChatHeader = document?.querySelector(`.online-status-${receivedUserID} .online-status-chat-header`);

        if (onlineStatusChatList) {
            onlineStatusChatList.className = userOnlineStatus ? 'online online-status-chat-header' : 'offline online-status-chat-header';
        }
        if (onlineStatusChatHeader) {
            onlineStatusChatHeader.className = userOnlineStatus ? 'online online-status-chat-list' : 'offline online-status-chat-list';
        }
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

window.addEventListener('beforeunload', function (event) {
    socket.send(JSON.stringify({
        'online_status': false,
        'user_id': currentUserID,
    }))
})
