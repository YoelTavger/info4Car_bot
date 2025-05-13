import telebot
import random
import vehicle_service
import re

def register_license_plate_numbers(bot):
    """
    רושם את כל הטיפולים בהודעות טקסט המכילות מספרי רכב
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
        plate_number = ''.join(filter(str.isdigit, message.text))
        
        # שליחת סטיקר כהודעת טעינה
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
        
        loading_sticker = bot.send_sticker(message.chat.id, random.choice(sticker_ids))
        
        # קבלת מידע מורחב על הרכב
        vehicle_data = vehicle_service.get_vehicle_complete(plate_number)
        
        # טיפול בתוצאות ושליחת ההודעה המתאימה
        if not vehicle_data:
            # אם אין מידע, שליחת הודעת שגיאה
            result_message = bot.reply_to(message, f"לא נמצא מידע עבור רכב מספר {plate_number} ❌")
        else:
            # בניית הודעה עם פרטי הרכב
            vehicle_info = vehicle_data[0]  # לקיחת הרשומה הראשונה
            
            # יצירת טקסט המידע עם כל השדות
            info_text = f"*מידע על רכב מספר {plate_number}* 🚗\n\n"
            
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
            
            # שליחת המידע בתגובה
            result_message = bot.reply_to(message, info_text, parse_mode="Markdown")
        
        # מחיקת סטיקר הטעינה אחרי שליחת ההודעה
        if result_message:
            try:
                bot.delete_message(message.chat.id, loading_sticker.message_id)
            except Exception as e:
                print(f"שגיאה במחיקת סטיקר טעינה: {e}")
