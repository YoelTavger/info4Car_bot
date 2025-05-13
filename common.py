def register_handlers(bot):
    """
    רישום הטיפולים הבסיסיים
    
    Args:
        bot: מופע הבוט
    """
    # פקודת התחלה
    @bot.message_handler(commands=['start'])
    def start_command(message):
        """טיפול בפקודת התחלה"""
        user = message.from_user
        
        welcome_text = f"""היי {user.first_name}! 👋

בוט המידע לרכבים מאפשר לך לקבל מידע על רכבים בישראל 🚗

פשוט:
- שלח מספר רכב (12345678)
- או שלח תמונה של לוחית רישוי

המאגר כולל רכבים פרטיים משנת 96' ומעלה ורכבים מסחריים קלים משנת 98'.

נסה עכשיו! 👇"""
        
        bot.send_message(message.chat.id, welcome_text)
        
    # טיפול בהודעות טקסט אחרות
    @bot.message_handler(func=lambda message: True)
    def echo_all(message):
        """מטפל בכל הודעה שאינה פקודה מוכרת"""
        bot.send_message(message.chat.id, "שלח מספר רכב או תמונה של לוחית רישוי כדי לקבל מידע 🔍")