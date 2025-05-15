def format_wltp_info(vehicle_info):
    """
    מעצב את כל המידע הזמין מ-WLTP על הרכב
    
    Args:
        vehicle_info: מילון עם נתוני הרכב
    
    Returns:
        טקסט מפורמט עם המידע מ-WLTP
    """
    info_text = ""
    
    # בדיקה אם יש מידע WLTP
    if not vehicle_info.get('wltp_info'):
        return info_text
        
    wltp = vehicle_info['wltp_info']
    info_text += "\n*נתוני WLTP - כל המידע הזמין:*\n"
    
    # הדפסת כל השדות הזמינים
    for key, value in wltp.items():
        # דילוג על שדות מיוחדים
        if key in ['_id', 'rank']:
            continue
            
        # אם יש ערך
        if value:
            # נרמול הערך במקרה של אינדיקטורים
            display_value = value
            if key.endswith('_ind') and value == 1:
                display_value = "✅"
            elif key.endswith('_ind') and value == 0:
                display_value = "❌"
                
            # מציאת התרגום לעברית אם קיים
            hebrew_key = get_hebrew_field_name(key)
            
            # טיפול בתווים מיוחדים ב-Markdown
            hebrew_key = escape_markdown(hebrew_key)
            
            if isinstance(display_value, str):
                display_value = escape_markdown(display_value)
            
            info_text += f"*{hebrew_key}:* {display_value}\n"
    
    return info_text

def escape_markdown(text):
    """
    מחליף תווים מיוחדים ב-Markdown
    
    Args:
        text: הטקסט לבריחה
        
    Returns:
        טקסט עם תווים מוחלפים
    """
    if not text:
        return text
        
    # החלפת תווים מיוחדים
    replacements = [
        ('*', '\\*'),
        ('_', '\\_'),
        ('`', '\\`'),
        ('[', '\\['),
        (']', '\\]'),
        ('(', '\\('),
        (')', '\\)'),
        ('~', '\\~'),
        ('>', '\\>'),
        ('#', '\\#'),
        ('+', '\\+'),
        ('-', '\\-'),
        ('=', '\\='),
        ('|', '\\|'),
        ('{', '\\{'),
        ('}', '\\}'),
        ('.', '\\.'),
        ('!', '\\!')
    ]
    
    escaped_text = text
    for old, new in replacements:
        # החלף רק אם התו לא חלק מהתגים של HTML
        if old not in ['<', '>']:
            escaped_text = escaped_text.replace(old, new)
    
    return escaped_text

def get_hebrew_field_name(field_name):
    """
    מחזיר את השם בעברית של שדה ב-WLTP
    
    Args:
        field_name: שם השדה באנגלית
    
    Returns:
        שם השדה בעברית או השם המקורי אם אין תרגום
    """
    # מילון תרגום שדות עם בריחה מתווים מיוחדים
    field_translations = {
        "mispar_rechev": "מספר רכב",
        "sug_degem": "סוג דגם",
        "tozeret_cd": "קוד יצרן",
        "tozeret_nm": "שם יצרן",
        "tozeret_eretz_nm": "מדינת יצרן",
        "tozar": "מותג",
        "degem_cd": "קוד דגם",
        "degem_nm": "שם דגם",
        "shnat_yitzur": "שנת ייצור",
        "kvuzat_agra_cd": "קוד קבוצת אגרה",
        "nefah_manoa": "נפח מנוע (סמ\"ק)",
        "mishkal_kolel": "משקל כולל",
        "gova": "גובה",
        "hanaa_cd": "קוד הנעה",
        "hanaa_nm": "סוג הנעה",
        "mazgan_ind": "מזגן",
        "abs_ind": "בלם ABS",  # תו מיוחד
        "kariot_avir_source": "מקור כריות אוויר",
        "mispar_kariot_avir": "מספר כריות אוויר",
        "hege_koah_ind": "הגה כוח",
        "automatic_ind": "תיבת הילוכים אוטומטית",
        "halonot_hashmal_source": "מקור חלונות חשמל",
        "mispar_halonot_hashmal": "מספר חלונות חשמל",
        "halon_bagg_ind": "חלון בגג",
        "galgaley_sagsoget_kala_ind": "גלגלי סגסוגת קלה",
        "argaz_ind": "ארגז",
        "merkav": "מרכב",
        "ramat_gimur": "רמת גימור",
        "delek_cd": "קוד סוג דלק",
        "delek_nm": "סוג דלק",
        "mispar_dlatot": "מספר דלתות",
        "koah_sus": "כוח סוס",
        "mispar_moshavim": "מספר מושבים",
        "bakarat_yatzivut_ind": "בקרת יציבות",
        "kosher_grira_im_blamim": "כושר גרירה עם בלמים (ק\"ג)",
        "kosher_grira_bli_blamim": "כושר גרירה בלי בלמים (ק\"ג)",
        "sug_tkina_cd": "קוד סוג תקינה",
        "sug_tkina_nm": "שם סוג תקינה",
        "sug_mamir_cd": "קוד סוג ממיר",
        "sug_mamir_nm": "שם סוג ממיר",
        "technologiat_hanaa_cd": "קוד טכנולוגיית הנעה",
        "technologiat_hanaa_nm": "טכנולוגיית הנעה",
        "kamut_CO2": "פליטת CO₂",
        "kamut_NOX": "פליטת NOx",
        "kamut_PM10": "פליטת PM10",
        "kamut_HC": "פליטת פחמימנים",
        "kamut_HC_NOX": "פליטת HC ו-NOx",  # שינוי + ל-ו
        "kamut_CO": "פליטת CO",
        "madad_yarok": "מדד ירוק",
        "kvutzat_zihum": "קבוצת זיהום",
        "bakarat_stiya_menativ_ind": "בקרת סטייה מנתיב",
        "bakarat_stiya_menativ_makor_hatkana": "מקור התקנה בקרת סטייה",  # הסרת המקף
        "nitur_merhak_milfanim_ind": "ניטור מרחק מלפנים",
        "nitur_merhak_milfanim_makor_hatkana": "מקור התקנה ניטור מרחק",  # הסרת המקף
        "zihuy_beshetah_nistar_ind": "זיהוי בשטח נסתר",
        "bakarat_shyut_adaptivit_ind": "בקרת שיוט אדפטיבית",
        "zihuy_holchey_regel_ind": "זיהוי הולכי רגל",
        "zihuy_holchey_regel_makor_hatkana": "מקור התקנה זיהוי הולכי רגל",  # הסרת המקף
        "maarechet_ezer_labalam_ind": "מערכת עזר לבלם",
        "matzlemat_reverse_ind": "מצלמת רוורס",
        "hayshaney_lahatz_avir_batzmigim_ind": "חיישני לחץ אוויר בצמיגים",
        "hayshaney_hagorot_ind": "חיישני חגורות בטיחות",
        "nikud_betihut": "ניקוד בטיחות",
        "ramat_eivzur_betihuty": "רמת אבזור בטיחות",
        "teura_automatit_benesiya_kadima_ind": "תאורה אוטומטית בנסיעה קדימה",
        "shlita_automatit_beorot_gvohim_ind": "שליטה אוטומטית באורות גבוהים",
        "zihuy_matzav_hitkarvut_mesukenet_ind": "זיהוי מצב התקרבות מסוכן",
        "zihuy_tamrurey_tnua_ind": "זיהוי תמרורי תנועה",
        "zihuy_tamrurey_tnua_makor_hatkana": "מקור התקנה זיהוי תמרורי תנועה",  # הסרת המקף
        "zihuy_rechev_do_galgali": "זיהוי רכב דו גלגלי",  # הסרת המקף
        "CO2_WLTP": "פליטת CO2 בתקן WLTP",
        "bakarat_stiya_activ_s": "בקרת סטייה אקטיבית",
        "blima_otomatit_nesia_leahor": "בלימה אוטומטית בנסיעה לאחור",
        "bakarat_mehirut_isa": "בקרת מהירות נסיעה",
        "blimat_hirum_lifnei_holhei_regel_ofanaim": "בלימת חירום לפני הולכי רגל ואופניים",  # הסרת /
        "hitnagshut_cad_shetah_met": "התנגשות צד בשטח מת",
        "alco_lock": "נעילת התנעה תחת השפעת אלכוהול",
        "dg_metach_solela": "דרגת מתח סוללה",
        "kinuy_mishari": "כינוי מסחרי"
    }
    
    # החזרת התרגום אם קיים, אחרת החזרת השם המקורי
    return field_translations.get(field_name, field_name)