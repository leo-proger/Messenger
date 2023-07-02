const chatUuid = JSON.parse(document.getElementById('json-chat_uuid').textContent);

const chatSocket = new WebSocket(`ws://${window.location.host}/ws/chats/${chatUuid}/`);

const email = JSON.parse(document.getElementById('json-email').textContent);
const userIcon = JSON.parse(document.getElementById('json-user_icon').textContent);
// const userId = JSON.parse(document.getElementById('json-user_id').textContent);

const chatMessages = document.querySelector('.chat-messages');
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
            document.querySelector('.discussion').appendChild(currentMessageGroup);
        }

        messageSentContainer.appendChild(messageSentText);
        currentMessageGroup.appendChild(messageSentContainer);

        // Применить анимацию только к последнему сообщению текущего пользователя
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
            const messagesContainer = document.createElement('div')

            const imgElement = document.createElement('img');
            imgElement.src = userIcon
            imgElement.alt = ''

            imgContainer.appendChild(imgElement)

            const messageReceivedContainer = document.createElement('div');
            messageReceivedContainer.classList.add('message-received', 'fade-in');

            const messageReceivedText = document.createElement('div');
            messageReceivedText.classList.add('message-received-text');
            messageReceivedText.textContent = message;

            messageReceivedContainer.appendChild(messageReceivedText);
            messagesContainer.appendChild(messageReceivedContainer);

            currentMessageGroup.appendChild(imgContainer);
            currentMessageGroup.appendChild(messagesContainer);

            document.querySelector('.discussion').appendChild(currentMessageGroup);
        }
    }


    const windowElement = document.querySelector('.chat-window')
    windowElement.scrollTo({
        top: chatMessages.scrollHeight,
        behavior: 'smooth'
    });
};

chatSocket.onopen = function (event) {
    console.log('open')
}

chatSocket.onclose = function (event) {
    console.log('close');
};

document.querySelector('.send-button').onclick = function (event) {
    event.preventDefault(); // Отменить стандартное поведение кнопки

    const messageInputDom = document.querySelector('.message-input');
    const message = messageInputDom.value;

    if (message) {
        chatSocket.send(JSON.stringify({
            'chat_uuid': chatUuid,
            'email': email,
            'message': message,
        }));
        messageInputDom.value = '';
    }
};

document.querySelector('.message-input').addEventListener('keydown', function (event) {
    if (event.keyCode === 13 && !event.shiftKey) {
        event.preventDefault(); // Отменить стандартное поведение клавиши Enter

        const messageInputDom = document.querySelector('.message-input');
        let message = messageInputDom.value;
        console.log(message)

        if (message) {
            chatSocket.send(JSON.stringify({
                'chat_uuid': chatUuid,
                'email': email,
                'message': message,
            }));
            messageInputDom.value = '';
            messageInputDom.style.height = '47.5px';
        }
    } else if (event.keyCode === 13 && event.shiftKey) {
        event.preventDefault();

        let messageInputDom = document.querySelector('.message-input');
        messageInputDom.insertAdjacentHTML('beforeend', '<br>');
    }
});


window.addEventListener('load', () => {
    const chatWindow = document.querySelector('.chat-window');
    chatWindow.scrollTop = chatMessages.scrollHeight;
});

const textarea = document.querySelector('.message-input');
textarea.addEventListener('input', autoResize, false);

function autoResize() {
    if (this.style.height > 100) {
        this.style.overflowY = 'visible';
    } else {
        this.style.height = '48px';
        this.style.height = this.scrollHeight + 'px';
    }
}


