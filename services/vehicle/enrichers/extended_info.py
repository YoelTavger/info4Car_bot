import requests
from config import GOVIL_API_URL, RESOURCE_ID_EXTENDED_INFO

class ExtendedInfoEnricher:
    """
    מעשיר נתוני רכב עם מידע נוסף ממאגר המידע הנוסף
    """
    
    def __init__(self):
        self.api_url = GOVIL_API_URL
        self.resource_id = RESOURCE_ID_EXTENDED_INFO
    
    def enrich(self, vehicle_data, license_plate):
        """
        מעשיר נתוני רכב עם מידע נוסף
        
        Args:
            vehicle_data: נתוני הרכב הקיימים
            license_plate: מספר הרכב
            
        Returns:
            נתוני רכב מועשרים
        """
        try:
            # בדיקה אם יש מידע קיים
            if not vehicle_data:
                return vehicle_data
                
            # ניסיון לקבל מידע נוסף
            r = requests.get(self.api_url, params={
                "resource_id": self.resource_id,
                "q": license_plate,
                "limit": 1
            })
            result = r.json()
            extended_data = result.get("result", {}).get("records", [])
            
            # אם מצאנו מידע נוסף
            if extended_data and len(extended_data) > 0:
                # מיזוג המידע החדש לנתונים הקיימים
                for key, value in extended_data[0].items():
                    # אם השדה לא קיים במידע הראשי או אם הוא ריק
                    if key not in vehicle_data[0] or not vehicle_data[0][key]:
                        vehicle_data[0][key] = value
            
            return vehicle_data
        except Exception as e:
            print(f"שגיאה בהעשרת מידע נוסף: {e}")
            return vehicle_data