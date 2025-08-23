const NotifySocket = new WebSocket(`ws://${window.location.host}/ws/message-notifications/${currentUserID}/`);

NotifySocket.onopen = function () {
    // console.log('open')
};

NotifySocket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    const type = data.type;

    if (type === 'new_message') {
        const receivedChatUUID = data.chat_uuid;
        const lastChatMessage = data.last_chat_message;

        if (chatUUID) {
            if (chatUUID !== receivedChatUUID) {
                const chat = document.getElementById(receivedChatUUID);
                const unreadMessagesCount = chat?.querySelector('.unread-messages-count > span');

                if (unreadMessagesCount) {
                    const count = parseInt(unreadMessagesCount.textContent, 10);
                    unreadMessagesCount.textContent = `${count + 1}`;
                } else {
                    const span = document.createElement('span');
                    span.textContent = '1';
                    const unreadMessagesCountElement = document.createElement('div');
                    unreadMessagesCountElement.classList.add('text-center', 'my-1', 'unread-messages-count');
                    unreadMessagesCountElement.appendChild(span);
                    const messageInfo = chat?.querySelector('.message-info');
                    messageInfo.appendChild(unreadMessagesCountElement);
                }

                const lastChatMessageElement = chat.querySelector('.chat-info > p');
                lastChatMessageElement.textContent = lastChatMessage;

                const timeLastChatMessage = chat?.querySelector('.time-last-message');
                timeLastChatMessage.textContent = getTimeNow();

                prependChat(receivedChatUUID);
            } else {
                markMessagesAsRead(chatUUID);
            }
        }
    }
};

NotifySocket.onclose = function (event) {
};
