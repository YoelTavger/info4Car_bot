import telebot
from services.vehicle.vehicle_service import get_vehicle_complete
from utils.stickers import LICENSE_PLATE_STICKERS
from utils.helpers import send_loading_sticker
from display.vehicle_info_formatter import format_vehicle_info
from display.response_messages import get_plate_selected_message, get_no_vehicle_data_message

def register_callback_handlers(bot):
    """
    רושם את כל הטיפולים בקריאות callback
    
    Args:
        bot: מופע הבוט
    """
    @bot.callback_query_handler(func=lambda call: call.data.startswith('plate_'))
    def handle_plate_selection(call):
        """מטפל בבחירת לוחית רישוי מהמקלדת"""
        # חילוץ מספר הלוחית שנבחרה
        selected_plate = call.data.replace("plate_", "")
        
        # אישור קבלת הקריאה עם סמן טעינה
        bot.answer_callback_query(
            callback_query_id=call.id,
            text="מחפש מידע... ⏳"
        )
        
        # הצג פעולת טעינה בצ'אט
        bot.send_chat_action(call.message.chat.id, "typing")
        
        # שליחת סטיקר טעינה
        loading_sticker = send_loading_sticker(bot, call.message.chat.id, LICENSE_PLATE_STICKERS)
        
        # קבלת מידע על הרכב ישירות (במקום להציג כפתור)
        handle_vehicle_info_direct(bot, call.message.chat.id, call.message.message_id, selected_plate, loading_sticker)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('info_'))
    def handle_vehicle_info(call):
        """מטפל בבקשה לקבלת מידע על רכב"""
        # חילוץ מספר הרכב
        license_plate = call.data.replace("info_", "")
        
        # אישור קבלת הקריאה עם סמן טעינה
        bot.answer_callback_query(
            callback_query_id=call.id,
            text="מחפש מידע... ⏳"
        )
        
        # הצג פעולת טעינה בצ'אט
        bot.send_chat_action(call.message.chat.id, "typing")
        
        # שליחת סטיקר טעינה
        loading_sticker = send_loading_sticker(bot, call.message.chat.id, LICENSE_PLATE_STICKERS)
        
        # קבלת מידע על הרכב
        handle_vehicle_info_direct(bot, call.message.chat.id, call.message.message_id, license_plate, loading_sticker)

def handle_vehicle_info_direct(bot, chat_id, message_id, license_plate, loading_sticker):
    # קבלת מידע מורחב על הרכב מה-API
    vehicle_data = get_vehicle_complete(license_plate)
    
    # הכנת התוכן לעדכון ההודעה
    if not vehicle_data:
        # אם אין מידע, עדכון ההודעה עם הודעת שגיאה
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=get_no_vehicle_data_message(license_plate),
            reply_markup=None
        )
    else:
        # בניית הודעה עם פרטי הרכב
        vehicle_info = vehicle_data[0]  # לקיחת הרשומה הראשונה
        info_text = format_vehicle_info(vehicle_info, license_plate)
        
        # הדפסת אורך הטקסט לבדיקה
        # print(f"אורך הטקסט: {len(info_text)} בתים")
        
        # פיצול הודעה אם ארוכה מדי
        MAX_LENGTH = 4000  # אורך מקסימלי להודעת טלגרם
        
        if len(info_text) > MAX_LENGTH:
            # שליחת הודעה חדשה במקום עדכון
            bot.delete_message(chat_id, message_id)
            
            # פיצול הטקסט לחלקים
            parts = []
            current_part = ""
            
            for line in info_text.split('\n'):
                if len(current_part) + len(line) + 1 > MAX_LENGTH:
                    parts.append(current_part)
                    current_part = line
                else:
                    if current_part:
                        current_part += '\n' + line
                    else:
                        current_part = line
            
            if current_part:
                parts.append(current_part)
            
            # שליחת החלקים
            for i, part in enumerate(parts):
                if i == 0:
                    bot.send_message(
                        chat_id=chat_id,
                        text=part,
                        parse_mode="Markdown"
                    )
                else:
                    bot.send_message(
                        chat_id=chat_id,
                        text=f"(המשך) {part}",
                        parse_mode="Markdown"
                    )
        else:
            # עדכון ההודעה עם המידע
            try:
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=info_text,
                    parse_mode="Markdown"
                )
            except Exception as e:
                print(f"שגיאה בעדכון הודעה: {e}")
                # ניסיון שני - שליחת הודעה חדשה במקום עדכון
                try:
                    bot.delete_message(chat_id, message_id)
                    bot.send_message(
                        chat_id=chat_id,
                        text=info_text,
                        parse_mode="Markdown"
                    )
                except Exception as e2:
                    print(f"שגיאה גם בשליחת הודעה חדשה: {e2}")
                    # ניסיון אחרון - ללא Markdown
                    bot.send_message(
                        chat_id=chat_id,
                        text="שגיאה בעיצוב ההודעה. הנה המידע ללא עיצוב:\n\n" + info_text.replace('*', ''),
                        parse_mode=None
                    )
    
    # מחיקת סטיקר הטעינה אחרי שליחת התשובה
    try:
        bot.delete_message(chat_id, loading_sticker.message_id)
    except Exception as e:
        print(f"שגיאה במחיקת סטיקר טעינה: {e}")