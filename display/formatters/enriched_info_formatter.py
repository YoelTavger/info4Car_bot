from display.formatters.date_formatter import format_date

def format_enriched_info(vehicle_info):
    """
    מעצב את המידע המועשר על הרכב מהמאגרים הנוספים
    
    Args:
        vehicle_info: מילון עם נתוני הרכב
    
    Returns:
        טקסט מפורמט עם המידע המועשר
    """
    info_text = ""
    
    # הוספת מידע היסטורי אם קיים
    info_text += "\n*היסטוריית הרכב:*\n"
    if vehicle_info.get('historia'):
        hist = vehicle_info['historia']
        
        if hist.get('kilometer_test_aharon'):
            info_text += f"*קילומטראז' במבחן אחרון:* {hist.get('kilometer_test_aharon')} ק\"מ\n"
        
        if hist.get('rishum_rishon_dt'):
            date = format_date(hist.get('rishum_rishon_dt'))
            info_text += f"*תאריך רישום ראשון:* {date}\n"
        
        if hist.get('mkoriut_nm'):
            info_text += f"*מקוריות:* {hist.get('mkoriut_nm')}\n"
        
        # אינדיקטורים להיסטוריה
        indicators = []
        if hist.get('shinui_mivne_ind') == 'Y':
            indicators.append("שינוי מבנה")
        if hist.get('gapam_ind') == 'Y':
            indicators.append("גפ\"ם (גז)")
        if hist.get('shnui_zeva_ind') == 'Y':
            indicators.append("שינוי צבע")
        if hist.get('shinui_zmig_ind') == 'Y':
            indicators.append("שינוי צמיגים")
        
        if indicators:
            info_text += f"*שינויים:* {', '.join(indicators)}\n"
    else:
        info_text += "אין מידע היסטורי זמין ❌\n"
    
    # הוספת מידע על תו נכה
    info_text += "\n*תו נכה:*\n"
    if vehicle_info.get('tav_nehe') and vehicle_info['tav_nehe'].get('kiyum'):
        info_text += f"*סוג תו:* {vehicle_info['tav_nehe'].get('sug_tav', 'לא ידוע')}\n"
        
        # פורמט תאריך הפקת תג
        tag_date = vehicle_info['tav_nehe'].get('taarich_hafakat_tag', '')
        # המרה למחרוזת במקרה שמדובר במספר
        tag_date = str(tag_date) if tag_date else ''
        if tag_date and len(tag_date) == 8:  # אם התאריך הוא בפורמט YYYYMMDD
            formatted_date = f"{tag_date[6:8]}-{tag_date[4:6]}-{tag_date[0:4]}"
            info_text += f"*תאריך הפקת תג:* {formatted_date}\n"
        else:
            info_text += f"*תאריך הפקת תג:* {tag_date}\n"
    else:
        info_text += "לרכב אין תו נכה ❌\n"
    
    # הוספת מידע על מערכות בטיחות
    info_text += "\n*מערכות בטיחות:*\n"
    if vehicle_info.get('maarchot_betihut') and vehicle_info['maarchot_betihut'].get('kiyum'):
        info_text += "הרכב נמצא במאגר מערכות הבטיחות ✅\n"
        
        if vehicle_info['maarchot_betihut'].get('updated_dt'):
            date = format_date(vehicle_info['maarchot_betihut'].get('updated_dt'))
            info_text += f"*תאריך עדכון:* {date}\n"
    else:
        info_text += "הרכב אינו רשום במאגר מערכות הבטיחות ❌\n"
    
    return info_text