from services.vehicle.base_provider import VehicleDataProvider
from config import GOVIL_API_URL, RESOURCE_ID_HEAVY_VEHICLES

class HeavyVehiclesProvider(VehicleDataProvider):
    """
    ספק נתונים עבור רכבים מעל 3.5 טון
    """
    def __init__(self):
        super().__init__(
            api_url=GOVIL_API_URL,
            resource_id=RESOURCE_ID_HEAVY_VEHICLES,
            name="מאגר רכב כבד"
        )
    
    def get_vehicle_data(self, license_plate):
        return self.fetch_data(license_plate)