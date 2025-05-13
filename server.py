from flask import Flask, request
import telebot

def setup_webhook_server(bot, token, port):
    """
    הגדרת שרת Flask עבור Webhook
    
    Args:
        bot: מופע הבוט
        token: טוקן API של הבוט
        port: פורט להאזנה
    """
    app = Flask(__name__)
    
    @app.route('/' + token, methods=['POST'])
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
    app.run(host='0.0.0.0', port=port)