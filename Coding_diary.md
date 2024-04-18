3. https://www.pythonanywhere.com/user/FinanceConsultant/consoles/33404427/
    - `ssh-keygen -t rsa -b 4096 -C "your_email@example.com"`
        - Replace your_email@example.com with the email address associated with your GitHub account.
    - `eval "$(ssh-agent -s)" && ssh-add ~/.ssh/id_rsa`
    - `cat ~/.ssh/id_rsa.pub`
        - Go to your GitHub account settings, navigate to "SSH and GPG keys," and click "New SSH key."
        - Paste the contents of your public key into the "Key" field, give it a meaningful title, and click "Add SSH key."
    - `git clone git@github.com:Ted-Rose/finance-consultant.git`
    - `mkvirtualenv finance_consultant_venv --python=/usr/bin/python3.10`
    - `workon finance_consultant_venv`
    - `pip install -r requirements.txt`
    - https://www.pythonanywhere.com/user/FinanceConsultant/webapps/
        - !!! Choose `» Manual configuration (including virtualenvs)`
        - `Source code:` = `/home/FinanceConsultant/finance-consultant`
        - In `/var/www/financeconsultant_pythonanywhere_com_wsgi.py` paste contents of this projects file `financeconsultant_pythonanywhere_com_wsgi.py`
        `python manage.py collectstatic`
2. `pip install gTTS`
    - "gTTS" is a Python library for text-to-speech conversion
1. `docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama`
  - Containerized Ollama and exposed it at http://localhost:11434/
