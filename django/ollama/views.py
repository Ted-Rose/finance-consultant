import requests
import json
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from gtts import gTTS
import os
from .utils import voice_input

@csrf_exempt
def transcribe(request):
    print("in here")
    if request.method == 'POST':
        # Call the voice_input function
        transcription = voice_input()
        return JsonResponse({'transcription': transcription})
    else:
        return JsonResponse({'error': 'This endpoint only supports POST requests.'})

def production_request(request):
    # This view is called when the site is deployed online. It will make
    # an API request to locally hosted version of this project
    # triggering view local_request and returning the response from
    # locally hosted ollama app thus making a quick fix for ollama's
    # resistance of accepting requests from the internet.
    return render(
        request,
        'ollama/local_request.html',
    )
# Don't do csrf_token check as the local django didn't render the form
# to the client
@csrf_exempt
def local_request(request):
    url = 'http://localhost:11434/api/generate'
    question = json.loads(request.body).get('question', '')
    transactions = '''
            {
                "transactionId": "9492293",
                "bookingDate": "2024-04-01",
                "transactionAmount": {
                    "amount": "438.0",
                    "currency": "ISK"
                },
                "creditorName": "John Smith",
                "remittanceInformation": "Big toy car"
            },
            {
                "transactionId": "9492288",
                "bookingDate": "2021-09-25",
                "transactionAmount": {
                    "amount": "-121.19",
                    "currency": "ISK"
                },
                "creditorName": "Bob Doe",
                "remittanceInformation": "McDonnald's"
            },
            {
                "transactionId": "9492294",
                "bookingDate": "2024-03-31",
                "transactionAmount": {
                    "amount": "-9.0",
                    "currency": "ISK"
                },
                "creditorName": "Jake Jones",
                "remittanceInformation": "Car repair"
            }
    '''
    prompt = (
        "Your a finance consultant. Please tell me " + question + "? Based on \
        this list of transactions: " + transactions
    )
    data = {
        'model': 'llama2',
        'prompt': prompt
    }
    print('prompt:\n', prompt)
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

        # Read the existing data from the file, or create a new list if the file doesn't exist
        try:
            with open('ollama_prompts.json', 'r') as json_file:
                data_list = json.load(json_file)
        except FileNotFoundError:
            data_list = []

        data_list.append({'response': full_response})

        # Save the updated data list to the JSON file
        with open('ollama_prompts.json', 'w') as json_file:
            json.dump(data_list, json_file, indent=4)

        text_to_audio = gTTS(text=full_response, lang='en', slow=False)
        audio_file_path = os.path.join(
            settings.MEDIA_ROOT,
            'prompt_responses/prompt_response.mp3'
        )
        text_to_audio.save(audio_file_path)
        audio_file_url = \
            'https://127.0.0.1:8000/media/' + 'prompt_responses/prompt_response.mp3'

        return JsonResponse({
            'response': full_response,
            'audio_file_url': audio_file_url,
        })
        # return render(
        #     request,
        #     'ollama/home.html',
        #     {
        #         'prompt': prompt,
        #         'response': full_response,
        #         'audio_file_url': audio_file_url,
        #     }
        # )
    else:
        error_message = f'Request failed with status code: {response.status_code}'
        # Return the error message in a JSON response
        return JsonResponse({'error_message': error_message}, status=response.status_code)
        # error_message = f'Request failed with status code: \
        #     {response.status_code}'
        # print(error_message)
        # return render(
        #     request,
        #     'ollama/home.html',
        #     {
        #         'error_message': error_message
        #     }
        # )
