import telebot
import re
from services.vehicle.vehicle_service import get_vehicle_complete
from utils.stickers import LICENSE_PLATE_STICKERS
from utils.helpers import send_loading_sticker
from display.vehicle_info_formatter import format_vehicle_info
from display.response_messages import get_plate_selected_message, get_no_vehicle_data_message

def clean_markdown_text(text):
    """
    מנקה טקסט מבעיות Markdown בצורה יסודית יותר
    """
    if not text:
        return text
    
    import re
    
    # הסרת תווי בקרה ותווים לא חוקיים
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
    
    # החלפת תווים בעייתיים
    text = text.replace('\\', '\\\\')
    
    # ספירת כוכביות ותיקון
    asterisk_positions = []
    i = 0
    while i < len(text):
        if text[i] == '*' and (i == 0 or text[i-1] != '\\'):
            asterisk_positions.append(i)
        i += 1
    
    # אם מספר הכוכביות אי-זוגי, הוסף כוכבית בסוף
    if len(asterisk_positions) % 2 != 0:
        text += '*'
    
    # טיפול דומה בקווים תחתונים
    underscore_positions = []
    i = 0
    while i < len(text):
        if text[i] == '_' and (i == 0 or text[i-1] != '\\'):
            underscore_positions.append(i)
        i += 1
    
    if len(underscore_positions) % 2 != 0:
        text += '_'
    
    # בדיקת סוגריים מרובעים
    open_brackets = text.count('[') - text.count('\\[')
    close_brackets = text.count(']') - text.count('\\]')
    if open_brackets != close_brackets:
        diff = abs(open_brackets - close_brackets)
        if open_brackets > close_brackets:
            text += ']' * diff
        else:
            text += '[' * diff
    
    return text

def remove_all_markdown(text):
    """
    מסיר לחלוטין את כל ה-Markdown מהטקסט
    """
    if not text:
        return text
    
    import re
    
    # הסרת כל תגי bold
    text = re.sub(r'\*([^*]*)\*', r'\1', text)
    text = re.sub(r'\*', '', text)  # הסרת כוכביות בודדות
    
    # הסרת כל תגי italic
    text = re.sub(r'_([^_]*)_', r'\1', text)
    text = re.sub(r'_', '', text)  # הסרת קווים תחתונים בודדים
    
    # הסרת תגים נוספים
    text = re.sub(r'`([^`]*)`', r'\1', text)
    text = re.sub(r'~([^~]*)~', r'\1', text)
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)
    
    # הסרת תווי escape
    text = re.sub(r'\\(.)', r'\1', text)
    
    return text

def send_safe_message(bot, chat_id, text, reply_markup=None, reply_to_message_id=None):
    """
    שולח הודעה בצורה בטוחה - ללא Markdown כברירת מחדל
    """
    # ניסיון ראשון: ללא Markdown כלל (הבטוח ביותר)
    try:
        plain_text = remove_all_markdown(text)
        if reply_to_message_id:
            return bot.reply_to(
                reply_to_message_id, 
                plain_text, 
                reply_markup=reply_markup
            )
        else:
            return bot.send_message(
                chat_id, 
                plain_text, 
                reply_markup=reply_markup
            )
    except Exception as e:
        print(f"ניסיון ללא Markdown נכשל: {e}")
    
    # ניסיון 2: טקסט בסיסי בלבד
    try:
        basic_text = f"מידע על רכב התקבל אך יש בעיה בהצגה.\nאנא נסה שוב או השתמש בתצוגה מפורטת."
        if reply_to_message_id:
            return bot.reply_to(reply_to_message_id, basic_text, reply_markup=reply_markup)
        else:
            return bot.send_message(chat_id, basic_text, reply_markup=reply_markup)
    except Exception as e:
        print(f"ניסיון טקסט בסיסי נכשל: {e}")
        return None

def safe_edit_message(bot, chat_id, message_id, text, reply_markup=None):
    """
    עורך הודעה בצורה בטוחה - ללא Markdown כברירת מחדל
    """
    # ניסיון ראשון: עדכון ללא Markdown
    try:
        plain_text = remove_all_markdown(text)
        return bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=plain_text,
            reply_markup=reply_markup
        )
    except Exception as e:
        print(f"ניסיון עדכון ללא Markdown נכשל: {e}")
    
    # ניסיון 2: מחיקה ושליחת הודעה חדשה
    try:
        bot.delete_message(chat_id, message_id)
        return send_safe_message(bot, chat_id, text, reply_markup)
    except Exception as e:
        print(f"ניסיון מחיקה ושליחה חדשה נכשל: {e}")
        return None

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
        
        # קבלת מידע על הרכב ישירות
        handle_vehicle_info_direct(bot, call.message.chat.id, call.message.message_id, selected_plate, loading_sticker)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('info_'))
    def handle_vehicle_info(call):
        """מטפל בבקשה לקבלת מידע על רכב - תמיד תצוגה מפורטת"""
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
    """מטפל בהצגת מידע רכב בצורה ישירה - תמיד תצוגה מפורטת"""
    # קבלת מידע מורחב על הרכב
    vehicle_data = get_vehicle_complete(license_plate)
    
    if not vehicle_data:
        # אם אין מידע, עדכון ההודעה עם הודעת שגיאה
        safe_edit_message(
            bot, 
            chat_id, 
            message_id,
            get_no_vehicle_data_message(license_plate)
        )
    else:
        # בניית הודעה עם פרטי הרכב - תמיד תצוגה מפורטת
        vehicle_info = vehicle_data[0]
        info_text = format_vehicle_info(vehicle_info, license_plate, show_all_fields=True)
        
        # בדיקת אורך ההודעה
        MAX_LENGTH = 4000
        
        if len(info_text) > MAX_LENGTH:
            # מחיקת ההודעה הקיימת
            try:
                bot.delete_message(chat_id, message_id)
            except:
                pass
            
            # פיצול הטקסט לחלקים
            parts = []
            current_part = ""
            
            for line in info_text.split('\n'):
                if len(current_part) + len(line) + 1 > MAX_LENGTH:
                    if current_part:
                        parts.append(current_part)
                        current_part = line
                    else:
                        # שורה ארוכה מדי - חתוך אותה
                        parts.append(line[:MAX_LENGTH])
                        current_part = line[MAX_LENGTH:]
                else:
                    if current_part:
                        current_part += '\n' + line
                    else:
                        current_part = line
            
            if current_part:
                parts.append(current_part)
            
            # שליחת החלקים
            for i, part in enumerate(parts):
                send_safe_message(
                    bot, 
                    chat_id, 
                    f"(חלק {i+1}) {part}" if i > 0 else part
                )
        else:
            # עדכון ההודעה
            safe_edit_message(
                bot, 
                chat_id, 
                message_id,
                info_text
            )
    
    # מחיקת סטיקר הטעינה
    try:
        bot.delete_message(chat_id, loading_sticker.message_id)
    except Exception as e:
        print(f"שגיאה במחיקת סטיקר טעינה: {e}")