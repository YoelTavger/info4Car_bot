from display.response_messages import get_welcome_message

def register_command_handlers(bot):
    """
    רישום הטיפולים בפקודות
    
    Args:
        bot: מופע הבוט
    """
    @bot.message_handler(commands=['start'])
    def start_command(message):
        """טיפול בפקודת התחלה"""
        user = message.from_user
        welcome_text = get_welcome_message(user.first_name)
        bot.send_message(message.chat.id, welcome_text)