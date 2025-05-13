import os
from dotenv import load_dotenv

load_dotenv()

# API Tokens
API_TOKEN = os.getenv('API_TOKEN')

# OCR Service
PLATE_RECOGNIZER_TOKEN = os.environ.get('PLATE_RECOGNIZER_TOKEN')
PLATE_RECOGNIZER_API_URL = os.environ.get('PLATE_RECOGNIZER_API_URL')
REGIONS = ["il"]

# Gov.il API
GOVIL_API_URL = os.getenv("GOVIL_API_URL")

# מאגרים ראשיים - רכבים שונים
RESOURCE_ID_PRIVATE_VEHICLES = os.getenv("RESOURCE_ID_PRIVATE_VEHICLES", "053cea08-09bc-40ec-8f7a-156f0677aff3")  # רכב פרטי ומסחרי
RESOURCE_ID_HEAVY_VEHICLES = os.getenv("RESOURCE_ID_HEAVY_VEHICLES", "cd3acc5c-03c3-4c89-9c54-d40f93c0d790")  # רכב מעל 3.5 טון
RESOURCE_ID_MOTORCYCLES = os.getenv("RESOURCE_ID_MOTORCYCLES", "bf9df4e2-d90d-4c0a-a400-19e15af8e95f")  # דו גלגלי
RESOURCE_ID_INACTIVE_VEHICLES = os.getenv("RESOURCE_ID_INACTIVE_VEHICLES", "f6efe89a-fb3d-43a4-bb61-9bf12a9b9099")  # לא פעיל
RESOURCE_ID_INACTIVE_HEAVY = os.getenv("RESOURCE_ID_INACTIVE_HEAVY", "6f6acd03-f351-4a8f-8ecf-df792f4f573a")  # לא פעיל, ללא קוד דגם
RESOURCE_ID_FINAL_CANCELED = os.getenv("RESOURCE_ID_FINAL_CANCELED", "851ecab1-0622-4dbe-a6c7-f950cf82abf9")  # ירד מהכביש
RESOURCE_ID_PERSONAL_IMPORT = os.getenv("RESOURCE_ID_PERSONAL_IMPORT", "03adc637-b6fe-402b-9937-7c3d3afc9140")  # יבוא אישי

# מאגרי העשרת נתונים
RESOURCE_ID_EXTENDED_INFO = os.getenv("RESOURCE_ID_EXTENDED_INFO", "0866573c-40cd-4ca8-91d2-9dd2d7a492e5")  # מידע נוסף
RESOURCE_ID_VEHICLE_HISTORY = os.getenv("RESOURCE_ID_VEHICLE_HISTORY", "56063a99-8a3e-4ff4-912e-5966c0279bad")  # היסטוריה
RESOURCE_ID_DISABILITY_TAG = os.getenv("RESOURCE_ID_DISABILITY_TAG", "c8b9f9c8-4612-4068-934f-d4acd2e3c06e")  # תו נכה
RESOURCE_ID_SAFETY_SYSTEMS = os.getenv("RESOURCE_ID_SAFETY_SYSTEMS", "83bfb278-7be1-4dab-ae2d-40125a923da1")  # מערכות בטיחות

# הגדרות לסביבת Render
IS_RENDER = os.getenv('RENDER', 'false').lower() == 'true'
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
PORT = int(os.getenv('PORT', 10000))