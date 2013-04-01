# Production settings for {{ project_name }}
from {{ project_name }}.settings import *

# Make this unique, and don't share it with anybody.
SECRET_KEY = '{{ secret_key }}'

SITE_URL = 'http://{{ heroku_app }}.herokuapp.com'

# Basic authentication for Heroku
BASIC_WWW_AUTHENTICATION_USERNAME = ""
BASIC_WWW_AUTHENTICATION_PASSWORD = ""
BASIC_WWW_AUTHENTICATION = False
