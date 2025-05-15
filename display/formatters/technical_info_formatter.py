from display.formatters.date_formatter import format_date

def format_technical_info(vehicle_info):
    """
    מעצב את המידע הטכני על הרכב
    
    Args:
        vehicle_info: מילון עם נתוני הרכב
    
    Returns:
        טקסט מפורמט עם המידע הטכני
    """
    info_text = "\n"
    
    # מידע על משקל אם קיים
    if vehicle_info.get('mishkal_kolel'):
        info_text += f"*משקל כולל:* {vehicle_info.get('mishkal_kolel')} ק\"ג\n"
    
    if vehicle_info.get('mishkal_azmi'):
        info_text += f"*משקל עצמי:* {vehicle_info.get('mishkal_azmi')} ק\"ג\n"
    
    # מידע על צמיגים - רק אם יש מידע
    has_tire_info = (
        vehicle_info.get('zmig_kidmi') or 
        vehicle_info.get('zmig_ahori') or 
        vehicle_info.get('mida_zmig_kidmi') or 
        vehicle_info.get('mida_zmig_ahori')
    )
    
    if has_tire_info:
        info_text += "\n*מידע על צמיגים:*\n"
        
        if vehicle_info.get('zmig_kidmi'):
            info_text += f"*צמיגים קדמיים:* {vehicle_info.get('zmig_kidmi')}"
            
            # הוספת מידע על עומס ומהירות מהמאגר השני (אם קיים)
            if vehicle_info.get('kod_omes_tzmig_kidmi'):
                info_text += f" | עומס: {vehicle_info.get('kod_omes_tzmig_kidmi')}"
            if vehicle_info.get('kod_mehirut_tzmig_kidmi'):
                info_text += f" | מהירות: {vehicle_info.get('kod_mehirut_tzmig_kidmi')}"
            info_text += "\n"
        
        if vehicle_info.get('mida_zmig_kidmi'):
            info_text += f"*צמיגים קדמיים:* {vehicle_info.get('mida_zmig_kidmi')}"
            if vehicle_info.get('kod_omes_zmig_kidmi'):
                info_text += f" | עומס: {vehicle_info.get('kod_omes_zmig_kidmi')}"
            if vehicle_info.get('kod_mehirut_zmig_kidmi'):
                info_text += f" | מהירות: {vehicle_info.get('kod_mehirut_zmig_kidmi')}"
            info_text += "\n"
            
        if vehicle_info.get('zmig_ahori'):
            info_text += f"*צמיגים אחוריים:* {vehicle_info.get('zmig_ahori')}"
            
            # הוספת מידע על עומס ומהירות מהמאגר השני (אם קיים)
            if vehicle_info.get('kod_omes_tzmig_ahori'):
                info_text += f" | עומס: {vehicle_info.get('kod_omes_tzmig_ahori')}"
            if vehicle_info.get('kod_mehirut_tzmig_ahori'):
                info_text += f" | מהירות: {vehicle_info.get('kod_mehirut_tzmig_ahori')}"
            info_text += "\n"
        
        if vehicle_info.get('mida_zmig_ahori'):
            info_text += f"*צמיגים אחוריים:* {vehicle_info.get('mida_zmig_ahori')}"
            if vehicle_info.get('kod_omes_zmig_ahori'):
                info_text += f" | עומס: {vehicle_info.get('kod_omes_zmig_ahori')}"
            if vehicle_info.get('kod_mehirut_zmig_ahori'):
                info_text += f" | מהירות: {vehicle_info.get('kod_mehirut_zmig_ahori')}"
            info_text += "\n"
        
        # מידע על גרירה (אם קיים)
        if vehicle_info.get('grira_nm'):
            info_text += f"*מידע על גרירה:* {vehicle_info.get('grira_nm')}\n"
    
    # מידע על רישוי ומבחנים
    info_text += "\n"
    if vehicle_info.get('tokef_dt'):
        date = format_date(vehicle_info.get('tokef_dt'))
        info_text += f"*תוקף רישיון:* {date}\n"
    
    if vehicle_info.get('mivchan_acharon_dt'):
        date = format_date(vehicle_info.get('mivchan_acharon_dt'))
        info_text += f"*מבחן אחרון:* {date}\n"
    
    if vehicle_info.get('baalut'):
        info_text += f"*בעלות:* {vehicle_info.get('baalut')}\n"
    
    if vehicle_info.get('horaat_rishum'):
        info_text += f"*הוראת רישום:* {vehicle_info.get('horaat_rishum')}\n"
    
    if vehicle_info.get('sug_yevu'):
        info_text += f"*סוג יבוא:* {vehicle_info.get('sug_yevu')}\n"
        
    # מידע על זיהום ובטיחות
    if vehicle_info.get('kvutzat_zihum') is not None:
        info_text += f"*קבוצת זיהום:* {vehicle_info.get('kvutzat_zihum')}\n"
        
    if vehicle_info.get('ramat_eivzur_betihuty'):
        info_text += f"*רמת אבזור בטיחותי:* {vehicle_info.get('ramat_eivzur_betihuty')}\n"
    
    return info_text