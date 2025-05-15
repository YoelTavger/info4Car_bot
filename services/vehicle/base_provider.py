import requests
from abc import ABC, abstractmethod

class VehicleDataProvider(ABC):
    """
    ממשק בסיסי לספקי נתוני רכב
    """
    def __init__(self, api_url, resource_id, name=None, id_field="mispar_rechev"):
        self.api_url = api_url
        self.resource_id = resource_id
        self.name = name or self.__class__.__name__
        self.id_field = id_field  # שם השדה שמכיל את מספר הרכב
    
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
            # חזרה לחיפוש באמצעות q כמו בקוד המקורי
            r = requests.get(
                self.api_url, 
                params={
                    "resource_id": self.resource_id,
                    "q": license_plate,
                    "limit": limit
                },
                timeout=5  # timeout של 5 שניות לכל בקשה
            )
            result = r.json()
            records = result.get("result", {}).get("records", [])
            
            if records:
                # סינון לפי שדה ID (אך ורק רשומות שמספר הרכב תואם בדיוק)
                filtered_records = []
                for record in records:
                    if record.get(self.id_field) == license_plate:
                        record['data_source'] = self.name
                        filtered_records.append(record)
                
                return filtered_records if filtered_records else None
            return None
        except requests.exceptions.Timeout:
            print(f"חריגת זמן בקבלת מידע מ{self.name}")
            return None
        except Exception as e:
            print(f"שגיאה בקבלת מידע מ{self.name}: {e}")
            return None