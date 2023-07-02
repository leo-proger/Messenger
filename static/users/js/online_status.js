const user_email = JSON.parse(document.getElementById('json-email').textContent);

const socket = new WebSocket(`ws://${window.location.host}/ws/online/`);

socket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    if (data.user !== user_email) {
        const online_status = data.online_status;
        const onlineStatusElement = document.querySelector('.online-status');
        onlineStatusElement.textContent = online_status ? 'Online' : 'Offline';
    }
}

socket.onopen = function (event) {
    console.log('Connect to Online')
    socket.send(JSON.stringify({
        'online_status': true,
        'user': user_email,
    }))
}

socket.onclose = function (event) {
    console.log('Disconnect from Online')
}

window.addEventListener('beforeunload', function (event) {
    socket.send(JSON.stringify({
        'online_status': false,
        'user': user_email
    }))
})
