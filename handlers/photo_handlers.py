import os
import telebot
from utils.stickers import PHOTO_STICKERS, LICENSE_PLATE_STICKERS
from utils.helpers import send_loading_sticker, clean_temp_files
from services.ocr.ocr_service import OCRService
from services.vehicle.vehicle_service import VehicleService
from display.vehicle_info_formatter import format_vehicle_info
from display.response_messages import (
    get_no_plate_detected_message,
    get_plate_detected_message,
    get_multiple_plates_detected_message,
    get_no_vehicle_data_message
)

# יצירת שירות OCR
ocr_service = OCRService()
vehicle_service = VehicleService()

def register_photo_handlers(bot):
    """
    רושם את כל הטיפולים בתמונות
    
    Args:
        bot: מופע הבוט
    """
    @bot.message_handler(content_types=['photo'])
    def handle_photo(message):
        """מטפל בתמונות שנשלחות לבוט"""
        # מציג "מקליד..." לפני התגובה
        bot.send_chat_action(message.chat.id, "typing")
        
        # הורדת התמונה
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # שמירת התמונה באופן זמני
        photo_path = f"temp_{message.chat.id}.jpg"
        with open(photo_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        # שליחת סטיקר כהודעת טעינה
        loading_sticker = send_loading_sticker(bot, message.chat.id, PHOTO_STICKERS)
        
        # זיהוי לוחית רישוי באמצעות שירות ה-OCR
        with open(photo_path, 'rb') as image_file:
            result = ocr_service.recognize_plate(image_file)
            plate_result = ocr_service.extract_ocr_results(result)
        
        # טיפול בתוצאות ושליחת ההודעה המתאימה
        result_message = None
        if not plate_result or 'full_plates' not in plate_result or not plate_result['full_plates']:
            result_message = bot.reply_to(message, get_no_plate_detected_message())
        elif len(plate_result['full_plates']) == 1:
            plate_number = plate_result['full_plates'][0]
            # יצירת כפתור אינליין לקבלת מידע על הרכב
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(
                text="קבל מידע על הרכב 🔍", 
                callback_data=f"info_{plate_number}"
            ))
            result_message = bot.reply_to(
                message, 
                get_plate_detected_message(plate_number), 
                reply_markup=markup
            )
        else:
            # זוהו מספר לוחיות - יצירת מקלדת אינליין
            markup = telebot.types.InlineKeyboardMarkup()
            for plate in plate_result['full_plates']:
                markup.add(telebot.types.InlineKeyboardButton(text=plate, callback_data=f"plate_{plate}"))
            
            result_message = bot.reply_to(message, get_multiple_plates_detected_message(), reply_markup=markup)
        
        # מחיקת סטיקר הטעינה רק אחרי שליחת ההודעה
        if result_message:
            try:
                bot.delete_message(message.chat.id, loading_sticker.message_id)
            except Exception as e:
                print(f"שגיאה במחיקת סטיקר טעינה: {e}")
        
        # ניקוי התמונה הזמנית
        clean_temp_files(photo_path)