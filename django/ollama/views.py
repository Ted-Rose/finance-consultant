import requests
import json
from django.conf import settings
from django.shortcuts import render
from gtts import gTTS
import os

def index(request):
    url = 'http://localhost:11434/api/generate'
    category_list = '''
        {
            'good_borrower': {
                'Balance is more than 2 000 EUR'
            },
            'bad_borrower': {
                'Balance is less than 100 EUR'
            }
        }
    '''
    balance = '''
        {
            'accounts': [
                {
                    'balanceAmount': {
                        'amount': '99.00',
                        'currency': 'EUR'
                    },
                    'balanceType': 'interimBooked',
                    'referenceDate': '2022-10-10'
                },
                {
                    'balanceAmount': {
                        'amount': '12.00',
                        'currency': 'EUR'
                    },
                    'balanceType': 'interimAvailable',
                    'referenceDate': '2022-10-10'
                }
            ]
        }
    '''
    prompt = (
        "Your task as a creditor's assistant is to categorize a borrower's\
            application based on their bank balance report. Here is the \
            balance report:" + balance + " The categorization is based on \
            the following criteria:" + category_list + "Based on the balance \
            report provided, categorize the borrower using a single word from \
            the category list ('good_borrower' or 'bad_borrower')"
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

        # Append the new prompt and response to the data list
        data_list.append({'prompt': prompt, 'response': full_response})

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
            settings.MEDIA_URL + 'prompt_responses/prompt_response.mp3'

        return render(
            request,
            'ollama/home.html',
            {
                'prompt': prompt,
                'response': full_response,
                'audio_file_url': audio_file_url,
            }
        )
    else:
        error_message = f'Request failed with status code: \
            {response.status_code}'
        print(error_message)
        return render(
            request,
            'ollama/home.html',
            {
                'error_message': error_message
            }
        )