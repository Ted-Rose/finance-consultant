import os
import sys

path = '/home/FinanceConsultant/finance-consultant/django/'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'finance_consultant.settings'

# then:
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
