from services.vehicle.base_provider import VehicleDataProvider
from config import GOVIL_API_URL, RESOURCE_ID_FINAL_CANCELED

class FinalCanceledProvider(VehicleDataProvider):
    """
    ספק נתונים עבור רכבים שירדו מהכביש
    """
    def __init__(self):
        super().__init__(
            api_url=GOVIL_API_URL,
            resource_id=RESOURCE_ID_FINAL_CANCELED,
            name="מאגר רכב שירד מהכביש"
        )
    
    def get_vehicle_data(self, license_plate):
        return self.fetch_data(license_plate)