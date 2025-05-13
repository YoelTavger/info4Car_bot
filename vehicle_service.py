import requests
from config import GOVIL_API_URL, GOVIL_RESOURCE_ID, GOVIL_RESOURCE_ID_ALT

def get_vehicle(license_plate):
    """מחזיר מידע על רכב לפי מספר רישוי מהמאגר הראשי"""
    try:
        r = requests.get(GOVIL_API_URL, params={
            "resource_id": GOVIL_RESOURCE_ID,
            "q": license_plate,
            "limit": 1
        })
        records = r.json().get("result", {}).get("records", [])
        if records:
            # print(f"מידע ממאגר ראשי: {records}")
            return records if records else None
    except Exception as e:
        print(f"שגיאה בקבלת מידע על רכב (מאגר ראשי): {e}")
        return None

def get_vehicle_extended(license_plate):
    """מחזיר מידע נוסף על רכב לפי מספר רישוי מהמאגר המשני"""
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

def get_vehicle_complete(license_plate):
    """מחזיר מידע מאוחד מכל המאגרים על הרכב"""
    vehicle_data = get_vehicle(license_plate)
    if not vehicle_data:
        return None
        
    # ניסיון לקבל מידע נוסף מהמאגר השני
    extended_data = get_vehicle_extended(license_plate)
    
    # אם מצאנו מידע נוסף, נשלב אותו עם המידע הקיים
    if extended_data:
        # מעבר על כל שדה במידע הנוסף ושילובו בנתונים הקיימים
        for key, value in extended_data.items():
            # אם השדה לא קיים במידע הראשי או אם הוא ריק, נוסיף אותו
            if key not in vehicle_data[0] or not vehicle_data[0][key]:
                vehicle_data[0][key] = value
    
    # print(f"מידע מאוחד: {vehicle_data}")
    return vehicle_data