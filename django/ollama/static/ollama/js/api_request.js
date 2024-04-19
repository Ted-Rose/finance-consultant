export function fetchLocalRequest() {
    const apiUrl = 'https://127.0.0.1:8000/ollama/local';
    const userInput = document.getElementById('userInput').value;
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 180000);

    // Update the prompt with the user's question
    document.getElementById('prompt').textContent = userInput;

    const requestData = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: userInput }),
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

document.addEventListener('DOMContentLoaded', function () {
    const submitButton = document.querySelector('button');
    submitButton.addEventListener('click', function () {
        fetchLocalRequest();
    });
});