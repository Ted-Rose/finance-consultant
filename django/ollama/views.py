from django.http import HttpResponse
import requests
import json

def index(request):
    url = 'http://localhost:11434/api/generate'
    category_list = """
        {
            "good_borrower": {
                "Balance is more than 2 000 EUR"
            },
            "bad_borrower": {
                "Balance is less than 100 EUR"
            }
        }
    """
    balance = """
        {
            "accounts": [
                {
                    "balanceAmount": {
                        "amount": "99.00",
                        "currency": "EUR"
                    },
                    "balanceType": "interimBooked",
                    "referenceDate": "2022-10-10"
                },
                {
                    "balanceAmount": {
                        "amount": "12.00",
                        "currency": "EUR"
                    },
                    "balanceType": "interimAvailable",
                    "referenceDate": "2022-10-10"
                }
            ]
        }
    """
    prompt = (
        "Your task as a creditor's assistant is to categorize a borrower's\
            application based on their bank balance report. Here is the \
            balance report:" + balance + " The categorization is based on \
            the following criteria:" + category_list + "Based on the balance \
            report provided, categorize the borrower using a single word from \
            the category list ('good_borrower' or 'bad_borrower')"
    )
    data = {
        "model": "llama2",
        "prompt": prompt
    }
    print("prompt:\n", prompt)
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