from services.vehicle.base_provider import VehicleDataProvider
from config import GOVIL_API_URL, RESOURCE_ID_INACTIVE_VEHICLES

class InactiveVehiclesProvider(VehicleDataProvider):
    """
    ספק נתונים עבור רכבים לא פעילים
    """
    def __init__(self):
        super().__init__(
            api_url=GOVIL_API_URL,
            resource_id=RESOURCE_ID_INACTIVE_VEHICLES,
            name="מאגר רכב לא פעיל"
        )
    
    def get_vehicle_data(self, license_plate):
        return self.fetch_data(license_plate)