import { getCookie } from './get_cookie.js';

function fetchLocalRequest() {
    const apiUrl = 'https://127.0.0.1:8000/ollama/local';
    const userInput = document.getElementById('userInput').value;
    const controller = new AbortController();
    const signal = controller.signal;
    const timeoutId = setTimeout(() => controller.abort(), 180000);

    // Update the prompt with the user's question
    document.getElementById('prompt').textContent = userInput;

    // Assuming the server expects the user input in a field named 'question'
    const requestData = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ question: userInput }),
        signal: signal,
        // Include cookies with the request
        credentials: 'include'
    };

    fetch(apiUrl, requestData)
        .then(response => {
            // Clear the timeout if the response is received
            clearTimeout(timeoutId);
            if (!response.ok) {
                throw new Error(`Request failed with status ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // Update the DOM with the response data
            document.getElementById('response').textContent = data.response;
            // If you have an audio file URL in the response, update the audio source
            if (data.audio_file_url) {
                var audioPlayer = document.getElementById('audioPlayer');
                audioPlayer.src = data.audio_file_url;
                audioPlayer.load();
                audioPlayer.play();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('error').textContent = 'Error fetching response.';
        });
}

// Call fetchLocalRequest when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Attach the event listener to the button
    document.querySelector('button').addEventListener('click', fetchLocalRequest);
});