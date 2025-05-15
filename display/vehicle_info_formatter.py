from display.formatters.date_formatter import format_date, format_road_date
from display.formatters.basic_info_formatter import format_basic_info
from display.formatters.technical_info_formatter import format_technical_info
from display.formatters.wltp_info_formatter import format_wltp_info
from display.formatters.enriched_info_formatter import format_enriched_info
from display.formatters.ownership_history_formatter import format_ownership_history

def format_vehicle_info(vehicle_info, plate_number):
    """
    יוצר טקסט מפורמט של מידע על רכב
    
    Args:
        vehicle_info: מילון עם נתוני הרכב
        plate_number: מספר הרכב
        
    Returns:
        טקסט מפורמט של המידע על הרכב
    """
    # קבלת מקור המידע אם קיים
    data_source = vehicle_info.get('data_source', 'מאגר מידע רכב')
    
    # כותרת ומידע בסיסי
    info_text = f"*מידע על רכב מספר {plate_number}* 🚗\n"
    info_text += f"*מקור המידע:* {data_source}\n\n"
    
    # הוספת מידע על יד וסוג בעלות נוכחית אם קיים
    if vehicle_info.get('current_hand'):
        info_text += f"*יד נוכחית:* {vehicle_info.get('current_hand')}"
        info_text += f" | *סוג בעלות:* {vehicle_info.get('current_ownership_type')}\n\n"
    
    # הוספת מידע בסיסי
    info_text += format_basic_info(vehicle_info)
    
    # הוספת מידע טכני
    info_text += format_technical_info(vehicle_info)
    
    # הוספת מידע WLTP
    info_text += format_wltp_info(vehicle_info)
    
    # הוספת מידע מועשר
    info_text += format_enriched_info(vehicle_info)
    
    # הוספת היסטוריית בעלויות
    info_text += format_ownership_history(vehicle_info)
    
    return info_text