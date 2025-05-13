from services.vehicle.data_provider import get_vehicle_data
from services.vehicle.extended_data_provider import get_vehicle_extended_data

def get_vehicle_complete(license_plate):
    """
    מחזיר מידע מאוחד מכל המאגרים על הרכב
    
    Args:
        license_plate: מספר הרכב לחיפוש
        
    Returns:
        רשימה עם מידע מלא מאוחד או None אם לא נמצא
    """
    vehicle_data = get_vehicle_data(license_plate)
    if not vehicle_data:
        return None
        
    # ניסיון לקבל מידע נוסף מהמאגר השני
    extended_data = get_vehicle_extended_data(license_plate)
    
    # אם מצאנו מידע נוסף, נשלב אותו עם המידע הקיים
    if extended_data:
        # מעבר על כל שדה במידע הנוסף ושילובו בנתונים הקיימים
        for key, value in extended_data.items():
            # אם השדה לא קיים במידע הראשי או אם הוא ריק, נוסיף אותו
            if key not in vehicle_data[0] or not vehicle_data[0][key]:
                vehicle_data[0][key] = value
    
    # print(f"מידע מאוחד: {vehicle_data}")
    return vehicle_data