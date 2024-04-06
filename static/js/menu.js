document.addEventListener('DOMContentLoaded', function() {
    const sendButton = document.getElementById('send-btn');
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');

    sendButton.addEventListener('click', function() {
        const message = userInput.value;
        sendMessage(message);
    });

    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            const message = userInput.value;
            sendMessage(message);
            e.preventDefault();  // Prevents the default enter key behavior
        }
    });

    function sendMessage(message) {
        if (message.trim() === '') return;

        appendMessage('User', message);
        
        userInput.value = '';
        userInput.focus();

        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        // Send message to Flask server
        fetch('/message', {
            method: 'POST',
            body: JSON.stringify({'message': message}),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken  // Include the CSRF token in the request header
            }
        })
        .then(response => response.json())
        .then(data => {
            appendMessage('Bot', data.response);
                    })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    function appendMessage(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add(sender === 'User' ? 'user-message' : 'bot-message');
        messageElement.textContent = message;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the latest message
    }
});
