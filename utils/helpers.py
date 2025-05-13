import random
import os

def send_loading_sticker(bot, chat_id, stickers_list):
    """
    שולח סטיקר טעינה אקראי
    
    Args:
        bot: מופע הבוט
        chat_id: מזהה הצ'אט
        stickers_list: רשימת סטיקרים אפשריים
    
    Returns:
        הודעת הסטיקר שנשלחה
    """
    return bot.send_sticker(chat_id, random.choice(stickers_list))

def clean_temp_files(file_path):
    """
    מנקה קבצים זמניים
    
    Args:
        file_path: נתיב הקובץ למחיקה
    """
    try:
        os.remove(file_path)
    except Exception as e:
        print(f"שגיאה בניקוי קובץ זמני: {e}")

def clean_plate_number(text):
    """
    מנקה מספר לוחית רישוי - מסיר כל תו שאינו ספרה
    
    Args:
        text: טקסט המספר
    
    Returns:
        מספר נקי מתווים שאינם ספרות
    """
    return ''.join(filter(str.isdigit, text))