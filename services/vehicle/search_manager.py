import concurrent.futures
from services.vehicle.providers.private_vehicles import PrivateVehiclesProvider
from services.vehicle.providers.heavy_vehicles import HeavyVehiclesProvider
from services.vehicle.providers.motorcycles import MotorcyclesProvider
from services.vehicle.providers.inactive_vehicles import InactiveVehiclesProvider
from services.vehicle.providers.inactive_heavy import InactiveHeavyProvider
from services.vehicle.providers.final_canceled import FinalCanceledProvider
from services.vehicle.providers.personal_import import PersonalImportProvider

class VehicleSearchManager:
    """
    מנהל חיפוש שמחפש במספר מאגרים במקביל או בזה אחר זה
    """
    def __init__(self):
        # יצירת כל ספקי הנתונים
        self.providers = [
            PrivateVehiclesProvider(),
            HeavyVehiclesProvider(),
            MotorcyclesProvider(),
            InactiveVehiclesProvider(),
            InactiveHeavyProvider(),
            FinalCanceledProvider(),
            PersonalImportProvider()
        ]
        
    def search_parallel(self, license_plate, timeout=5):
        """
        חיפוש במקביל בכל המאגרים
        
        Args:
            license_plate: מספר הרכב לחיפוש
            timeout: זמן מקסימלי בשניות לחיפוש
            
        Returns:
            תוצאות החיפוש הראשונות או None אם לא נמצא
        """
        # מגדירים רשימת ספקים פעילים
        active_providers = self.providers
        
        # יוצרים מאגר של workers
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # שולחים את כל הבקשות במקביל
            future_to_provider = {
                executor.submit(provider.get_vehicle_data, license_plate): provider
                for provider in active_providers
            }
            
            # ממתינים לתוצאה הראשונה שתחזור
            for future in concurrent.futures.as_completed(future_to_provider, timeout=timeout):
                provider = future_to_provider[future]
                try:
                    data = future.result()
                    if data:  # אם יש תוצאות
                        # מחזירים את התוצאות הראשונות שנמצאו
                        return data, provider.name
                except Exception as e:
                    print(f"שגיאה בחיפוש ב{provider.name}: {e}")
        
        # אם לא נמצאו תוצאות באף אחד מהמאגרים
        return None, None
    
    def search_sequential(self, license_plate):
        """
        חיפוש בזה אחר זה במאגרים לפי סדר עדיפות
        
        Args:
            license_plate: מספר הרכב לחיפוש
            
        Returns:
            תוצאות החיפוש או None אם לא נמצא
        """
        for provider in self.providers:
            data = provider.get_vehicle_data(license_plate)
            if data:
                return data, provider.name
        
        return None, None
    
    def search_vehicle(self, license_plate, strategy="parallel"):
        """
        חיפוש רכב לפי אסטרטגיה
        
        Args:
            license_plate: מספר הרכב לחיפוש
            strategy: אסטרטגיית חיפוש ("parallel" או "sequential")
            
        Returns:
            תוצאות החיפוש או None אם לא נמצא
        """
        if strategy == "parallel":
            return self.search_parallel(license_plate)
        else:
            return self.search_sequential(license_plate)
        