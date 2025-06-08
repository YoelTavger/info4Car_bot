def format_ownership_history(vehicle_info, show_all_fields=False):
    """
    מעצב את היסטוריית הבעלויות של הרכב
    
    Args:
        vehicle_info: מילון עם נתוני הרכב
        show_all_fields: האם להציג גם שדות ריקים
    
    Returns:
        טקסט מפורמט עם היסטוריית הבעלויות
    """
    info_text = ""
    
    # בדיקה אם יש היסטוריית בעלויות
    ownership_history = vehicle_info.get('ownership_history')
    if not ownership_history and not show_all_fields:
        return info_text
    
    # חישוב יד הרכב (לא כולל סוחרים)
    yad_rechev = vehicle_info.get('yad_rechev', 0)
    
    info_text += "\n*היסטוריית בעלויות:*\n"
    
    # הצגת יד הרכב
    if yad_rechev > 0:
        info_text += f"*רכב יד:* {yad_rechev}\n\n"
    elif show_all_fields:
        info_text += f"*רכב יד:* לא ידוע\n\n"
    
    if not ownership_history:
        if show_all_fields:
            info_text += "אין היסטוריית בעלויות זמינה ❌\n"
        return info_text
    
    # הצגת רשימת הבעלויות
    history = ownership_history
    
    # מיון הרשומות לפי תאריך (מהישן לחדש)
    def get_date_key(record):
        date = record.get('baalut_dt', '0')
        return str(date) if date is not None else '0'
        
    sorted_history = sorted(history, key=get_date_key)
    
    # הצגת הבעלויות מהראשון לנוכחי
    for i, record in enumerate(sorted_history):
        # עיצוב התאריך מפורמט YYYYMM לחודש/שנה
        baalut_dt = record.get('baalut_dt', '')
        formatted_date = format_ownership_date(baalut_dt)
        
        # הצגת סוג הבעלות והתאריך
        baalut_type = record.get('baalut', 'לא ידוע')
        
        if i == len(sorted_history) - 1:
            info_text += f"*בעלות נוכחית:* {baalut_type}"
        else:
            info_text += f"*בעלות {i+1}:* {baalut_type}"
            
        if formatted_date:
            info_text += f" ({formatted_date})"
        elif show_all_fields:
            info_text += " (תאריך לא ידוע)"
            
        info_text += "\n"
        
        # אם תצוגה מפורטת, הוסף פרטים נוספים על הבעלות
        if show_all_fields:
            additional_info = []
            for key, value in record.items():
                if key not in ['baalut', 'baalut_dt'] and value:
                    hebrew_key = translate_ownership_field(key)
                    additional_info.append(f"  • {hebrew_key}: {value}")
            
            if additional_info:
                info_text += "\n".join(additional_info) + "\n"
    
    return info_text

def format_ownership_date(date_str):
    """
    מעצב תאריך בעלות מפורמט YYYYMM לחודש/שנה
    
    Args:
        date_str: מחרוזת או מספר תאריך בפורמט YYYYMM
    
    Returns:
        תאריך מעוצב או מחרוזת ריקה אם הפורמט לא תקין
    """
    if not date_str:
        return ""
    
    # המרה למחרוזת אם צריך
    date_str = str(date_str)
    
    # בדיקת אורך
    if len(date_str) != 6:
        return date_str
    
    try:
        year = date_str[:4]
        month = date_str[4:]
        
        # מיפוי מספרי חודשים לשמות בעברית
        months = {
            "01": "ינואר",
            "02": "פברואר",
            "03": "מרץ",
            "04": "אפריל",
            "05": "מאי",
            "06": "יוני",
            "07": "יולי",
            "08": "אוגוסט",
            "09": "ספטמבר",
            "10": "אוקטובר",
            "11": "נובמבר",
            "12": "דצמבר"
        }
        
        month_name = months.get(month, month)
        return f"{month_name} {year}"
    except:
        return date_str

def translate_ownership_field(field_name):
    """
    מתרגם שמות שדות של בעלות לעברית
    
    Args:
        field_name: שם השדה באנגלית
        
    Returns:
        שם השדה בעברית או המקורי אם אין תרגום
    """
    translations = {
        'mispar_rechev': 'מספר רכב',
        'baalut': 'סוג בעלות',
        'baalut_dt': 'תאריך בעלות',
        'baal_cd': 'קוד בעל',
        'baal_shem': 'שם בעל',
        'ir_baal': 'עיר בעל',
        'ezor_baal': 'אזור בעל',
        'mikud_baal': 'מיקוד בעל',
        'taarich_rishum': 'תאריך רישום',
        'siba_shikul': 'סיבת שינוי',
        'makor_netunim': 'מקור נתונים'
    }
    
    return translations.get(field_name, field_name)