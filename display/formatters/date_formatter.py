def format_date(date_str):
    """
    מעצב תאריך לפורמט DD-MM-YYYY
    
    Args:
        date_str: מחרוזת או ערך התאריך המקורי
        
    Returns:
        תאריך מעוצב או המחרוזת המקורית אם אי אפשר לעצב
    """
    if not date_str:
        return date_str
    
    # המרה למחרוזת אם צריך
    date_str = str(date_str)
    
    # הסרת שעה אם קיימת
    date_parts = date_str.split()
    date_only = date_parts[0] if date_parts else date_str
    
    # ניסיון לעצב לפי פורמטים שונים
    try:
        # אם הפורמט כבר DD-MM-YYYY
        if len(date_only.split('-')) == 3 and not date_only.startswith(('19', '20')):
            return date_only
        
        # אם הפורמט YYYY-MM-DD
        if date_only.startswith(('19', '20')) and len(date_only.split('-')) == 3:
            parts = date_only.split('-')
            if len(parts) == 3:
                day = parts[2].split()[0]  # מסיר את השעה אם קיימת
                return f"{day}-{parts[1]}-{parts[0]}"
        
        # אם הפורמט הוא YYYYMMDD
        if len(date_only) == 8 and date_only.isdigit():
            return f"{date_only[6:8]}-{date_only[4:6]}-{date_only[0:4]}"
            
    except Exception:
        pass
    
    # החזרת המחרוזת המקורית אם לא ניתן לעצב
    return date_only

def format_road_date(road_date):
    """
    מעצב תאריך עלייה לכביש בפורמט חודש בעברית ושנה
    
    Args:
        road_date: תאריך עלייה לכביש בפורמט YYYY-M
        
    Returns:
        תאריך מעוצב או המחרוזת המקורית אם אי אפשר לעצב
    """
    if not road_date:
        return road_date
    
    # המרה למחרוזת אם צריך
    road_date = str(road_date)
    
    try:
        # אם בפורמט YYYY-M או YYYY-MM
        if '-' in road_date:
            parts = road_date.split('-')
            if len(parts) == 2:
                year = parts[0]
                month_num = int(parts[1])
                
                # מיפוי מספרי חודשים לשמות בעברית
                months = {
                    1: "ינואר",
                    2: "פברואר",
                    3: "מרץ",
                    4: "אפריל",
                    5: "מאי",
                    6: "יוני",
                    7: "יולי",
                    8: "אוגוסט",
                    9: "ספטמבר",
                    10: "אוקטובר",
                    11: "נובמבר",
                    12: "דצמבר"
                }
                
                month_name = months.get(month_num, str(month_num))
                return f"{month_name} {year}"
    except Exception:
        pass
    
    # החזרת המחרוזת המקורית אם לא ניתן לעצב
    return road_date