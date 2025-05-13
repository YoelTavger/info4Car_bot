def format_vehicle_info(vehicle_info, plate_number):
    """
    יוצר טקסט מפורמט של מידע על רכב
    
    Args:
        vehicle_info: מילון עם נתוני הרכב
        plate_number: מספר הרכב
        
    Returns:
        טקסט מפורמט של המידע על הרכב
    """
    info_text = f"*מידע על רכב מספר {plate_number}* 🚗\n\n"
    
    # מספר רכב ומסגרת (מידע חשוב)
    info_text += f"*מספר רכב:* {vehicle_info.get('mispar_rechev', 'לא ידוע')}\n"
    info_text += f"*מספר שילדה:* {vehicle_info.get('misgeret', 'לא ידוע')}\n\n"
    
    # מידע על היצרן והדגם
    info_text += f"*יצרן:* {vehicle_info.get('tozeret_nm', 'לא ידוע')}"
    if vehicle_info.get('tozeret_cd'):
        info_text += f" (קוד: {vehicle_info.get('tozeret_cd')})"
    info_text += "\n"
    
    info_text += f"*דגם:* {vehicle_info.get('degem_nm', 'לא ידוע')}"
    if vehicle_info.get('degem_cd'):
        info_text += f" (קוד: {vehicle_info.get('degem_cd')})"
    info_text += "\n"
    
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
        info_text += f"*מועד עלייה לכביש:* {vehicle_info.get('moed_aliya_lakvish')}\n"
        
    info_text += f"*סוג דלק:* {vehicle_info.get('sug_delek_nm', 'לא ידוע')}\n"
    
    # צבע הרכב
    info_text += f"*צבע:* {vehicle_info.get('tzeva_rechev', 'לא ידוע')}"
    if vehicle_info.get('tzeva_cd'):
        info_text += f" (קוד: {vehicle_info.get('tzeva_cd')})"
    info_text += "\n\n"
        
# מידע על צמיגים - כולל המידע הנוסף
    info_text += "*מידע על צמיגים:*\n"
    if vehicle_info.get('zmig_kidmi'):
        info_text += f"*צמיגים קדמיים:* {vehicle_info.get('zmig_kidmi')}"
        
        # הוספת מידע על עומס ומהירות מהמאגר השני (אם קיים)
        if vehicle_info.get('kod_omes_tzmig_kidmi'):
            info_text += f" | עומס: {vehicle_info.get('kod_omes_tzmig_kidmi')}"
        if vehicle_info.get('kod_mehirut_tzmig_kidmi'):
            info_text += f" | מהירות: {vehicle_info.get('kod_mehirut_tzmig_kidmi')}"
        info_text += "\n"
        
    if vehicle_info.get('zmig_ahori'):
        info_text += f"*צמיגים אחוריים:* {vehicle_info.get('zmig_ahori')}"
        
        # הוספת מידע על עומס ומהירות מהמאגר השני (אם קיים)
        if vehicle_info.get('kod_omes_tzmig_ahori'):
            info_text += f" | עומס: {vehicle_info.get('kod_omes_tzmig_ahori')}"
        if vehicle_info.get('kod_mehirut_tzmig_ahori'):
            info_text += f" | מהירות: {vehicle_info.get('kod_mehirut_tzmig_ahori')}"
        info_text += "\n"
    
    # מידע על גרירה (אם קיים)
    if vehicle_info.get('grira_nm'):
        info_text += f"*מידע על גרירה:* {vehicle_info.get('grira_nm')}\n"
        
    info_text += "\n"
    
    # מידע על רישוי ומבחנים
    info_text += f"*תוקף רישיון:* {vehicle_info.get('tokef_dt', 'לא ידוע')}\n"
    info_text += f"*מבחן אחרון:* {vehicle_info.get('mivchan_acharon_dt', 'לא ידוע')}\n"
    info_text += f"*בעלות:* {vehicle_info.get('baalut', 'לא ידוע')}\n"
    
    if vehicle_info.get('horaat_rishum'):
        info_text += f"*הוראת רישום:* {vehicle_info.get('horaat_rishum')}\n"
        
    # מידע על זיהום ובטיחות
    if vehicle_info.get('kvutzat_zihum') is not None:
        info_text += f"*קבוצת זיהום:* {vehicle_info.get('kvutzat_zihum')}\n"
        
    if vehicle_info.get('ramat_eivzur_betihuty'):
        info_text += f"*רמת אבזור בטיחותי:* {vehicle_info.get('ramat_eivzur_betihuty')}\n"
    
    return info_text