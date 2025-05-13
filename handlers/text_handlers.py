from display.response_messages import get_default_text_message

def register_text_handlers(bot):
    """
    רישום הטיפולים בהודעות טקסט כלליות
    
    Args:
        bot: מופע הבוט
    """
    # טיפול בהודעות טקסט אחרות
    @bot.message_handler(func=lambda message: True)
    def handle_text_message(message):
        """מטפל בכל הודעה שאינה פקודה מוכרת או מספר רכב"""
        bot.send_message(message.chat.id, get_default_text_message())