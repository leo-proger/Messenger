const userID = JSON.parse(document.getElementById('json-user_id').textContent);

const NotifySocket = new WebSocket(`ws://${window.location.host}/ws/message-notifications/${userID}/`);

NotifySocket.onopen = function () {
    console.log('open')
};

NotifySocket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    const type = data.type;
    const chatUUID = data.chat_uuid;
    const lastChatMessage = data.last_chat_message;

    const chatUUIDEl = JSON.parse(document.getElementById('json-chat_uuid')?.textContent ?? 'null');

    if (type === 'new_message' && chatUUIDEl !== chatUUID) {
        const chat = document.getElementById(chatUUID);
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
            const chatInfoElement = chat?.querySelector('.chat-info')
            chatInfoElement.appendChild(unreadMessagesCountElement);
        }

        const lastChatMessageElement = chat.querySelector('.companion-info > p')
        lastChatMessageElement.textContent = lastChatMessage;

        const timeLastChatMessage = chat?.querySelector('.time-last-message');
        timeLastChatMessage.textContent = getTimeNow();

        prependChat(chatUUID);

    }
};

NotifySocket.onclose = function (event) {
};
