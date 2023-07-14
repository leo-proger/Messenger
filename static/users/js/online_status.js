const socket = new WebSocket(`ws://${window.location.host}/ws/online/`);

socket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    const receivedUserID = data.user_id;
    const userOnlineStatus = data.online_status;

    if (receivedUserID !== currentUserID) {
        const onlineStatus = document.querySelectorAll(`.online-status-${receivedUserID}`);
        const onlineStatusChatList = onlineStatus[0].querySelector('.online-status-chat-list');
        const onlineStatusChatHeader = onlineStatus[1].querySelector('.online-status-chat-header')
        console.log(onlineStatusChatHeader)

        if (userOnlineStatus) {
            if (onlineStatusChatHeader) {
                onlineStatusChatHeader.className = 'online online-status-chat-header';
            }
            onlineStatusChatList.className = 'online online-status-chat-list';
        } else {
            if (onlineStatusChatHeader) {
                onlineStatusChatHeader.className = 'offline online-status-chat-header';
            }
            onlineStatusChatList.className = 'offline online-status-chat-list';
        }
    }
}

socket.onopen = function (event) {
    console.log('Connect to Online')
    socket.send(JSON.stringify({
        'online_status': true,
        'user_id': currentUserID,
    }))
}

socket.onclose = function (event) {
    console.log('Disconnect from Online')
}

window.addEventListener('beforeunload', function (event) {
    socket.send(JSON.stringify({
        'online_status': false,
        'user_id': currentUserID,
    }))
})
