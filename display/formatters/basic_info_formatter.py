from display.formatters.date_formatter import format_date, format_road_date

def format_basic_info(vehicle_info, show_all_fields=False):
    """
    מעצב את המידע הבסיסי על הרכב
    
    Args:
        vehicle_info: מילון עם נתוני הרכב
        show_all_fields: האם להציג גם שדות ריקים
    
    Returns:
        טקסט מפורמט עם המידע הבסיסי
    """
    info_text = ""
    
    # מספר שילדה (ללא מספר רכב כי הוא כבר בכותרת)
    chassis_number = None
    if vehicle_info.get('misgeret'):
        chassis_number = vehicle_info.get('misgeret')
    elif vehicle_info.get('mispar_shilda'):
        chassis_number = vehicle_info.get('mispar_shilda')
    elif vehicle_info.get('shilda'):
        chassis_number = vehicle_info.get('shilda')
    
    if chassis_number or show_all_fields:
        info_text += f"*מספר שילדה:* {chassis_number or 'לא ידוע'}\n\n"
    elif chassis_number:  # רק אם יש מידע
        info_text += f"*מספר שילדה:* {chassis_number}\n\n"
    
    # מידע על היצרן והדגם - עם העשרה ממאגר התוצרים
    manufacturer_info = vehicle_info.get('manufacturer_info', {})
    
    if manufacturer_info:
        # מידע מעושר ממאגר התוצרים
        brand = manufacturer_info.get('tozar', vehicle_info.get('tozeret_nm', 'לא ידוע'))
        country = manufacturer_info.get('tozeret_eretz_nm', '')
        manufacturer_code = manufacturer_info.get('tozeret_cd', vehicle_info.get('tozeret_cd', ''))
        
        info_text += f"*יצרן:* {brand}\n"
        if country or show_all_fields:
            country_display = country if country else 'לא ידוע'
            info_text += f"*תוצרת:* {country_display}\n"
        
        if show_all_fields and manufacturer_code:
            info_text += f"*קוד יצרן:* {manufacturer_code}\n"
    else:
        # מידע בסיסי אם אין העשרה
        manufacturer = vehicle_info.get('tozeret_nm', 'לא ידוע')
        manufacturer_code = vehicle_info.get('tozeret_cd', '')
        
        info_text += f"*יצרן:* {manufacturer}\n"
        if show_all_fields and manufacturer_code:
            info_text += f"*קוד יצרן:* {manufacturer_code}\n"
    
    model = vehicle_info.get('degem_nm', 'לא ידוע')
    model_code = vehicle_info.get('degem_cd', '')
    
    info_text += f"*דגם:* {model}"
    if model_code and (model_code or show_all_fields):
        info_text += f" (קוד: {model_code})"
    elif show_all_fields:
        info_text += " (קוד: לא ידוע)"
    info_text += "\n"
    
    # רשימת שדות נוספים עם תרגומים
    additional_fields = [
        ('sug_rechev_nm', 'סוג רכב'),
        ('sug_degem', 'סוג דגם'),
        ('kinuy_mishari', 'כינוי מסחרי'),
        ('ramat_gimur', 'רמת גימור'),
        ('degem_manoa', 'דגם מנוע'),
    ]
    
    for field_key, field_name in additional_fields:
        field_value = vehicle_info.get(field_key, '')
        if field_value or show_all_fields:
            display_value = field_value if field_value else 'לא ידוע'
            info_text += f"*{field_name}:* {display_value}\n"
    
    info_text += "\n"
    
    # נתונים עיקריים
    year = vehicle_info.get('shnat_yitzur', '')
    if year or show_all_fields:
        display_year = year if year else 'לא ידוע'
        info_text += f"*שנת ייצור:* {display_year}\n"
    
    if vehicle_info.get('moed_aliya_lakvish') or show_all_fields:
        aliya = vehicle_info.get('moed_aliya_lakvish')
        if aliya:
            aliya = format_road_date(aliya)
        else:
            aliya = 'לא ידוע'
        info_text += f"*מועד עלייה לכביש:* {aliya}\n"
    
    if vehicle_info.get('bitul_dt') or show_all_fields:
        cancel_date = vehicle_info.get('bitul_dt')
        if cancel_date:
            cancel_date = format_date(cancel_date)
        else:
            cancel_date = 'לא ידוע'
        info_text += f"*תאריך ביטול רישום:* {cancel_date}\n"
    
    # סוג דלק
    fuel_type = vehicle_info.get('sug_delek_nm', '')
    if fuel_type or show_all_fields:
        display_fuel = fuel_type if fuel_type else 'לא ידוע'
        info_text += f"*סוג דלק:* {display_fuel}\n"
    
    # צבע הרכב
    color = vehicle_info.get('tzeva_rechev', '')
    color_code = vehicle_info.get('tzeva_cd', '')
    
    if color or show_all_fields:
        display_color = color if color else 'לא ידוע'
        info_text += f"*צבע:* {display_color}"
        if color_code and (color_code or show_all_fields):
            info_text += f" (קוד: {color_code})"
        elif show_all_fields:
            info_text += " (קוד: לא ידוע)"
        info_text += "\n"
    
    # אם תצוגה מפורטת, הוספת מידע על מקור הנתונים
    if show_all_fields:
        data_source = vehicle_info.get('data_source', 'לא ידוע')
        info_text += f"\n*מקור נתונים בסיסיים:* {data_source}\n"
    
    return info_text