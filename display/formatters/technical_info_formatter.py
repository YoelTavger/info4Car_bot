from display.formatters.date_formatter import format_date

def format_technical_info(vehicle_info, show_all_fields=False):
    """
    מעצב את המידע הטכני על הרכב
    
    Args:
        vehicle_info: מילון עם נתוני הרכב
        show_all_fields: האם להציג גם שדות ריקים
    
    Returns:
        טקסט מפורמט עם המידע הטכני
    """
    info_text = "\n"
    
    # מידע על משקל
    weight_info = []
    if vehicle_info.get('mishkal_kolel') or show_all_fields:
        weight = vehicle_info.get('mishkal_kolel', 'לא ידוע') if show_all_fields else vehicle_info.get('mishkal_kolel')
        source_info = ""
        if vehicle_info.get('mishkal_kolel_source'):
            source_info = f" (מקור: {vehicle_info.get('mishkal_kolel_source')})"
        weight_info.append(f"משקל כולל: {weight} ק\"ג{source_info}")
    
    if vehicle_info.get('mishkal_azmi') or show_all_fields:
        weight = vehicle_info.get('mishkal_azmi', 'לא ידוע') if show_all_fields else vehicle_info.get('mishkal_azmi')
        weight_info.append(f"משקל עצמי: {weight} ק\"ג")
    
    # שדות מיוחדים לרכבים כבדים
    if vehicle_info.get('mishkal_mitan_harama') or show_all_fields:
        weight = vehicle_info.get('mishkal_mitan_harama', 'לא ידוע') if show_all_fields else vehicle_info.get('mishkal_mitan_harama')
        weight_info.append(f"משקל מטען הרמה: {weight} ק\"ג")
    
    if weight_info:
        info_text += "\n".join(weight_info) + "\n"
    
    # מידע על מנוע ומושבים (כולל שדות מיוחדים לרכבים כבדים)
    engine_info = []
    
    # נפח מנוע
    if vehicle_info.get('nefach_manoa') or show_all_fields:
        volume = vehicle_info.get('nefach_manoa', 'לא ידוע') if show_all_fields else vehicle_info.get('nefach_manoa')
        source_info = ""
        if vehicle_info.get('nefach_manoa_source'):
            source_info = f" (מקור: {vehicle_info.get('nefach_manoa_source')})"
        engine_info.append(f"נפח מנוע: {volume} סמ\"ק{source_info}")
    
    # כוח סוס
    if vehicle_info.get('koah_sus') or show_all_fields:
        power = vehicle_info.get('koah_sus', 'לא ידוע') if show_all_fields else vehicle_info.get('koah_sus')
        source_info = ""
        if vehicle_info.get('koah_sus_source'):
            source_info = f" (מקור: {vehicle_info.get('koah_sus_source')})"
        engine_info.append(f"כוח סוס: {power}{source_info}")
    
    # מספר מנוע
    if vehicle_info.get('mispar_manoa') or show_all_fields:
        engine_num = vehicle_info.get('mispar_manoa', 'לא ידוע') if show_all_fields else vehicle_info.get('mispar_manoa')
        engine_info.append(f"מספר מנוע: {engine_num}")
    
    # מספר מקומות - כללי
    if vehicle_info.get('mispar_mekomot') or show_all_fields:
        seats = vehicle_info.get('mispar_mekomot', 'לא ידוע') if show_all_fields else vehicle_info.get('mispar_mekomot')
        engine_info.append(f"מספר מקומות: {seats}")
    
    # מספר מושבים (מ-WLTP)
    if vehicle_info.get('mispar_moshavim') or show_all_fields:
        seats = vehicle_info.get('mispar_moshavim', 'לא ידוע') if show_all_fields else vehicle_info.get('mispar_moshavim')
        source_info = ""
        if vehicle_info.get('mispar_moshavim_source'):
            source_info = f" (מקור: {vehicle_info.get('mispar_moshavim_source')})"
        engine_info.append(f"מספר מושבים: {seats}{source_info}")
    
    # מספר דלתות
    if vehicle_info.get('mispar_dlatot') or show_all_fields:
        doors = vehicle_info.get('mispar_dlatot', 'לא ידוע') if show_all_fields else vehicle_info.get('mispar_dlatot')
        source_info = ""
        if vehicle_info.get('mispar_dlatot_source'):
            source_info = f" (מקור: {vehicle_info.get('mispar_dlatot_source')})"
        engine_info.append(f"מספר דלתות: {doors}{source_info}")
    
    # מספר מקומות ליד הנהג - לרכבים כבדים
    if vehicle_info.get('mispar_mekomot_leyd_nahag') or show_all_fields:
        seats = vehicle_info.get('mispar_mekomot_leyd_nahag', 'לא ידוע') if show_all_fields else vehicle_info.get('mispar_mekomot_leyd_nahag')
        engine_info.append(f"מספר מקומות ליד הנהג: {seats}")
    
    # גובה
    if vehicle_info.get('gova') or show_all_fields:
        height = vehicle_info.get('gova', 'לא ידוע') if show_all_fields else vehicle_info.get('gova')
        source_info = ""
        if vehicle_info.get('gova_source'):
            source_info = f" (מקור: {vehicle_info.get('gova_source')})"
        engine_info.append(f"גובה: {height}{source_info}")
    
    # סוג הנעה (שדה נוסף לרכבים כבדים)
    if vehicle_info.get('hanaa_nm') or show_all_fields:
        hanaa = vehicle_info.get('hanaa_nm', 'לא ידוע') if show_all_fields else vehicle_info.get('hanaa_nm')
        source_info = ""
        if vehicle_info.get('hanaa_nm_source'):
            source_info = f" (מקור: {vehicle_info.get('hanaa_nm_source')})"
        engine_info.append(f"סוג הנעה: {hanaa}{source_info}")
    
    if engine_info:
        info_text += "\n" + "\n".join(engine_info) + "\n"
    
    # מידע על צמיגים - רק אם יש מידע
    tire_fields = [
        ('zmig_kidmi', 'צמיגים קדמיים'),
        ('zmig_ahori', 'צמיגים אחוריים'),
        ('mida_zmig_kidmi', 'מידת צמיג קדמי'),
        ('mida_zmig_ahori', 'מידת צמיג אחורי')
    ]
    
    has_tire_info = any(vehicle_info.get(field) for field, _ in tire_fields) or show_all_fields
    
    if has_tire_info:
        info_text += "\nמידע על צמיגים:\n"
        
        for field, display_name in tire_fields:
            value = vehicle_info.get(field)
            if value or show_all_fields:
                display_value = value if value else 'לא ידוע'
                info_text += f"{display_name}: {display_value}"
                
                # הוספת מידע נוסף על עומס ומהירות
                if field in ['zmig_kidmi', 'mida_zmig_kidmi']:
                    load_key = 'kod_omes_tzmig_kidmi' if field == 'zmig_kidmi' else 'kod_omes_zmig_kidmi'
                    speed_key = 'kod_mehirut_tzmig_kidmi' if field == 'zmig_kidmi' else 'kod_mehirut_zmig_kidmi'
                elif field in ['zmig_ahori', 'mida_zmig_ahori']:
                    load_key = 'kod_omes_tzmig_ahori' if field == 'zmig_ahori' else 'kod_omes_zmig_ahori'
                    speed_key = 'kod_mehirut_tzmig_ahori' if field == 'zmig_ahori' else 'kod_mehirut_zmig_ahori'
                else:
                    load_key = speed_key = None
                
                if load_key and (vehicle_info.get(load_key) or show_all_fields):
                    load_value = vehicle_info.get(load_key, 'לא ידוע') if show_all_fields else vehicle_info.get(load_key)
                    info_text += f" | עומס: {load_value}"
                
                if speed_key and (vehicle_info.get(speed_key) or show_all_fields):
                    speed_value = vehicle_info.get(speed_key, 'לא ידוע') if show_all_fields else vehicle_info.get(speed_key)
                    info_text += f" | מהירות: {speed_value}"
                
                info_text += "\n"
        
        # מידע על גרירה
        if vehicle_info.get('grira_nm') or show_all_fields:
            grira_value = vehicle_info.get('grira_nm', 'לא ידוע') if show_all_fields else vehicle_info.get('grira_nm')
            info_text += f"מידע על גרירה: {grira_value}\n"
    
    # מידע על רישוי ומבחנים וסטנדרטים
    license_info = []
    
    if vehicle_info.get('tokef_dt') or show_all_fields:
        date_value = vehicle_info.get('tokef_dt')
        if date_value:
            date_value = format_date(date_value)
        else:
            date_value = 'לא ידוע'
        license_info.append(f"תוקף רישיון: {date_value}")
    
    if vehicle_info.get('mivchan_acharon_dt') or show_all_fields:
        date_value = vehicle_info.get('mivchan_acharon_dt')
        if date_value:
            date_value = format_date(date_value)
        else:
            date_value = 'לא ידוע'
        license_info.append(f"מבחן אחרון: {date_value}")
    
    if vehicle_info.get('baalut') or show_all_fields:
        baalut_value = vehicle_info.get('baalut', 'לא ידוע') if show_all_fields else vehicle_info.get('baalut')
        license_info.append(f"בעלות: {baalut_value}")
    
    if vehicle_info.get('horaat_rishum') or show_all_fields:
        horaat_value = vehicle_info.get('horaat_rishum', 'לא ידוע') if show_all_fields else vehicle_info.get('horaat_rishum')
        license_info.append(f"הוראת רישום: {horaat_value}")
    
    if vehicle_info.get('sug_yevu') or show_all_fields:
        yevu_value = vehicle_info.get('sug_yevu', 'לא ידוע') if show_all_fields else vehicle_info.get('sug_yevu')
        license_info.append(f"סוג יבוא: {yevu_value}")
    
    # תקינה אירופאית (לרכבים כבדים)
    if vehicle_info.get('tkina_EU') or show_all_fields:
        tkina_value = vehicle_info.get('tkina_EU', 'לא ידוע') if show_all_fields else vehicle_info.get('tkina_EU')
        license_info.append(f"תקינה אירופאית: {tkina_value}")
    
    if license_info:
        info_text += "\n" + "\n".join(license_info) + "\n"
    
    # מידע על זיהום ובטיחות
    env_safety_info = []
    
    if vehicle_info.get('kvutzat_zihum') is not None or show_all_fields:
        zihum_value = vehicle_info.get('kvutzat_zihum')
        if zihum_value is not None:
            zihum_value = str(zihum_value)
        else:
            zihum_value = 'לא ידוע'
        env_safety_info.append(f"קבוצת זיהום: {zihum_value}")
        
    if vehicle_info.get('ramat_eivzur_betihuty') or show_all_fields:
        safety_value = vehicle_info.get('ramat_eivzur_betihuty', 'לא ידוע') if show_all_fields else vehicle_info.get('ramat_eivzur_betihuty')
        env_safety_info.append(f"רמת אבזור בטיחותי: {safety_value}")
    
    if env_safety_info:
        info_text += "\n" + "\n".join(env_safety_info) + "\n"
    
    return info_text