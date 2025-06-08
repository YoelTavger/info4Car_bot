from services.vehicle.base_provider import VehicleDataProvider
from config import GOVIL_API_URL

class ManufacturerProvider(VehicleDataProvider):
    """
    ספק נתונים עבור מידע תוצרים של כלי רכב
    """
    def __init__(self):
        # המאגר החדש שציינת
        resource_id = "d00812f4-58c5-4ce8-b16c-ac13ae52f9d8"
        super().__init__(
            api_url=GOVIL_API_URL,
            resource_id=resource_id,
            name="מאגר תוצרים",
            id_field="tozeret_cd"  # השדה שמכיל את קוד התוצר
        )
    
    def get_vehicle_data(self, license_plate):
        """
        מימוש חובה של המתודה המופשטת - אך כאן לא נשתמש בה
        כי אנחנו מחפשים לפי קוד תוצר ולא מספר רכב
        """
        return None
    
    def get_manufacturer_data(self, manufacturer_code):
        """
        מחזיר מידע על תוצר לפי קוד תוצר
        
        Args:
            manufacturer_code: קוד התוצר לחיפוש
            
        Returns:
            מידע על התוצר או None אם לא נמצא
        """
        if not manufacturer_code:
            return None
            
        return self.fetch_data(manufacturer_code, limit=5)
    
    def enrich_vehicle_with_manufacturer_data(self, vehicle_data):
        """
        מעשיר נתוני רכב עם מידע תוצר מפורט
        
        Args:
            vehicle_data: נתוני הרכב המקוריים
            
        Returns:
            נתוני הרכב מעושרים עם מידע התוצר
        """
        if not vehicle_data:
            return vehicle_data
            
        manufacturer_code = vehicle_data.get('tozeret_cd')
        if not manufacturer_code:
            return vehicle_data
        
        # חיפוש מידע התוצר
        manufacturer_info = self.get_manufacturer_data(manufacturer_code)
        
        if manufacturer_info and len(manufacturer_info) > 0:
            manufacturer_record = manufacturer_info[0]
            
            # הוספת המידע המעושר לנתוני הרכב
            vehicle_data['manufacturer_info'] = {
                'tozeret_cd': manufacturer_record.get('tozeret_cd'),
                'tozeret_nm': manufacturer_record.get('tozeret_nm'),
                'tozar': manufacturer_record.get('tozar'),  # המותג
                'tozeret_eretz_nm': manufacturer_record.get('tozeret_eretz_nm'),  # מדינת התוצר
                'data_source': 'מאגר תוצרים'
            }
            
            # עדכון השדות הבסיסיים עם המידע המפורט יותר
            if manufacturer_record.get('tozar'):
                vehicle_data['brand'] = manufacturer_record.get('tozar')
            if manufacturer_record.get('tozeret_eretz_nm'):
                vehicle_data['country_of_origin'] = manufacturer_record.get('tozeret_eretz_nm')
            
            print(f"הועשר מידע התוצר עבור קוד {manufacturer_code}: {manufacturer_record.get('tozar')} מ{manufacturer_record.get('tozeret_eretz_nm')}")
        
        return vehicle_data