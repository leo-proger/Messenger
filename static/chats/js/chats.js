let chatSocket = null;

const initialize = function (newChatUUID = null, newEmail = null, newLastChatMessage = null, newCompanionPhoto = null) {

    const chatUUID = newChatUUID !== null ? newChatUUID : JSON.parse(document.getElementById('json-chat_uuid').textContent);

    chatSocket = new WebSocket(`ws://${window.location.host}/ws/chats/${chatUUID}/`);

    const email = newEmail !== null ? newEmail : JSON.parse(document.getElementById('json-email').textContent);
    const companionPhoto = newCompanionPhoto !== null ? newCompanionPhoto : JSON.parse(document.getElementById('json-companion_photo').textContent);

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
                imgElement.src = companionPhoto;
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

        const lastChatMessage = document.querySelector(`#companion-info-${chatUUID} > p`);
        if (message.length > 30) {
            lastChatMessage.textContent = newLastChatMessage !== null ? newLastChatMessage : message.substring(0, 30) + '...';
        } else {
            lastChatMessage.textContent = newLastChatMessage !== null ? newLastChatMessage : message;
        }

        const timeLastChatMessage = document.querySelector('.time-last-message');
        timeLastChatMessage.textContent = getTimeNow();
    };

    chatSocket.onopen = function (event) {
        // console.log('open');
    };

    chatSocket.onclose = function (event) {
        // console.log('close');
    };

    // Отправка сообщения по нажатию на кнопку
    document.querySelector('.send-button').onclick = function (event) {
        event.preventDefault();

        const messageInputDom = document.querySelector('.message-input');
        const message = messageInputDom.value;

        if (message.trim() !== '') {
            chatSocket.send(JSON.stringify({
                'chat_uuid': chatUUID,
                'email': email,
                'message': message,
            }));

            messageInputDom.value = '';
        }
    };

    // Отправка сообщения по нажатию на Enter
    document.querySelector('.message-input').addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault();

            const messageInputDom = document.querySelector('.message-input');
            const message = messageInputDom.value;

            if (message.trim() !== '') {
                chatSocket.send(JSON.stringify({
                    'chat_uuid': chatUUID,
                    'email': email,
                    'message': message,
                }));

                messageInputDom.value = '';
            }
        }
    });


    // Прокрутка окна сообщений вниз
    scrollDown(chatMessagesContainer)
}

// Поиск по чатам
const searchInput = document.querySelector('.chat-search');
searchInput.addEventListener('input', () => searchContact(searchInput.value));

const chats = document.querySelectorAll('.chat');

function searchContact(value) {
    const noResultsMessage = document.getElementById('no-results-message');
    let hasResults = false;

    chats.forEach((chat) => {
        const companionName = chat.querySelector('.companion-info h3').textContent;
        const isMatch = companionName.toLowerCase().includes(value.toLowerCase());

        chat.classList.toggle('d-none', !isMatch);

        if (isMatch) {
            hasResults = true;
        }
    });

    noResultsMessage.classList.toggle('d-none', hasResults);
}


function scrollDown(tag) {
    tag.scrollTop = tag.scrollHeight;
}


function getTimeNow() {
    const currentDate = new Date();
    let hours = currentDate.getHours();
    let minutes = currentDate.getMinutes();

    // При необходимости отформатируйте часы и минуты с ведущими нулями
    if (hours < 10) {
        hours = "0" + hours;
    }
    if (minutes < 10) {
        minutes = "0" + minutes;
    }

    return hours + ":" + minutes;
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

            if (chatSocket !== null) {
                // Закрыть предыдущее WebSocket-соединение, если оно существует
                chatSocket.close();
            }

            const newEmail = JSON.parse($(response).filter('#json-email').text());
            const newLastChatMessage = $(parsedHTML).find(`#companion-info-${chatUUID} > p`)[1];
            const newCompanionPhoto = JSON.parse($(response).filter('#json-companion_photo').text());

            initialize(chatUUID, newEmail, newLastChatMessage, newCompanionPhoto);

            scrollDown(document.getElementById('chat-messages'));
            markMessagesAsRead(chatUUID);

            const chatUUIDJSONElement = document.getElementById('json-chat_uuid')
            chatUUIDJSONElement.textContent = JSON.stringify(chatUUID);
        },
        error: function () {
        }
    });
});

