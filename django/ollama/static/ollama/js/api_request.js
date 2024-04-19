function fetchLocalRequest() {
    const apiUrl = 'http://127.0.0.1:8000/ollama/local';
    const controller = new AbortController();
    const signal = controller.signal;
    const timeoutId = setTimeout(() => controller.abort(), 180000);

    fetch(apiUrl, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
        signal: signal
    })
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

// Call the function when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function () {
    fetchLocalRequest();
});