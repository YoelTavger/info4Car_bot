import requests
from config import PLATE_RECOGNIZER_TOKEN, PLATE_RECOGNIZER_API_URL, REGIONS

def recognize_license_plate(image_file):
    """
    זיהוי לוחית רישוי מתמונה באמצעות PlateRecognizer API
    
    Args:
        image_file: קובץ התמונה (בינארי)
        
    Returns:
        dict: תוצאות הזיהוי או None אם נכשל
    """
    try:
        # שליחת התמונה ל-API
        response = requests.post(
            PLATE_RECOGNIZER_API_URL,
            data=dict(regions=REGIONS),
            files=dict(upload=image_file),
            headers={'Authorization': f'Token {PLATE_RECOGNIZER_TOKEN}'},
            timeout=30  # הגדרת timeout למניעת תקיעות
        )
        
        # בדיקת תקינות התגובה
        if response.status_code == 200 or response.status_code == 201:  # תגובה תקינה
            result = response.json()
            # print(f"תוצאת זיהוי לוחית: {result}")
            return result
        else:
            print(f"שגיאה בזיהוי לוחית: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.Timeout:
        print("פסק הזמן לזיהוי לוחית הסתיים")
        return None
    except requests.exceptions.ConnectionError:
        print("שגיאת חיבור בזיהוי לוחית")
        return None
    except Exception as e:
        print(f"שגיאה בזיהוי לוחית: {e}")
        return None