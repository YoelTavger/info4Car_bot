import os
import socket
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')

PLATE_RECOGNIZER_TOKEN = os.environ.get('PLATE_RECOGNIZER_TOKEN')
PLATE_RECOGNIZER_API_URL = os.environ.get('PLATE_RECOGNIZER_API_URL')
REGIONS = ["il"]

GOVIL_API_URL = os.getenv("GOVIL_API_URL")
GOVIL_RESOURCE_ID = os.getenv("GOVIL_RESOURCE_ID")
GOVIL_RESOURCE_ID_ALT = os.getenv("GOVIL_RESOURCE_ID_ALT")

def detect_environment():
    """
    זיהוי אוטומטי של סביבת ההרצה (מקומית או Render)
    
    הפונקציה בודקת מספר מאפיינים כדי להחליט אם הסביבה היא Render:
    1. בדיקת משתנה סביבה RENDER (אם הוגדר מפורשות)
    2. בדיקת משתנה סביבה RENDER_SERVICE_NAME (ייחודי ל-Render)
    3. בדיקת שם המחשב (hostname)
    
    Returns:
        bool: True אם הסביבה מזוהה כ-Render, אחרת False
    """
    # בדיקה אם המשתנה RENDER הוגדר מפורשות
    render_env = os.environ.get('RENDER', '').lower()
    if render_env in ['true', '1', 'yes']:
        return True
    if render_env in ['false', '0', 'no']:
        return False
        
    # בדיקה אם קיים משתנה סביבה ייחודי ל-Render
    if os.environ.get('RENDER_SERVICE_NAME'):
        return True
        
    # בדיקת שם המחשב (בדרך כלל מכיל "render" בסביבת Render)
    try:
        hostname = socket.gethostname()
        if 'render' in hostname.lower():
            return True
    except:
        pass
        
    # ברירת מחדל: להניח שזו סביבה מקומית
    return False

# בדיקה אם הסביבה היא Render
IS_RENDER = detect_environment()

# IS_RENDER = os.environ.get('RENDER')
PORT = int(os.environ.get('PORT'))
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')