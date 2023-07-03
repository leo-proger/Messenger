let chatSocket = null;

const initialize = function (newChatUUID = null, newLastChatMessage = null) {

    const chatUUID = newChatUUID !== null ? newChatUUID : JSON.parse(document.getElementById('json-chat_uuid').textContent);

    chatSocket = new WebSocket(`ws://${window.location.host}/ws/chats/${chatUUID}/`);

    const email = JSON.parse(document.getElementById('json-email').textContent);
    const userIcon = JSON.parse(document.getElementById('json-user_icon').textContent);

    const chatMessagesContainer = document.getElementById('chat-messages');
    let currentMessageGroup = null;

    chatSocket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        const message = data.message;
        const sender = data.sender;

        if (sender === email) {
            const messageSentContainer = document.createElement('div');
            messageSentContainer.classList.add('message-sent');

            const messageSentText = document.createElement('div');
            messageSentText.classList.add('message-sent-text');
            messageSentText.textContent = message;

            if (!currentMessageGroup || currentMessageGroup.classList.contains('message-group-received')) {
                currentMessageGroup = document.createElement('div');
                currentMessageGroup.classList.add('message-group-sent');
                document.querySelector('#chat-messages > div').appendChild(currentMessageGroup);
            }

            messageSentContainer.appendChild(messageSentText);
            currentMessageGroup.appendChild(messageSentContainer);

            const sentMessages = currentMessageGroup.getElementsByClassName('message-sent');
            if (sentMessages.length > 1) {
                const lastSentMessage = sentMessages[sentMessages.length - 1];
                lastSentMessage.classList.add('fade-in');
            }
        } else {
            if (currentMessageGroup && currentMessageGroup.classList.contains('message-group-received')) {
                const messagesContainer = currentMessageGroup.lastChild;

                const messageReceivedContainer = document.createElement('div');
                messageReceivedContainer.classList.add('message-received', 'fade-in');

                const messageReceivedText = document.createElement('div');
                messageReceivedText.classList.add('message-received-text');
                messageReceivedText.textContent = message;

                messageReceivedContainer.appendChild(messageReceivedText);
                messagesContainer.appendChild(messageReceivedContainer);
            } else {
                currentMessageGroup = document.createElement('div');
                currentMessageGroup.classList.add('message-group-received');

                const imgContainer = document.createElement('div');
                const messagesContainer = document.createElement('div');

                const imgElement = document.createElement('img');
                imgElement.src = userIcon;
                imgElement.alt = '';

                imgContainer.appendChild(imgElement);

                const messageReceivedContainer = document.createElement('div');
                messageReceivedContainer.classList.add('message-received', 'fade-in');

                const messageReceivedText = document.createElement('div');
                messageReceivedText.classList.add('message-received-text');
                messageReceivedText.textContent = message;

                messageReceivedContainer.appendChild(messageReceivedText);
                messagesContainer.appendChild(messageReceivedContainer);

                currentMessageGroup.appendChild(imgContainer);
                currentMessageGroup.appendChild(messagesContainer);

                document.querySelector('#chat-messages > div').appendChild(currentMessageGroup);
            }
        }

        chatMessagesContainer.scrollTo({
            top: chatMessagesContainer.scrollHeight,
            behavior: 'smooth'
        });
    };

    chatSocket.onopen = function (event) {
        // console.log('open');
    };

    chatSocket.onclose = function (event) {
        // console.log('close');
    };

    document.querySelector('.send-button').onclick = function (event) {
        event.preventDefault();

        const messageInputDom = document.querySelector('.message-input');
        const message = messageInputDom.value;

        if (message.split('').some(s => s.match(/[a-zA-Zа-яА-Я]/))) {
            chatSocket.send(JSON.stringify({
                'chat_uuid': chatUUID,
                'email': email,
                'message': message,
            }));

            const lastChatMessage = document.querySelector(`#companion-info-${chatUUID} > p`);

            if (message.length > 30) {
                lastChatMessage.textContent = newLastChatMessage !== null ? newLastChatMessage : message.substring(0, 30) + '...';
            } else {
                lastChatMessage.textContent = newLastChatMessage !== null ? newLastChatMessage : message;
            }

            messageInputDom.value = '';
        }
    };

    // Поиск по чатам
    const searchInput = document.querySelector('.chat-search');
    searchInput.addEventListener('input', () => searchContact(searchInput.value));

    // Прокрутка окна сообщений вниз
    scrollDown(chatMessagesContainer)
}

const chats = document.querySelectorAll('.chat');
const companionNames = document.querySelectorAll('.companion-info > h3');

function searchContact(value) {
    chats.forEach((chat, index) => {
        chat.classList.add('d-none');
        const companionName = companionNames[index].textContent;
        const [firstName, lastName] = companionName.split(' ');

        if (
            firstName.toLowerCase().startsWith(value.toLowerCase()) ||
            lastName.toLowerCase().startsWith(value.toLowerCase())
        ) {
            chat.classList.remove('d-none');
        }
    });
}

function scrollDown(tag) {
    tag.scrollTop = tag.scrollHeight;
}

// Обработчик клика на элемент .chat
$('.chat').on('click', function () {
    const chatUUID = $(this).data('chat-uuid');

    $.ajax({
        url: `/chats/${chatUUID}/`,
        method: 'GET',
        success: function (response) {
            const parsedHTML = $.parseHTML(response);
            const chatContent = $(parsedHTML).find('#chat-content').html();
            $('#chat-content').html(chatContent);
            document.title = $(parsedHTML).find('title').text();

            const newURL = `/chats/${chatUUID}/`;
            history.pushState(null, null, newURL);

            const newLastChatMessage = $(parsedHTML).find(`#companion-info-${chatUUID} > p`)[1];

            // Переключить WebSocket-соединение на новый чат
            if (chatSocket !== null) {
                // Закрыть предыдущее WebSocket-соединение, если оно существует
                chatSocket.close();
            }

            initialize(chatUUID, newLastChatMessage);

            scrollDown(document.getElementById('chat-messages'));
        },
        error: function () {
        }
    });
});
