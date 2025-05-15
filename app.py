import telebot
import os
import time
import requests
from server import setup_webhook_server
from config import API_TOKEN, IS_RENDER, WEBHOOK_URL, PORT, GOVIL_API_URL, RESOURCE_ID_PRIVATE_VEHICLES
from handlers.registry import register_all_handlers
from keep_alive import setup_keep_alive

def test_api_connection():
    """בדיקת חיבור ל-API"""
    try:
        test_plate = "12345678"  # מספר רכב לבדיקה 
        r = requests.get(
            GOVIL_API_URL, 
            params={
                "resource_id": RESOURCE_ID_PRIVATE_VEHICLES,
                "q": test_plate,
                "limit": 5
            },
            timeout=10
        )
        
        print(f"תשובה מה-API: {r.status_code}")
        result = r.json()
        records = result.get("result", {}).get("records", [])
        print(f"מספר רשומות שהתקבלו: {len(records)}")
        
        if records:
            print(f"דוגמה לרשומה: {records[0].get('mispar_rechev')}")
        
        return r.status_code == 200
    except Exception as e:
        print(f"שגיאה בבדיקת API: {e}")
        return False

def main():
    """
    פונקציית הכניסה הראשית של הבוט
    """
    # בדיקה שקיים טוקן תקין
    if not API_TOKEN:
        raise ValueError("חסר טוקן API! וודא שקובץ .env מוגדר כראוי.")
    
    # בדיקת תקשורת עם ה-API
    print("בודק חיבור ל-API...")
    api_working = test_api_connection()
    if not api_working:
        print("אזהרה: חיבור ל-API נכשל, ייתכן שהמערכת לא תעבוד כראוי")
    
    # יצירת מופע הבוט
    bot = telebot.TeleBot(API_TOKEN)

    # רישום כל הטיפולים בפקודות
    register_all_handlers(bot)

    # הפעלת הבוט
    try:
        print("הבוט מופעל! לחץ Ctrl+C כדי לעצור.")
        
        if IS_RENDER:
            print(f"מפעיל במצב webhook עבור Render")
            
            webhook_url = WEBHOOK_URL
            if not webhook_url:
                print("אזהרה: WEBHOOK_URL לא מוגדר. ייתכן שהבוט לא יעבוד כראוי.")
                # השתמש בכתובת ברירת מחדל אם לא הוגדרה
                webhook_url = f"https://{os.environ.get('RENDER_SERVICE_NAME')}.onrender.com/{API_TOKEN}"
                
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
            setup_webhook_server(bot, API_TOKEN, PORT)
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