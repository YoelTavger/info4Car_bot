from utils.stickers import LICENSE_PLATE_STICKERS
from utils.helpers import send_loading_sticker, clean_plate_number
from services.vehicle.vehicle_service import VehicleService
from display.vehicle_info_formatter import format_vehicle_info
from display.response_messages import get_no_vehicle_data_message

# יצירת שירות רכב
vehicle_service = VehicleService()

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
        vehicle_data = vehicle_service.get_vehicle_complete(plate_number)
        
        # טיפול בתוצאות ושליחת ההודעה המתאימה
        result_message = None
        if not vehicle_data:
            # אם אין מידע, שליחת הודעת שגיאה
            error_message = get_no_vehicle_data_message(plate_number)
            result_message = bot.reply_to(message, error_message)
        else:
            # בניית הודעה עם פרטי הרכב
            vehicle_info = vehicle_data[0]  # לקיחת הרשומה הראשונה
            info_text = format_vehicle_info(vehicle_info, plate_number)
            
            # שליחת המידע בתגובה
            result_message = bot.reply_to(message, info_text, parse_mode="Markdown")
        
        # מחיקת סטיקר הטעינה אחרי שליחת ההודעה
        if result_message:
            try:
                bot.delete_message(message.chat.id, loading_sticker.message_id)
            except Exception as e:
                print(f"שגיאה במחיקת סטיקר טעינה: {e}")