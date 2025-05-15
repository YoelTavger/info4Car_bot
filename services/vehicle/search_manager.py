import concurrent.futures
import time
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
        
    def search_parallel(self, license_plate, timeout=10):
        """
        חיפוש במקביל בכל המאגרים
        
        Args:
            license_plate: מספר הרכב לחיפוש
            timeout: זמן מקסימלי בשניות לחיפוש
            
        Returns:
            תוצאות החיפוש הראשונות או None אם לא נמצא
        """
        print(f"מחפש רכב מספר '{license_plate}' במקביל ב-{len(self.providers)} מאגרים")
        
        # משמש לשמירת התוצאה הראשונה שנמצאה
        first_result = None
        first_provider = None
        completed_futures = 0
        total_futures = len(self.providers)
        
        # יוצרים מאגר של workers
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # מילון שממפה עתידים (futures) לספקים
            future_to_provider = {}
            
            # שליחת כל הבקשות במקביל
            for provider in self.providers:
                future = executor.submit(provider.get_vehicle_data, license_plate)
                future_to_provider[future] = provider
            
            # ממתינים לתוצאות או לחריגת זמן
            try:
                for future in concurrent.futures.as_completed(future_to_provider, timeout=timeout):
                    completed_futures += 1
                    provider = future_to_provider[future]
                    
                    try:
                        data = future.result()
                        if data and not first_result:  # אם יש תוצאות וזו התוצאה הראשונה
                            first_result = data
                            first_provider = provider.name
                            print(f"נמצא רכב מספר '{license_plate}' במאגר '{provider.name}'")
                            # נמשיך לחכות לאחרים אבל לפחות יש לנו תוצאה
                    except Exception as e:
                        print(f"שגיאה בחיפוש ב{provider.name}: {e}")
                        # המשך למרות השגיאה
                
                # ניתן לרשום כמה נסיימו
                print(f"הושלמו {completed_futures} מתוך {total_futures} חיפושים")
                
                # אם מצאנו משהו, נחזיר אותו
                if first_result:
                    return first_result, first_provider
                
                # אם הגענו לכאן, לא נמצאו תוצאות
                return None, None
                
            except concurrent.futures.TimeoutError:
                print(f"חריגת זמן: הושלמו {completed_futures} מתוך {total_futures} חיפושים. נמצאו תוצאות: {first_result is not None}")
                
                # אם למרות חריגת הזמן יש לנו תוצאה, נחזיר אותה
                if first_result:
                    return first_result, first_provider
                
                # אם אין תוצאות כלל, ננסה בשיטה הטורית עם הספקים העיקריים
                print("ננסה חיפוש טורי במאגרים העיקריים...")
                return self.search_sequential_main_providers(license_plate)
    
    def search_sequential_main_providers(self, license_plate):
        """
        חיפוש טורי במאגרים העיקריים בלבד (גיבוי כשהחיפוש המקבילי נכשל)
        
        Args:
            license_plate: מספר הרכב לחיפוש
            
        Returns:
            תוצאות החיפוש או None אם לא נמצא
        """
        # מאגרים עיקריים (שלושת הראשונים)
        main_providers = self.providers[:3]
        
        for provider in main_providers:
            try:
                data = provider.get_vehicle_data(license_plate)
                if data:
                    print(f"נמצא רכב מספר '{license_plate}' במאגר '{provider.name}' (חיפוש טורי)")
                    return data, provider.name
            except Exception as e:
                print(f"שגיאה בחיפוש ב{provider.name}: {e}")
        
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
            try:
                data = provider.get_vehicle_data(license_plate)
                if data:
                    print(f"נמצא רכב מספר '{license_plate}' במאגר '{provider.name}' (חיפוש טורי)")
                    return data, provider.name
            except Exception as e:
                print(f"שגיאה בחיפוש ב{provider.name}: {e}")
        
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
        try:
            if strategy == "parallel":
                return self.search_parallel(license_plate)
            else:
                return self.search_sequential(license_plate)
        except Exception as e:
            print(f"שגיאה כללית בחיפוש רכב: {e}")
            # במקרה של שגיאה כללית, ננסה את שיטת הגיבוי
            return self.search_sequential_main_providers(license_plate)