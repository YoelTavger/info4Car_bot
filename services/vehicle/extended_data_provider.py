import requests
from config import GOVIL_API_URL, GOVIL_RESOURCE_ID_ALT

def get_vehicle_extended_data(license_plate):
    """
    מחזיר מידע נוסף על רכב לפי מספר רישוי מהמאגר המשני
    
    Args:
        license_plate: מספר הרכב לחיפוש
        
    Returns:
        מילון עם מידע נוסף או None אם לא נמצא
    """
    try:
        r = requests.get(GOVIL_API_URL, params={
            "resource_id": GOVIL_RESOURCE_ID_ALT,
            "q": license_plate,
            "limit": 1
        })
        result = r.json()
        records = result.get("result", {}).get("records", [])
        if records:
            # print(f"מידע ממאגר משני: {records}")
            return records[0]
        return None
    except Exception as e:
        print(f"שגיאה בקבלת מידע נוסף על רכב (מאגר משני): {e}")
        return None