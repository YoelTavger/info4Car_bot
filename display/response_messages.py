# הודעות סטנדרטיות לשימוש בבוט

def get_welcome_message(user_first_name):
    """
    מחזיר את הודעת הפתיחה לפי שם המשתמש
    
    Args:
        user_first_name: שם המשתמש
        
    Returns:
        טקסט הודעת הפתיחה
    """
    return f"""היי {user_first_name}! 👋

בוט המידע לרכבים מאפשר לך לקבל מידע על רכבים בישראל 🚗

פשוט:
- שלח מספר רכב (12345678)
- או שלח תמונה של לוחית רישוי

המאגר כולל רכבים פרטיים משנת 96' ומעלה ורכבים מסחריים קלים משנת 98'.

נסה עכשיו! 👇"""

def get_no_plate_detected_message():
    """
    מחזיר הודעת שגיאה כאשר לא זוהה מספר רכב בתמונה
    
    Returns:
        טקסט הודעת השגיאה
    """
    return "לא זוהה מספר רכב בתמונה ❌"

def get_plate_detected_message(plate_number):
    """
    מחזיר הודעה כאשר זוהה מספר רכב
    
    Args:
        plate_number: מספר הרכב שזוהה
        
    Returns:
        טקסט ההודעה
    """
    return f"מספר הרכב שזוהה: {plate_number} ✅"

def get_multiple_plates_detected_message():
    """
    מחזיר הודעה כאשר זוהו מספר לוחיות רישוי
    
    Returns:
        טקסט ההודעה
    """
    return "זוהו מספר לוחיות רישוי 🔢\nאנא בחר את המספר הרצוי:"

def get_plate_selected_message(selected_plate):
    """
    מחזיר הודעה כאשר נבחר מספר רכב מתוך מספר אפשרויות
    
    Args:
        selected_plate: מספר הרכב שנבחר
        
    Returns:
        טקסט ההודעה
    """
    return f"נבחר מספר רכב: {selected_plate} ✅"

def get_no_vehicle_data_message(plate_number):
    """
    מחזיר הודעה כאשר לא נמצא מידע על רכב
    
    Args:
        plate_number: מספר הרכב שחיפשו
        
    Returns:
        טקסט הודעת השגיאה
    """
    return f"לא נמצא מידע עבור רכב מספר {plate_number} ❌"

def get_default_text_message():
    """
    מחזיר הודעה כללית למשתמש שלא הזין מספר רכב תקין
    
    Returns:
        טקסט ההודעה
    """
    return "שלח מספר רכב או תמונה של לוחית רישוי כדי לקבל מידע 🔍"