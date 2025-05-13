from services.vehicle.search_manager import VehicleSearchManager
from services.vehicle.enrichers.extended_info import ExtendedInfoEnricher

class VehicleService:
    """
    שירות מאוחד לקבלת מידע מלא על רכב
    """
    
    def __init__(self):
        self.search_manager = VehicleSearchManager()
        self.extended_info_enricher = ExtendedInfoEnricher()
        # ניתן להוסיף עוד מעשירי נתונים לפי הצורך
    
    def get_vehicle_data(self, license_plate, strategy="parallel"):
        """
        מקבל מידע בסיסי על רכב
        
        Args:
            license_plate: מספר הרכב
            strategy: אסטרטגיית חיפוש
            
        Returns:
            נתוני רכב או None אם לא נמצא
        """
        # חיפוש בסיסי
        vehicle_data, source = self.search_manager.search_vehicle(license_plate, strategy)
        return vehicle_data, source
    
    def get_vehicle_complete(self, license_plate, strategy="parallel"):
        """
        מקבל מידע מורחב על רכב
        
        Args:
            license_plate: מספר הרכב
            strategy: אסטרטגיית חיפוש
            
        Returns:
            נתוני רכב מלאים או None אם לא נמצא
        """
        # חיפוש בסיסי
        vehicle_data, source = self.search_manager.search_vehicle(license_plate, strategy)
        
        if not vehicle_data:
            return None
        
        # העשרת נתונים
        enriched_data = self.extended_info_enricher.enrich(vehicle_data, license_plate)
        
        return enriched_data
    
    def get_vehicle_with_history(self, license_plate, callback=None):
        """
        מקבל מידע מלא כולל היסטוריה, עם אופציה לקולבק כשיש עדכון
        
        Args:
            license_plate: מספר הרכב
            callback: פונקציית קולבק לעדכון כשמגיע מידע נוסף
            
        Returns:
            נתוני רכב בסיסיים מיידית
        """
        # חיפוש בסיסי והחזרה מיידית
        vehicle_data, source = self.search_manager.search_vehicle(license_plate)
        
        if not vehicle_data:
            return None
        
        # העשרת מידע בסיסי (מהיר)
        vehicle_data = self.extended_info_enricher.enrich(vehicle_data, license_plate)
        
        # TODO: העשרת מידע נוספת בתהליך נפרד והפעלת קולבק
        
        return vehicle_data