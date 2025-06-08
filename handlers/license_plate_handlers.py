import telebot
import random
import re
from utils.stickers import LICENSE_PLATE_STICKERS
from utils.helpers import send_loading_sticker, clean_plate_number
from services.vehicle.vehicle_service import get_vehicle_complete
from display.vehicle_info_formatter import format_vehicle_info
from display.response_messages import get_no_vehicle_data_message

def clean_markdown_text(text):
    """מנקה טקסט מבעיות Markdown"""
    if not text:
        return text
    
    # הסרת תווי בקרה
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
    
    # בדיקת איזון כוכביות
    asterisk_count = text.count('*')
    if asterisk_count % 2 != 0:
        text += '*'
    
    # בדיקת איזון קווים תחתונים
    underscore_count = text.count('_')
    if underscore_count % 2 != 0:
        text += '_'
    
    return text

def safe_reply_to(bot, message, text, reply_markup=None):
    """שולח תגובה בצורה בטוחה"""
    try:
        # ניסיון ראשון עם Markdown
        cleaned_text = clean_markdown_text(text)
        return bot.reply_to(message, cleaned_text, parse_mode="Markdown", reply_markup=reply_markup)
    except Exception as e:
        print(f"שגיאה עם Markdown: {e}")
        try:
            # ניסיון שני ללא Markdown
            plain_text = re.sub(r'\*([^*]*)\*', r'\1', text)
            plain_text = re.sub(r'_([^_]*)_', r'\1', plain_text)
            return bot.reply_to(message, plain_text, reply_markup=reply_markup)
        except Exception as e2:
            print(f"שגיאה גם ללא Markdown: {e2}")
            return bot.reply_to(message, "שגיאה בהצגת המידע. אנא נסה שוב.", reply_markup=reply_markup)

def register_license_plate_handlers(bot):
    """
    רושם את כל הטיפולים בהודעות טקסט המכילות מספרי רכב
    
    Args:
        bot: מופע הבוט
    """
    
    @bot.message_handler(regexp=r'^\d{6}$')
    @bot.message_handler(regexp=r'^\d{7,8}$')
    @bot.message_handler(regexp=r'^\d{2,3}-\d{2,3}-\d{2}$')
    @bot.message_handler(regexp=r'^\d{3}-\d{2}-\d{3}$')
    def handle_license_plate_direct(message):
        """מטפל בהודעות טקסט המכילות רק מספר רכב"""
        # מציג "מקליד..." לפני התגובה
        bot.send_chat_action(message.chat.id, "typing")
        
        # ניקוי מספר הרכב - מסיר כל תו שאינו ספרה
        plate_number = clean_plate_number(message.text)
        
        # שליחת סטיקר כהודעת טעינה
        loading_sticker = send_loading_sticker(bot, message.chat.id, LICENSE_PLATE_STICKERS)
        
        # קבלת מידע מורחב על הרכב
        vehicle_data = get_vehicle_complete(plate_number)
        
        # טיפול בתוצאות ושליחת ההודעה המתאימה
        result_message = None
        if not vehicle_data:
            # אם אין מידע, שליחת הודעת שגיאה
            error_message = get_no_vehicle_data_message(plate_number)
            result_message = bot.reply_to(message, error_message)
        else:
            # בניית הודעה עם פרטי הרכב - תמיד תצוגה מפורטת
            vehicle_info = vehicle_data[0]  # לקיחת הרשומה הראשונה
            info_text = format_vehicle_info(vehicle_info, plate_number, show_all_fields=True)
            
            # שליחת המידע בתגובה בצורה בטוחה (ללא כפתורים)
            result_message = safe_reply_to(bot, message, info_text)
        
        # מחיקת סטיקר הטעינה אחרי שליחת ההודעה
        if result_message:
            try:
                bot.delete_message(message.chat.id, loading_sticker.message_id)
            except Exception as e:
                print(f"שגיאה במחיקת סטיקר טעינה: {e}")