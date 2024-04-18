document.addEventListener('DOMContentLoaded', function () {
    const apiUrl = 'http://127.0.0.1:8000/ollama/local';


    fetch(apiUrl, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Request failed with status ${response.status}`);
            }
            return response.json();
        })
        .then(jsonResponse => {
            console.log(jsonResponse);
        })
        .catch(error => {
            console.error('Error:', error);
        });
});