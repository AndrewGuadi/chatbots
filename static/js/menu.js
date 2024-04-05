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

    function sendMessage(message, iterationCounter = 1) {
        if (message.trim() === '') return;

        appendMessage('User', message);
        userInput.value = '';
        userInput.focus();

        // Send message to Flask server
        fetch('/message', {
            method: 'POST',
            body: JSON.stringify({'message': message, 'iteration_counter': iterationCounter}),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            appendMessage('Bot', data.response);
            if (!data.done) {
                // Update iterationCounter for the next message
                iterationCounter += 1;
            }
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
