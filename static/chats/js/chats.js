let chatSocket = null;

const initialize = function (newChatUUID = null, newEmail = null, newLastChatMessage = null, newRecipientImage = null) {
    const chatUUID = newChatUUID || JSON.parse(document.getElementById('json-chat_uuid').textContent);
    chatSocket = new WebSocket(`ws://${window.location.host}/ws/chats/${chatUUID}/`);

    const email = newEmail || JSON.parse(document.getElementById('json-email').textContent);
    const recipientImage = newRecipientImage || JSON.parse(document.getElementById('json-recipient_image').textContent);

    const chatMessagesContainer = document.getElementById('chat-messages');
    let currentMessageGroup = null;

    chatSocket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        const {message, sender} = data;

        if (sender === email) {
            const messageSentContainer = createMessageSentContainer(message);
            if (!currentMessageGroup || currentMessageGroup.classList.contains('message-group-received')) {
                currentMessageGroup = createMessageGroupSent();
                document.querySelector('#chat-messages > div').appendChild(currentMessageGroup);
            }

            currentMessageGroup.appendChild(messageSentContainer);
            fadeInLastSentMessage(currentMessageGroup);
        } else {
            if (currentMessageGroup && currentMessageGroup.classList.contains('message-group-received')) {
                const messagesContainer = currentMessageGroup.lastChild;
                const messageReceivedContainer = createMessageReceivedContainer(message);
                messagesContainer.appendChild(messageReceivedContainer);
            } else {
                currentMessageGroup = createMessageGroupReceived(recipientImage, message);
                document.querySelector('#chat-messages > div').appendChild(currentMessageGroup);
            }
        }

        scrollDown(chatMessagesContainer);
        updateLastChatMessage(chatUUID, newLastChatMessage || message);
        updateTimeLastChatMessage();

        prependChat(chatUUID);
    };

    chatSocket.onopen = function (event) {
        // console.log('open');
    };

    chatSocket.onclose = function (event) {
        // console.log('close');
    };

    // Отправка сообщения по нажатию на кнопку
    document.querySelector('.send-button').onclick = function (event) {
        sendMessage(event, chatUUID);
        prependChat(chatUUID);
    };

    // Отправка сообщения по нажатию на Enter
    document.querySelector('.message-input').addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            sendMessage(event, chatUUID);
            prependChat(chatUUID);
        }
    });

    // Прокрутка окна сообщений вниз
    scrollDown(chatMessagesContainer);
};

function createMessageSentContainer(message) {
    const messageSentContainer = document.createElement('div');
    messageSentContainer.classList.add('message-sent');

    const messageSentText = document.createElement('div');
    messageSentText.classList.add('message-sent-text');
    messageSentText.textContent = message;

    messageSentContainer.appendChild(messageSentText);

    return messageSentContainer;
}

function createMessageGroupSent() {
    const messageGroupSent = document.createElement('div');
    messageGroupSent.classList.add('message-group-sent');

    return messageGroupSent;
}

function createMessageReceivedContainer(message) {
    const messageReceivedContainer = document.createElement('div');
    messageReceivedContainer.classList.add('message-received', 'fade-in');

    const messageReceivedText = document.createElement('div');
    messageReceivedText.classList.add('message-received-text');
    messageReceivedText.textContent = message;

    messageReceivedContainer.appendChild(messageReceivedText);

    return messageReceivedContainer;
}

function createMessageGroupReceived(recipientImage, message) {
    const messageGroupReceived = document.createElement('div');
    messageGroupReceived.classList.add('message-group-received');

    const imgContainer = document.createElement('div');
    const messagesContainer = document.createElement('div');

    const imgElement = document.createElement('img');
    imgElement.src = recipientImage;
    imgElement.alt = '';

    imgContainer.appendChild(imgElement);

    const messageReceivedContainer = createMessageReceivedContainer(message);
    messagesContainer.appendChild(messageReceivedContainer);

    messageGroupReceived.appendChild(imgContainer);
    messageGroupReceived.appendChild(messagesContainer);

    return messageGroupReceived;
}

function fadeInLastSentMessage(currentMessageGroup) {
    const sentMessages = currentMessageGroup.getElementsByClassName('message-sent');
    if (sentMessages.length > 1) {
        const lastSentMessage = sentMessages[sentMessages.length - 1];
        lastSentMessage.classList.add('fade-in');
    }
}

function updateLastChatMessage(chatUUID, message) {
    const lastChatMessage = document.querySelector(`#recipient-info-${chatUUID} > p`);
    lastChatMessage.textContent = message;
}

function updateTimeLastChatMessage() {
    const timeLastChatMessage = document.querySelector('.time-last-message');
    timeLastChatMessage.textContent = getTimeNow();
}

function sendMessage(event, chatUUID) {
    event.preventDefault();

    const messageInputDom = document.querySelector('.message-input');
    const message = messageInputDom.value;

    if (message.trim() !== '') {
        chatSocket.send(JSON.stringify({
            'chat_uuid': chatUUID,
            'message': message,
        }));
        messageInputDom.value = '';
    }
}

function prependChat(chatUUID) {
    const chatBox = document.getElementById('chat-box');
    const chat = document.getElementById(chatUUID);
    chatBox.insertAdjacentElement('afterbegin', chat);
}


// Поиск по чатам
const searchInput = document.querySelector('.chat-search');
searchInput.addEventListener('input', () => searchContact(searchInput.value));

const chats = document.querySelectorAll('.chat');

function searchContact(value) {
    const noResultsMessage = document.getElementById('no-results-message');
    let hasResults = false;

    chats.forEach((chat) => {
        const recipientName = chat.querySelector('.recipient-info h3').textContent;
        const isMatch = recipientName.toLowerCase().includes(value.toLowerCase());

        chat.classList.toggle('d-none', !isMatch);

        if (isMatch) {
            hasResults = true;
        }
    });

    noResultsMessage.classList.toggle('d-none', hasResults);
}

function scrollDown(tag) {
    tag.scrollTo({
        top: tag.scrollHeight,
        behavior: 'smooth'
    });
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
            const newLastChatMessage = $(parsedHTML).find(`#recipient-info-${chatUUID} > p`)[1];
            const newRecipientImage = JSON.parse($(response).filter('#json-recipient_image').text());

            initialize(chatUUID, newEmail, newLastChatMessage, newRecipientImage);

            scrollDown(document.getElementById('chat-messages'));
            markMessagesAsRead(chatUUID);

            const chatUUIDJSONElement = document.getElementById('json-chat_uuid');
            if (chatUUIDJSONElement !== null) {
                chatUUIDJSONElement.textContent = JSON.stringify(chatUUID);
            }

            const chatList = document.getElementById('chat-list');
            chatList.className = 'd-none d-md-block col-md-5';

            $('#chat-content').removeClass().addClass('d-block col bg-black');
        },
        error: function () {
        }
    });
});
