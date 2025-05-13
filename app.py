import telebot
import os
import time
from common import register_handlers
from config import API_TOKEN, IS_RENDER, WEBHOOK_URL, PORT
from keep_alive import setup_keep_alive
from license_plate_numbers_handlers import register_license_plate_numbers
from photo_handlers import register_photo


def main():
    """
    פונקציית הכניסה הראשית של הבוט
    """
    # בדיקה שקיים טוקן תקין
    if not API_TOKEN:
        raise ValueError("חסר טוקן API! וודא שקובץ .env מוגדר כראוי.")
    
    # יצירת מופע הבוט
    bot = telebot.TeleBot(API_TOKEN)

    # רישום כל הטיפולים בפקודות
    register_photo(bot)
    register_license_plate_numbers(bot)
    register_handlers(bot)

    # הפעלת הבוט
    try:
        print("הבוט מופעל! לחץ Ctrl+C כדי לעצור.")
        
        if IS_RENDER:
            print(f"מפעיל במצב webhook עבור Render")
            
            if not WEBHOOK_URL:
                print("אזהרה: WEBHOOK_URL לא מוגדר. ייתכן שהבוט לא יעבוד כראוי.")
                # השתמש בכתובת ברירת מחדל אם לא הוגדרה
                webhook_url = f"https://{os.environ.get('RENDER_SERVICE_NAME')}.onrender.com/{API_TOKEN}"
            else:
                webhook_url = WEBHOOK_URL
                
            # הפעלת מנגנון Keep-Alive עם כתובת ה-webhook
            # הוצא את חלק הנתיב מ-webhook_url כדי לקבל רק את כתובת הבסיס
            base_url = webhook_url.split('/' + API_TOKEN)[0]
            print(f"מפעיל מנגנון Keep-Alive עם URL: {base_url}")
            setup_keep_alive(base_url)
            
            # הסרת webhook קיים והגדרת webhook חדש
            bot.remove_webhook()
            time.sleep(1)
            bot.set_webhook(url=webhook_url)
            
            # הפעלת שרת Flask לקבלת עדכונים
            from flask import Flask, request
            app = Flask(__name__)
            
            @app.route('/' + API_TOKEN, methods=['POST'])
            def webhook():
                try:
                    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
                    bot.process_new_updates([update])
                    return ''
                except Exception as e:
                    print(f"שגיאה בטיפול בעדכון: {e}")
                    return 'error'
            
            @app.route('/')
            def index():
                return "בוט אינפו-רכב פעיל!"
            
            # הפעלת שרת
            app.run(host='0.0.0.0', port=PORT)
        else:
            # הפעלה במצב polling (מקומי)
            print("מפעיל במצב polling")
            bot.remove_webhook()
            time.sleep(1)
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except KeyboardInterrupt:
        print("הבוט הופסק על ידי המשתמש.")
    except Exception as e:
        print(f"שגיאה קריטית בהפעלת הבוט: {e}")

if __name__ == "__main__":
    main()