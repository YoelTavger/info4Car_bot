from display.formatters.date_formatter import format_date, format_road_date

def format_basic_info(vehicle_info):
    """
    מעצב את המידע הבסיסי על הרכב
    
    Args:
        vehicle_info: מילון עם נתוני הרכב
    
    Returns:
        טקסט מפורמט עם המידע הבסיסי
    """
    info_text = ""
    
    # מספר רכב ומסגרת (מידע חשוב)
    info_text += f"*מספר רכב:* {vehicle_info.get('mispar_rechev', 'לא ידוע')}\n"
    
    # בדיקה איזה שדה של מספר שילדה קיים
    if vehicle_info.get('misgeret'):
        info_text += f"*מספר שילדה:* {vehicle_info.get('misgeret')}\n\n"
    elif vehicle_info.get('mispar_shilda'):
        info_text += f"*מספר שילדה:* {vehicle_info.get('mispar_shilda')}\n\n"
    elif vehicle_info.get('shilda'):
        info_text += f"*מספר שילדה:* {vehicle_info.get('shilda')}\n\n"
    else:
        info_text += f"*מספר שילדה:* לא ידוע\n\n"
    
    # מידע על היצרן והדגם
    info_text += f"*יצרן:* {vehicle_info.get('tozeret_nm', 'לא ידוע')}"
    if vehicle_info.get('tozeret_cd'):
        info_text += f" (קוד: {vehicle_info.get('tozeret_cd')})"
    info_text += "\n"
    
    info_text += f"*דגם:* {vehicle_info.get('degem_nm', 'לא ידוע')}"
    if vehicle_info.get('degem_cd'):
        info_text += f" (קוד: {vehicle_info.get('degem_cd')})"
    info_text += "\n"
    
    # בדיקת סוג הרכב אם קיים
    if vehicle_info.get('sug_rechev_nm'):
        info_text += f"*סוג רכב:* {vehicle_info.get('sug_rechev_nm')}\n"
    
    if vehicle_info.get('sug_degem'):
        info_text += f"*סוג דגם:* {vehicle_info.get('sug_degem')}\n"
        
    if vehicle_info.get('kinuy_mishari'):
        info_text += f"*כינוי מסחרי:* {vehicle_info.get('kinuy_mishari')}\n"
        
    if vehicle_info.get('ramat_gimur'):
        info_text += f"*רמת גימור:* {vehicle_info.get('ramat_gimur')}\n"
        
    if vehicle_info.get('degem_manoa'):
        info_text += f"*דגם מנוע:* {vehicle_info.get('degem_manoa')}\n"
    
    info_text += "\n"
    
    # נתונים עיקריים
    info_text += f"*שנת ייצור:* {vehicle_info.get('shnat_yitzur', 'לא ידוע')}\n"
    
    if vehicle_info.get('moed_aliya_lakvish'):
        # עיצוב מועד עלייה לכביש - בפורמט "חודש בעברית שנה"
        aliya = format_road_date(vehicle_info.get('moed_aliya_lakvish'))
        info_text += f"*מועד עלייה לכביש:* {aliya}\n"
    
    if vehicle_info.get('bitul_dt'):
        date = format_date(vehicle_info.get('bitul_dt'))
        info_text += f"*תאריך ביטול רישום:* {date}\n"
    
    # בדיקה איזה שדה של סוג דלק קיים
    if vehicle_info.get('sug_delek_nm'):
        info_text += f"*סוג דלק:* {vehicle_info.get('sug_delek_nm')}\n"
    
    # צבע הרכב
    if vehicle_info.get('tzeva_rechev'):
        info_text += f"*צבע:* {vehicle_info.get('tzeva_rechev', 'לא ידוע')}"
        if vehicle_info.get('tzeva_cd'):
            info_text += f" (קוד: {vehicle_info.get('tzeva_cd')})"
        info_text += "\n"
    
    return info_text