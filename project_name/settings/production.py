# Production settings for {{ project_name }}
from {{ project_name }}.settings import *

SITE_URL = 'http://{{ heroku_app }}.herokuapp.com'

# Basic authentication for Heroku
BASIC_WWW_AUTHENTICATION_USERNAME = ""
BASIC_WWW_AUTHENTICATION_PASSWORD = ""
BASIC_WWW_AUTHENTICATION = False
