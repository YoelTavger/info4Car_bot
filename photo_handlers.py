import telebot
from ocr_service import OCRService
import os
import vehicle_service
import random

ocr_service = OCRService()

def register_photo(bot):

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
        sticker_ids = [
            "CAACAgIAAxkBAAEOdkRoIgvpc4P3QzgI3yaRgbt0nsAQ9wAC-BIAAlo16Uhs4hFMpJkFTjYE",
            "CAACAgIAAxkBAAEOdktoIgyYCo0zN0xajTvyeNongDA4xwACVQADr8ZRGmTn_PAl6RC_NgQ",
            "CAACAgIAAxkBAAEOdlloIgyx5b4QE7fkXXg38g72OixomwACJQ8AAkuTkUjrHBy-H6OZCjYE",
            "CAACAgIAAxkBAAEOdwhoIly1GVZ87f4ytQABoNRh5qWq8KkAAmcLAAJFsfFKYW0imca0hI02BA",
            "CAACAgIAAxkBAAEOdwpoIlzP5lFtcAyQwjdMTJO_JVuhqAACogEAAladvQpBnnI7eRH13TYE",
            "CAACAgIAAxkBAAEOdwxoIlzj1wABipiEOpekBr7MDLvF1-kAAtgAA6tXxAsSurtX4BbuKTYE",
            "CAACAgIAAxkBAAEOdxFoIlz7oZfMfBNApuLwbyc52oWxgwACmxAAAprSKEqaRjN_uTLIETYE",
            "CAACAgIAAxkBAAEOdxNoIl0FpQZpW_16wvzN9egq96tk3gAC-CEAArKhMEptBVGAop7OozYE",
            "CAACAgIAAxkBAAEOdxloIl1gu9rFrTgpGdqqI5B53vQWQQACdAAD2bxqGtx1qD4BXPEkNgQ",
            "CAACAgIAAxkBAAEOdxtoIl2vHYNZU_gt1bbBaclmxLeUdwAC3RIAAsngQUrQNf4Mt1ehCDYE",
            "CAACAgIAAxkBAAEOdyNoIl7fKCxzx0P7Di5A-nposZ1qwgACJS0AApDSgEuMX-VjddzZFjYE",
            "CAACAgIAAxkBAAEOdyVoIl7pAomvTpXCvA9wLBWxLAFvDgACX1UAAk4YUUiwAe6ltVD-BTYE",
            "CAACAgEAAxkBAAEOdz1oImD-UlAp_eTxZ_F7uMv73ii7jgACxQIAAkeAGUTTk7G7rIZ7GjYE",
            "CAACAgIAAxkBAAEOd0VoImHMSKBgCHmfE2lXXXD3gd8O6QACFgkAAowt_QfAndcgnWZVfTYE",
            "CAACAgIAAxkBAAEOd0doImJL2t-RZhuNrmgJDlqJZ3jsqAACmw4AAhJp0UjTJWW13JUuJzYE",
            "CAACAgEAAxkBAAEOd1FoImPCFdff9GhS_qyQX86QmptOKAAC7QIAAivCCEfCfaoWAaqnZTYE",
            "CAACAgIAAxkBAAEOd1NoImP0_GcOff4Rsu2QN7t0n5RuQQACeQ0AAoAfYEhV0H5JoN5_JDYE",
            "CAACAgIAAxkBAAEOd1VoImQGBIQ-ijaYE5SHFSBwJ6Og3QACMwADDbbSGUVhcOyd4UGCNgQ",
            "CAACAgIAAxkBAAEOd1doImQ9jGBvBhaxx-iPIA8B6Jur-AACIwADfoTDCB9Wh2bqIorCNgQ",
        ]
        
        loading_sticker = bot.send_sticker(message.chat.id, random.choice(sticker_ids))
        
        # זיהוי לוחית רישוי באמצעות שירות ה-OCR
        with open(photo_path, 'rb') as image_file:
            result = ocr_service.recognize_plate(image_file)
            plate_result = ocr_service.extract_ocr_results(result)
        
        # טיפול בתוצאות ושליחת ההודעה המתאימה
        result_message = None
        if not plate_result or 'full_plates' not in plate_result or not plate_result['full_plates']:
            result_message = bot.reply_to(message, "לא זוהה מספר רכב בתמונה ❌")
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
                f"מספר הרכב שזוהה: {plate_number} ✅", 
                reply_markup=markup
            )
        else:
            # זוהו מספר לוחיות - יצירת מקלדת אינליין
            markup = telebot.types.InlineKeyboardMarkup()
            for plate in plate_result['full_plates']:
                markup.add(telebot.types.InlineKeyboardButton(text=plate, callback_data=f"plate_{plate}"))
            
            result_message = bot.reply_to(message, "זוהו מספר לוחיות רישוי 🔢\nאנא בחר את המספר הרצוי:", reply_markup=markup)
        
        # מחיקת סטיקר הטעינה רק אחרי שליחת ההודעה
        if result_message:
            try:
                bot.delete_message(message.chat.id, loading_sticker.message_id)
            except Exception as e:
                print(f"שגיאה במחיקת סטיקר טעינה: {e}")
        
        # ניקוי התמונה הזמנית
        try:
            os.remove(photo_path)
        except Exception as e:
            print(f"שגיאה בניקוי קובץ זמני: {e}")

    @bot.callback_query_handler(func=lambda call: call.data.startswith('plate_'))
    def handle_plate_selection(call):
        """מטפל בבחירת לוחית רישוי מהמקלדת"""
        # חילוץ מספר הלוחית שנבחרה
        selected_plate = call.data.replace("plate_", "")
        
        # יצירת כפתור אינליין לקבלת מידע על הרכב
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(
            text="קבל מידע על הרכב 🔍", 
            callback_data=f"info_{selected_plate}"
        ))
        
        # עדכון ההודעה הקיימת במקום שליחת הודעה חדשה
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"נבחר מספר רכב: {selected_plate} ✅",
            reply_markup=markup
        )
        
        # אישור קבלת הקריאה
        bot.answer_callback_query(callback_query_id=call.id)
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
        sticker_ids = [
            "CAACAgEAAxkBAAEOdx1oIl5SiRGr8MdaXGv-fFh1YvsqPgACtgIAAk8C2EawnAhyEryg3TYE",
            "CAACAgEAAxkBAAEOdx9oIl6OIPTprdkAAa3aKPmL0bvrlXcAAjkEAAJHpxlETlv1LldFLEQ2BA",
            "CAACAgIAAxkBAAEOdyFoIl6ancyVJ449DVytfUK0gwABcz4AAksCAAJWnb0KYlBF0FD6cZw2BA",
            "CAACAgIAAxkBAAEOdydoIl9n0aIp9BpkV_HAzt7zzr74AAPvDAAC18bxSnuZNkCo-dJnNgQ",
            "CAACAgIAAxkBAAEOdyloIl96w8VgzoEn7bjDnEFu5JoLkQAC0AkAAowt_Qc89_7kt1u7szYE",
            "CAACAgIAAxkBAAEOdytoIl-JMmXiJa2VXUqNKbkXu33WOQACTVQAAmH0SUq_8VQbtwOFgjYE",
            "CAACAgEAAxkBAAEOdy1oIl-0gFVAwCeR2_MRFnDnlTMBLgACIgMAAma-oUY566OY856vSzYE",
            "CAACAgIAAxkBAAEOdy9oIl_EUypB5oOBXVXZRmjebI3EdQACHxAAAnCswEgvF961dhIdtzYE",
            "CAACAgIAAxkBAAEOdzFoImA0UsGLzDbXuT0oBGiMplAFEwACwQoAAh5hoUpZi8YqzCzJ5TYE",
            "CAACAgIAAxkBAAEOdzNoImA76lh2h34tMPo9_x3KguxxgQACESEAAnLDQEhgZeBxMNdpAjYE",
            "CAACAgEAAxkBAAEOdzVoImCb-EnNOThpo01b8IfM9zHftAACkQMAAm61IUTQ2KZBkzXupDYE",
            "CAACAgEAAxkBAAEOdzdoImDWQhGLSXvMT6OTeoByQ1c-MgACmwIAApZrGEQBmK2R5D2DJDYE",
            "CAACAgEAAxkBAAEOdzloImDjGDcqGxuVygABDXuG3Bs9DAEAApQCAAKc1yFEBFvLkO-3UkI2BA",
            "CAACAgEAAxkBAAEOdztoImDsmebIHSmybyGLR_hHEFIBtgACrwIAAphXIUS8lNoZG4P3rDYE",
            "CAACAgEAAxkBAAEOdz9oImEdO2vRMQW-UNElDBPgtHGuhwACigIAApFJIEQVpamIL42sCjYE",
            "CAACAgIAAxkBAAEOd0FoImGwoaLkfhu-aIj7rYYvTnakeAACLAADJHFiGsUg5gPvePzkNgQ",
            "CAACAgIAAxkBAAEOd0NoImHBMI2upSMoD90Se0GlDm6s1QACMwkAAowt_QcRGmyAI0zRfDYE",
            "CAACAgIAAxkBAAEOd0loImJz1IGcI9GdedXMRC4_mVpxKgACYA4AArUZqUoDTvrWOrylSjYE",
            "CAACAgIAAxkBAAEOd0toImKIw4krtWxxj3fyjkd0LL7RhQACjgAD2bxqGtF8Ty-NE_o9NgQ",
            "CAACAgIAAxkBAAEOd01oImKPQQQkd9H2IM0Q_RdY9ddoswACkAAD2bxqGsrJpeQupLNWNgQ",
            "CAACAgIAAxkBAAEOd09oImLT3V_d5qruCY_CV2iiVaH-_gACmxAAAngZSEqihrOSUgjlqTYE",
        ]
        loading_sticker = bot.send_sticker(call.message.chat.id, random.choice(sticker_ids))
        
        # קבלת מידע מורחב על הרכב מה-API (משילוב שני המאגרים)
        vehicle_data = vehicle_service.get_vehicle_complete(license_plate)
        
        # הכנת התוכן לעדכון ההודעה
        if not vehicle_data:
            # אם אין מידע, עדכון ההודעה עם הודעת שגיאה
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"לא נמצא מידע עבור רכב מספר {license_plate} ❌",
                reply_markup=None
            )
            # מחיקת סטיקר הטעינה
            try:
                bot.delete_message(call.message.chat.id, loading_sticker.message_id)
            except Exception as e:
                print(f"שגיאה במחיקת סטיקר טעינה: {e}")
            return
            
        # בניית הודעה עם פרטי הרכב
        vehicle_info = vehicle_data[0]  # לקיחת הרשומה הראשונה
        
        # יצירת טקסט המידע עם כל השדות
        info_text = f"*מידע על רכב מספר {license_plate}* 🚗\n\n"
        
        # מספר רכב ומסגרת (מידע חשוב)
        info_text += f"*מספר רכב:* {vehicle_info.get('mispar_rechev', 'לא ידוע')}\n"
        info_text += f"*מספר שילדה:* {vehicle_info.get('misgeret', 'לא ידוע')}\n\n"
        
        # מידע על היצרן והדגם
        info_text += f"*יצרן:* {vehicle_info.get('tozeret_nm', 'לא ידוע')}"
        if vehicle_info.get('tozeret_cd'):
            info_text += f" (קוד: {vehicle_info.get('tozeret_cd')})"
        info_text += "\n"
        
        info_text += f"*דגם:* {vehicle_info.get('degem_nm', 'לא ידוע')}"
        if vehicle_info.get('degem_cd'):
            info_text += f" (קוד: {vehicle_info.get('degem_cd')})"
        info_text += "\n"
        
        if vehicle_info.get('sug_degem'):
            info_text += f"*סוג דגם:* {vehicle_info.get('sug_degem')}\n"
            
        if vehicle_info.get('kinuy_mishari'):
            info_text += f"*כינוי מסחרי:* {vehicle_info.get('kinuy_mishari')}\n"
            
        if vehicle_info.get('ramat_gimur'):
            info_text += f"*רמת גימור:* {vehicle_info.get('ramat_gimur')}\n"
            
        if vehicle_info.get('degem_manoa'):
            info_text += f"*דגם מנוע:* {vehicle_info.get('degem_manoa')}\n"
        
        info_text += "\n"
        
        # נתונים עיקריים
        info_text += f"*שנת ייצור:* {vehicle_info.get('shnat_yitzur', 'לא ידוע')}\n"
        
        if vehicle_info.get('moed_aliya_lakvish'):
            info_text += f"*מועד עלייה לכביש:* {vehicle_info.get('moed_aliya_lakvish')}\n"
            
        info_text += f"*סוג דלק:* {vehicle_info.get('sug_delek_nm', 'לא ידוע')}\n"
        
        # צבע הרכב
        info_text += f"*צבע:* {vehicle_info.get('tzeva_rechev', 'לא ידוע')}"
        if vehicle_info.get('tzeva_cd'):
            info_text += f" (קוד: {vehicle_info.get('tzeva_cd')})"
        info_text += "\n\n"
            
        # מידע על צמיגים - כולל המידע הנוסף
        info_text += "*מידע על צמיגים:*\n"
        if vehicle_info.get('zmig_kidmi'):
            info_text += f"*צמיגים קדמיים:* {vehicle_info.get('zmig_kidmi')}"
            
            # הוספת מידע על עומס ומהירות מהמאגר השני (אם קיים)
            if vehicle_info.get('kod_omes_tzmig_kidmi'):
                info_text += f" | עומס: {vehicle_info.get('kod_omes_tzmig_kidmi')}"
            if vehicle_info.get('kod_mehirut_tzmig_kidmi'):
                info_text += f" | מהירות: {vehicle_info.get('kod_mehirut_tzmig_kidmi')}"
            info_text += "\n"
            
        if vehicle_info.get('zmig_ahori'):
            info_text += f"*צמיגים אחוריים:* {vehicle_info.get('zmig_ahori')}"
            
            # הוספת מידע על עומס ומהירות מהמאגר השני (אם קיים)
            if vehicle_info.get('kod_omes_tzmig_ahori'):
                info_text += f" | עומס: {vehicle_info.get('kod_omes_tzmig_ahori')}"
            if vehicle_info.get('kod_mehirut_tzmig_ahori'):
                info_text += f" | מהירות: {vehicle_info.get('kod_mehirut_tzmig_ahori')}"
            info_text += "\n"
        
        # מידע על גרירה (אם קיים)
        if vehicle_info.get('grira_nm'):
            info_text += f"*מידע על גרירה:* {vehicle_info.get('grira_nm')}\n"
            
        info_text += "\n"
        
        # מידע על רישוי ומבחנים
        info_text += f"*תוקף רישיון:* {vehicle_info.get('tokef_dt', 'לא ידוע')}\n"
        info_text += f"*מבחן אחרון:* {vehicle_info.get('mivchan_acharon_dt', 'לא ידוע')}\n"
        info_text += f"*בעלות:* {vehicle_info.get('baalut', 'לא ידוע')}\n"
        
        if vehicle_info.get('horaat_rishum'):
            info_text += f"*הוראת רישום:* {vehicle_info.get('horaat_rishum')}\n"
            
        # מידע על זיהום ובטיחות
        if vehicle_info.get('kvutzat_zihum') is not None:
            info_text += f"*קבוצת זיהום:* {vehicle_info.get('kvutzat_zihum')}\n"
            
        if vehicle_info.get('ramat_eivzur_betihuty'):
            info_text += f"*רמת אבזור בטיחותי:* {vehicle_info.get('ramat_eivzur_betihuty')}\n"
        
        # עדכון ההודעה עם המידע
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=info_text,
            parse_mode="Markdown"
        )
        
        # מחיקת סטיקר הטעינה אחרי שליחת התשובה
        try:
            bot.delete_message(call.message.chat.id, loading_sticker.message_id)
        except Exception as e:
            print(f"שגיאה במחיקת סטיקר טעינה: {e}")