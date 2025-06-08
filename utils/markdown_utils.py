import re

def safe_markdown_escape(text):
    """
    בריחה בטוחה מתווי Markdown עם הגנה נוספת
    
    Args:
        text: הטקסט לבריחה
        
    Returns:
        טקסט בטוח לשליחה בטלגרם
    """
    if not text:
        return text
    
    # המרה למחרוזת
    text = str(text)
    
    # הסרת תווי בקרה ותווים לא חוקיים
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
    
    # החלפת תווים מיוחדים ב-Markdown MarkdownV2
    special_chars = [
        '_', '*', '[', ']', '(', ')', '~', '`', '>', '#', 
        '+', '-', '=', '|', '{', '}', '.', '!'
    ]
    
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    
    return text

def validate_markdown_message(text):
    """
    בודק אם הודעת Markdown תקינה
    
    Args:
        text: הטקסט לבדיקה
        
    Returns:
        tuple: (is_valid, cleaned_text)
    """
    if not text:
        return True, text
    
    try:
        # בדיקת איזון של תגי *
        asterisk_count = text.count('*') - text.count('\\*')
        if asterisk_count % 2 != 0:
            # מספר לא זוגי של כוכביות - הוסף אחת או הסר
            text = text + '*' if asterisk_count % 2 == 1 else text
        
        # בדיקת איזון של תגי _
        underscore_count = text.count('_') - text.count('\\_')
        if underscore_count % 2 != 0:
            text = text + '_' if underscore_count % 2 == 1 else text
        
        # בדיקת סוגריים
        open_brackets = text.count('[') - text.count('\\[')
        close_brackets = text.count(']') - text.count('\\]')
        if open_brackets != close_brackets:
            # תיקון חוסר איזון
            diff = abs(open_brackets - close_brackets)
            if open_brackets > close_brackets:
                text += ']' * diff
            else:
                text += '[' * diff
        
        return True, text
    except Exception:
        # אם יש בעיה, החזר גרסה ללא Markdown
        cleaned_text = remove_all_markdown(text)
        return False, cleaned_text

def remove_all_markdown(text):
    """
    מסיר את כל תגי ה-Markdown מהטקסט
    
    Args:
        text: הטקסט המקורי
        
    Returns:
        טקסט ללא Markdown
    """
    if not text:
        return text
    
    # הסרת תגי בריחה
    text = re.sub(r'\\(.)', r'\1', text)
    
    # הסרת תגי bold ו-italic
    text = re.sub(r'\*([^*]*)\*', r'\1', text)
    text = re.sub(r'_([^_]*)_', r'\1', text)
    
    # הסרת קישורים
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)
    
    # הסרת תגים נוספים
    text = re.sub(r'`([^`]*)`', r'\1', text)
    text = re.sub(r'~([^~]*)~', r'\1', text)
    
    return text

def safe_format_field(field_name, field_value, escape_value=True):
    """
    מעצב שדה בצורה בטוחה
    
    Args:
        field_name: שם השדה
        field_value: ערך השדה
        escape_value: האם לבצע escape לערך
        
    Returns:
        שדה מעוצב בצורה בטוחה
    """
    if field_value is None:
        field_value = "לא ידוע"
    
    # ניקוי שם השדה
    safe_field_name = safe_markdown_escape(str(field_name))
    
    # ניקוי ערך השדה
    if escape_value:
        safe_field_value = safe_markdown_escape(str(field_value))
    else:
        safe_field_value = str(field_value)
    
    return f"*{safe_field_name}:* {safe_field_value}"

def split_long_message(text, max_length=4000):
    """
    מפצל הודעה ארוכה לחלקים תוך שמירה על תקינות Markdown
    
    Args:
        text: הטקסט לפיצול
        max_length: אורך מקסימלי לכל חלק
        
    Returns:
        רשימה של חלקים
    """
    if len(text) <= max_length:
        return [text]
    
    parts = []
    current_part = ""
    
    # פיצול לפי שורות
    lines = text.split('\n')
    
    for line in lines:
        # בדיקה אם הוספת השורה תחרוג מהמגבלה
        if len(current_part) + len(line) + 1 > max_length:
            # סיים את החלק הנוכחי
            if current_part:
                # וודא שהחלק תקין מבחינת Markdown
                is_valid, cleaned_part = validate_markdown_message(current_part)
                parts.append(cleaned_part)
                current_part = ""
            
            # אם השורה עצמה ארוכה מדי
            if len(line) > max_length:
                # חתוך אותה לחלקים קטנים יותר
                for i in range(0, len(line), max_length):
                    part = line[i:i + max_length]
                    is_valid, cleaned_part = validate_markdown_message(part)
                    parts.append(cleaned_part)
            else:
                current_part = line
        else:
            # הוסף את השורה לחלק הנוכחי
            if current_part:
                current_part += '\n' + line
            else:
                current_part = line
    
    # הוסף את החלק האחרון
    if current_part:
        is_valid, cleaned_part = validate_markdown_message(current_part)
        parts.append(cleaned_part)
    
    return parts