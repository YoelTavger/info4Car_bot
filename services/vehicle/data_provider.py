import requests
from config import GOVIL_API_URL, GOVIL_RESOURCE_ID

def get_vehicle_data(license_plate):
    """
    מחזיר מידע על רכב לפי מספר רישוי מהמאגר הראשי
    
    Args:
        license_plate: מספר הרכב לחיפוש
        
    Returns:
        רשימה של רשומות מידע או None אם לא נמצא
    """
    try:
        r = requests.get(GOVIL_API_URL, params={
            "resource_id": GOVIL_RESOURCE_ID,
            "q": license_plate,
            "limit": 1
        })
        records = r.json().get("result", {}).get("records", [])
        if records:
            # print(f"מידע ממאגר ראשי: {records}")
            return records
        return None
    except Exception as e:
        print(f"שגיאה בקבלת מידע על רכב (מאגר ראשי): {e}")
        return None