from services.vehicle.base_provider import VehicleDataProvider
from config import GOVIL_API_URL, RESOURCE_ID_PRIVATE_VEHICLES

class PrivateVehiclesProvider(VehicleDataProvider):
    """
    ספק נתונים עבור רכבים פרטיים ומסחריים עד 3.5 טון
    """
    def __init__(self):
        super().__init__(
            api_url=GOVIL_API_URL,
            resource_id=RESOURCE_ID_PRIVATE_VEHICLES,
            name="מאגר רכב פרטי",
            id_field="mispar_rechev"
        )
    
    def get_vehicle_data(self, license_plate):
        """
        מקבל מידע על רכב פרטי לפי מספר רישוי
        
        Args:
            license_plate: מספר הרכב לחיפוש
            
        Returns:
            נתוני רכב או None אם לא נמצא
        """
        return self.fetch_data(license_plate)