import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')

PLATE_RECOGNIZER_TOKEN = os.environ.get('PLATE_RECOGNIZER_TOKEN')
PLATE_RECOGNIZER_API_URL = os.environ.get('PLATE_RECOGNIZER_API_URL')
REGIONS = ["il"]

GOVIL_API_URL = os.getenv("GOVIL_API_URL")
GOVIL_RESOURCE_ID = os.getenv("GOVIL_RESOURCE_ID")
GOVIL_RESOURCE_ID_ALT = os.getenv("GOVIL_RESOURCE_ID_ALT")

# הגדרות לסביבת Render
IS_RENDER = os.getenv('RENDER', 'false').lower() == 'true'
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
PORT = int(os.getenv('PORT', 10000))