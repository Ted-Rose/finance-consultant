from django.http import HttpResponse
import requests
import json

def index(request):
    url = 'http://localhost:11434/api/generate'
    data = {
        "model": "llama2",
        "prompt": "Why is the sky blue?"
    }
    response = requests.post(url, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        full_response = ''

        # The response from the API comes in chunks, thus iterate the lines
        for line in response.iter_lines():
            if line:
                json_response = json.loads(line)
                full_response += json_response.get('response', '')

                # If the 'done' key is True the response is complete
                if json_response.get('done', False):
                    break

        print(full_response)
        return HttpResponse(full_response)
    else:
        error_message = f"Request failed with status code: {response.status_code}"
        print(error_message)
        return HttpResponse(error_message)