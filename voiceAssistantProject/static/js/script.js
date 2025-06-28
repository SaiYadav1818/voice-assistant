document.addEventListener('DOMContentLoaded', () => {
    const startBtn = document.getElementById('start-btn');
    const statusText = document.getElementById('status');
    const responseText = document.getElementById('response');

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();

    recognition.lang = 'en-US';  // Set the language to English

    recognition.onstart = function() {
        statusText.textContent = 'Listening...';
    };

    recognition.onspeechend = function() {
        recognition.stop();
        statusText.textContent = 'Stopped listening, processing...';
    };

    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript.toLowerCase();
        statusText.textContent = `You said: ${transcript}`;
        responseText.classList.remove('error');  // Remove error class if it exists
        handleCommand(transcript);
    };

    recognition.onerror = function(event) {
        if (event.error === 'no-speech') {
            statusText.textContent = 'No speech was detected. Please try again.';
            responseText.textContent = '';
        } else {
            statusText.textContent = `Error: ${event.error}`;
            responseText.textContent = 'Doesn\'t recognize';
        }
        responseText.classList.add('error');      
    };

    startBtn.addEventListener('click', () => {
        responseText.textContent = '';
        responseText.classList.remove('error');
        recognition.start();
    });

    function speak(text) {
        const speech = new SpeechSynthesisUtterance(text);
        window.speechSynthesis.speak(speech);
    }

    function handleCommand(command) {
        fetch('/command', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ command: command })
        })
        .then(response => response.json())
        .then(data => {
            const response = data.response;
            responseText.textContent = response;
            speak(response);
        })
        .catch(error => {
            responseText.textContent = 'An error occurred. Please try again.';
            responseText.classList.add('error');
        });
    }
});