import requests
from abc import ABC, abstractmethod

class VehicleDataProvider(ABC):
    """
    ממשק בסיסי לספקי נתוני רכב
    """
    def __init__(self, api_url, resource_id, name=None):
        self.api_url = api_url
        self.resource_id = resource_id
        self.name = name or self.__class__.__name__
    
    @abstractmethod
    def get_vehicle_data(self, license_plate):
        """
        מחזיר מידע על רכב לפי מספר רישוי
        
        Args:
            license_plate: מספר הרכב לחיפוש
            
        Returns:
            רשומות מידע או None אם לא נמצא
        """
        pass
    
    def fetch_data(self, license_plate, limit=1):
        """
        מבצע בקשת API לקבלת נתוני רכב
        
        Args:
            license_plate: מספר רכב לחיפוש
            limit: מגבלת תוצאות
            
        Returns:
            רשומות מהמאגר או None אם נכשל
        """
        try:
            r = requests.get(self.api_url, params={
                "resource_id": self.resource_id,
                "q": license_plate,
                "limit": limit
            })
            result = r.json()
            records = result.get("result", {}).get("records", [])
            if records:
                # print(f"מידע מ{self.name}: {records}")
                return records
            return None
        except Exception as e:
            print(f"שגיאה בקבלת מידע מ{self.name}: {e}")
            return None