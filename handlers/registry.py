from handlers.command_handlers import register_command_handlers
from handlers.text_handlers import register_text_handlers
from handlers.license_plate_handlers import register_license_plate_handlers
from handlers.photo_handlers import register_photo_handlers
from handlers.callback_handlers import register_callback_handlers

def register_all_handlers(bot):
    """
    רישום כל הטיפולים בבוט
    
    Args:
        bot: מופע הבוט
    """
    # רישום הטיפולים לפי סדר העדיפות
    register_photo_handlers(bot)
    register_license_plate_handlers(bot)
    register_callback_handlers(bot)
    register_command_handlers(bot)
    
    # רישום טיפול בטקסט כללי אחרון (כברירת מחדל)
    register_text_handlers(bot)