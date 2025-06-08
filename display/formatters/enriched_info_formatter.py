from display.formatters.date_formatter import format_date

def format_enriched_info(vehicle_info, show_all_fields=False):
    """
    מעצב את המידע המועשר על הרכב מהמאגרים הנוספים
    
    Args:
        vehicle_info: מילון עם נתוני הרכב
        show_all_fields: האם להציג גם שדות ריקים
    
    Returns:
        טקסט מפורמט עם המידע המועשר
    """
    info_text = ""
    
    # הוספת מידע היסטורי
    historia = vehicle_info.get('historia')
    if historia or show_all_fields:
        info_text += "\n*היסטוריית הרכב:*\n"
        
        if historia:
            if historia.get('kilometer_test_aharon') or show_all_fields:
                km_value = historia.get('kilometer_test_aharon', 'לא ידוע') if show_all_fields else historia.get('kilometer_test_aharon')
                info_text += f"*קילומטראז' במבחן אחרון:* {km_value} ק\"מ\n"
            
            if historia.get('rishum_rishon_dt') or show_all_fields:
                date_value = historia.get('rishum_rishon_dt')
                if date_value:
                    date_value = format_date(date_value)
                else:
                    date_value = 'לא ידוע'
                info_text += f"*תאריך רישום ראשון:* {date_value}\n"
            
            if historia.get('mkoriut_nm') or show_all_fields:
                mkoriut_value = historia.get('mkoriut_nm', 'לא ידוע') if show_all_fields else historia.get('mkoriut_nm')
                info_text += f"*מקוריות:* {mkoriut_value}\n"
            
            # אינדיקטורים להיסטוריה
            indicators = []
            if historia.get('shinui_mivne_ind') == 'Y':
                indicators.append("שינוי מבנה")
            elif show_all_fields and historia.get('shinui_mivne_ind') == 'N':
                indicators.append("ללא שינוי מבנה")
                
            if historia.get('gapam_ind') == 'Y':
                indicators.append("גפ\"ם (גז)")
            elif show_all_fields and historia.get('gapam_ind') == 'N':
                indicators.append("ללא גפ\"ם")
                
            if historia.get('shnui_zeva_ind') == 'Y':
                indicators.append("שינוי צבע")
            elif show_all_fields and historia.get('shnui_zeva_ind') == 'N':
                indicators.append("ללא שינוי צבע")
                
            if historia.get('shinui_zmig_ind') == 'Y':
                indicators.append("שינוי צמיגים")
            elif show_all_fields and historia.get('shinui_zmig_ind') == 'N':
                indicators.append("ללא שינוי צמיגים")
            
            if indicators:
                info_text += f"*שינויים:* {', '.join(indicators)}\n"
            elif show_all_fields:
                info_text += "*שינויים:* לא ידוע\n"
        else:
            info_text += "אין מידע היסטורי זמין ❌\n"
    
    # הוספת מידע על תו נכה
    tav_nehe = vehicle_info.get('tav_nehe')
    if tav_nehe or show_all_fields:
        info_text += "\n*תו נכה:*\n"
        
        if tav_nehe and tav_nehe.get('kiyum'):
            if tav_nehe.get('sug_tav') or show_all_fields:
                sug_value = tav_nehe.get('sug_tav', 'לא ידוע') if show_all_fields else tav_nehe.get('sug_tav')
                info_text += f"*סוג תו:* {sug_value}\n"
            
            # פורמט תאריך הפקת תג
            tag_date = tav_nehe.get('taarich_hafakat_tag', '')
            if tag_date or show_all_fields:
                # המרה למחרוזת במקרה שמדובר במספר
                tag_date = str(tag_date) if tag_date else ''
                if tag_date and len(tag_date) == 8:  # אם התאריך הוא בפורמט YYYYMMDD
                    formatted_date = f"{tag_date[6:8]}-{tag_date[4:6]}-{tag_date[0:4]}"
                    info_text += f"*תאריך הפקת תג:* {formatted_date}\n"
                elif show_all_fields:
                    info_text += f"*תאריך הפקת תג:* {tag_date or 'לא ידוע'}\n"
                elif tag_date:
                    info_text += f"*תאריך הפקת תג:* {tag_date}\n"
        else:
            info_text += "לרכב אין תו נכה ❌\n"
    
    # הוספת מידע על מערכות בטיחות
    maarchot_betihut = vehicle_info.get('maarchot_betihut')
    if maarchot_betihut or show_all_fields:
        info_text += "\n*מערכות בטיחות:*\n"
        
        if maarchot_betihut and maarchot_betihut.get('kiyum'):
            info_text += "הרכב נמצא במאגר מערכות הבטיחות ✅\n"
            
            if maarchot_betihut.get('updated_dt') or show_all_fields:
                date_value = maarchot_betihut.get('updated_dt')
                if date_value:
                    date_value = format_date(date_value)
                else:
                    date_value = 'לא ידוע'
                info_text += f"*תאריך עדכון:* {date_value}\n"
        else:
            info_text += "הרכב אינו רשום במאגר מערכות הבטיחות ❌\n"
    
    return info_text