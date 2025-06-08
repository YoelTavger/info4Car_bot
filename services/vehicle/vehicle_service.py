import requests
from config import GOVIL_API_URL, RESOURCE_ID_PRIVATE_VEHICLES, RESOURCE_ID_HEAVY_VEHICLES, RESOURCE_ID_MOTORCYCLES, RESOURCE_ID_INACTIVE_VEHICLES, RESOURCE_ID_INACTIVE_HEAVY, RESOURCE_ID_FINAL_CANCELED, RESOURCE_ID_PERSONAL_IMPORT, RESOURCE_ID_EXTENDED_INFO, RESOURCE_ID_VEHICLE_HISTORY, RESOURCE_ID_DISABILITY_TAG, RESOURCE_ID_SAFETY_SYSTEMS, RESOURCE_ID_OWNERSHIP_HISTORY, RESOURCE_ID_WLTP_MODELS
from services.vehicle.duplicate_detector import DuplicateDetector
from services.vehicle.providers.manufacturer import ManufacturerProvider

# יצירת מופעים של הכלים החדשים
duplicate_detector = DuplicateDetector()
manufacturer_provider = ManufacturerProvider()

def get_vehicle(license_plate):
    """מחזיר מידע על רכב לפי מספר רישוי מהמאגר הראשי"""
    try:
        r = requests.get(GOVIL_API_URL, params={
            "resource_id": RESOURCE_ID_PRIVATE_VEHICLES,
            "q": license_plate,
            "limit": 1
        })
        records = r.json().get("result", {}).get("records", [])
        if records:
            records[0]['data_source'] = "מאגר רכב פרטי"
            records[0]['vehicle_type_detected'] = "רכב פרטי/מסחרי קל"
            return records if records else None
    except Exception as e:
        print(f"שגיאה בקבלת מידע על רכב (מאגר ראשי): {e}")
        return None

def get_vehicle_heavy(license_plate):
    """מחזיר מידע על רכב כבד מעל 3.5 טון"""
    try:
        r = requests.get(GOVIL_API_URL, params={
            "resource_id": RESOURCE_ID_HEAVY_VEHICLES,
            "q": license_plate,
            "limit": 1
        })
        records = r.json().get("result", {}).get("records", [])
        if records:
            records[0]['data_source'] = "מאגר רכב כבד"
            records[0]['vehicle_type_detected'] = "רכב כבד (מעל 3.5 טון)"
            return records if records else None
    except Exception as e:
        print(f"שגיאה בקבלת מידע על רכב כבד: {e}")
        return None

def get_vehicle_motorcycle(license_plate):
    """מחזיר מידע על רכב דו-גלגלי"""
    try:
        r = requests.get(GOVIL_API_URL, params={
            "resource_id": RESOURCE_ID_MOTORCYCLES,
            "q": license_plate,
            "limit": 1
        })
        records = r.json().get("result", {}).get("records", [])
        if records:
            records[0]['data_source'] = "מאגר דו גלגלי"
            records[0]['vehicle_type_detected'] = "אופנוע/דו-גלגלי"
            return records if records else None
    except Exception as e:
        print(f"שגיאה בקבלת מידע על רכב דו-גלגלי: {e}")
        return None

def get_vehicle_inactive(license_plate):
    """מחזיר מידע על רכב לא פעיל"""
    try:
        r = requests.get(GOVIL_API_URL, params={
            "resource_id": RESOURCE_ID_INACTIVE_VEHICLES,
            "q": license_plate,
            "limit": 1
        })
        records = r.json().get("result", {}).get("records", [])
        if records:
            records[0]['data_source'] = "מאגר רכב לא פעיל"
            records[0]['vehicle_type_detected'] = "רכב לא פעיל"
            return records if records else None
    except Exception as e:
        print(f"שגיאה בקבלת מידע על רכב לא פעיל: {e}")
        return None

def get_vehicle_inactive_heavy(license_plate):
    """מחזיר מידע על רכב כבד לא פעיל"""
    try:
        r = requests.get(GOVIL_API_URL, params={
            "resource_id": RESOURCE_ID_INACTIVE_HEAVY,
            "q": license_plate,
            "limit": 1
        })
        records = r.json().get("result", {}).get("records", [])
        if records:
            records[0]['data_source'] = "מאגר רכב כבד לא פעיל"
            records[0]['vehicle_type_detected'] = "רכב כבד לא פעיל"
            return records if records else None
    except Exception as e:
        print(f"שגיאה בקבלת מידע על רכב כבד לא פעיל: {e}")
        return None

def get_vehicle_final_canceled(license_plate):
    """מחזיר מידע על רכב שירד מהכביש"""
    try:
        r = requests.get(GOVIL_API_URL, params={
            "resource_id": RESOURCE_ID_FINAL_CANCELED,
            "q": license_plate,
            "limit": 1
        })
        records = r.json().get("result", {}).get("records", [])
        if records:
            records[0]['data_source'] = "מאגר רכב שירד מהכביש"
            records[0]['vehicle_type_detected'] = "רכב שירד מהכביש"
            return records if records else None
    except Exception as e:
        print(f"שגיאה בקבלת מידע על רכב שירד מהכביש: {e}")
        return None

def get_vehicle_personal_import(license_plate):
    """מחזיר מידע על רכב ביבוא אישי"""
    try:
        r = requests.get(GOVIL_API_URL, params={
            "resource_id": RESOURCE_ID_PERSONAL_IMPORT,
            "q": license_plate,
            "limit": 1
        })
        records = r.json().get("result", {}).get("records", [])
        if records:
            records[0]['data_source'] = "מאגר יבוא אישי"
            records[0]['vehicle_type_detected'] = "יבוא אישי"
            return records if records else None
    except Exception as e:
        print(f"שגיאה בקבלת מידע על רכב ביבוא אישי: {e}")
        return None

def get_vehicle_extended(license_plate):
    """מחזיר מידע נוסף על רכב לפי מספר רישוי מהמאגר המשני"""
    try:
        r = requests.get(GOVIL_API_URL, params={
            "resource_id": RESOURCE_ID_EXTENDED_INFO,
            "q": license_plate,
            "limit": 1
        })
        result = r.json()
        records = result.get("result", {}).get("records", [])
        if records:
            return records[0]
        return None
    except Exception as e:
        print(f"שגיאה בקבלת מידע נוסף על רכב (מאגר משני): {e}")
        return None

def get_vehicle_history(license_plate):
    """מחזיר היסטוריית רכב"""
    try:
        r = requests.get(GOVIL_API_URL, params={
            "resource_id": RESOURCE_ID_VEHICLE_HISTORY,
            "q": license_plate,
            "limit": 1
        })
        records = r.json().get("result", {}).get("records", [])
        if records:
            print(f"נמצאה היסטוריית רכב עבור רכב {license_plate}")
            return records[0]
        return None
    except Exception as e:
        print(f"שגיאה בקבלת היסטוריית רכב: {e}")
        return None
    
def get_vehicle_ownership_history(license_plate):
    """
    מקבל היסטוריית בעלויות של רכב
    
    Args:
        license_plate: מספר רכב
        
    Returns:
        רשימה של רשומות בעלות או None אם לא נמצא
    """
    try:
        r = requests.get(GOVIL_API_URL, params={
            "resource_id": RESOURCE_ID_OWNERSHIP_HISTORY,
            "q": license_plate,
            "limit": 20
        })
        
        result = r.json()
        records = result.get("result", {}).get("records", [])
        
        if records:
            print(f"נמצאו {len(records)} רשומות בעלות לרכב {license_plate}")
            
            # מיון הרשומות לפי תאריך (מהחדש לישן)
            def get_date_key(record):
                date = record.get('baalut_dt', '0')
                return str(date) if date is not None else '0'
                
            sorted_records = sorted(records, key=get_date_key, reverse=True)
            return sorted_records
        else:
            print(f"לא נמצאו רשומות בעלויות לרכב {license_plate}")
            
        return None
    except Exception as e:
        print(f"שגיאה בקבלת היסטוריית בעלויות: {e}")
        return None

def get_disability_tag(license_plate):
    """בודק אם לרכב יש תו נכה"""
    try:
        r = requests.get(GOVIL_API_URL, params={
            "resource_id": RESOURCE_ID_DISABILITY_TAG,
            "q": license_plate,
            "limit": 1
        })
        records = r.json().get("result", {}).get("records", [])
        if records and license_plate in str(records[0].get("MISPAR RECHEV", "")):
            print(f"נמצא תו נכה עבור רכב {license_plate}")
            return records[0]
        return None
    except Exception as e:
        print(f"שגיאה בקבלת מידע על תו נכה: {e}")
        return None

def get_safety_systems(license_plate):
    """בודק אם יש מידע על מערכות בטיחות ברכב"""
    try:
        r = requests.get(GOVIL_API_URL, params={
            "resource_id": RESOURCE_ID_SAFETY_SYSTEMS,
            "q": license_plate,
            "limit": 1
        })
        records = r.json().get("result", {}).get("records", [])
        if records:
            print(f"נמצאו מערכות בטיחות עבור רכב {license_plate}")
            return records[0]
        return None
    except Exception as e:
        print(f"שגיאה בקבלת מידע על מערכות בטיחות: {e}")
        return None

def try_all_vehicle_sources(license_plate):
    """
    מנסה את כל מקורות המידע האפשריים לחיפוש מידע על רכב
    כולל זיהוי כפילויות ומיזוג נתונים
    
    Args:
        license_plate: מספר הרכב לחיפוש
        
    Returns:
        הנתונים מאוחדים לאחר מיזוג כפילויות
    """
    print(f"מחפש רכב {license_plate} בכל המאגרים עם זיהוי כפילויות")
    
    # רשימת כל הפונקציות לחיפוש
    search_functions = [
        get_vehicle,               # רכב פרטי
        get_vehicle_heavy,         # רכב כבד
        get_vehicle_motorcycle,    # דו-גלגלי
        get_vehicle_inactive,      # לא פעיל
        get_vehicle_inactive_heavy, # כבד לא פעיל
        get_vehicle_final_canceled, # ירד מהכביש
        get_vehicle_personal_import # יבוא אישי
    ]
    
    # איסוף כל התוצאות
    all_results = []
    
    # ניסיון לפי הסדר
    for func in search_functions:
        try:
            data = func(license_plate)
            if data:
                print(f"נמצא מידע על רכב {license_plate} במקור: {data[0].get('data_source', 'לא ידוע')}")
                all_results.extend(data)
        except Exception as e:
            print(f"שגיאה בחיפוש ב-{func.__name__}: {e}")
    
    if not all_results:
        print(f"לא נמצא מידע לרכב {license_plate}")
        return None
    
    # זיהוי כפילויות ומיזוג נתונים
    merged_results = duplicate_detector.detect_and_merge_duplicates(all_results)
    
    if merged_results:
        print(f"לאחר מיזוג כפילויות: {len(merged_results)} רשומות")
        return merged_results
    
    return None

def get_vehicle_wltp_data(degem_cd=None, degem_nm=None, shnat_yitzur=None):
    """
    מחזיר מידע WLTP על דגם רכב - רק לרכבים ממאגר פרטי
    
    Args:
        degem_cd: קוד דגם (אופציונלי)
        degem_nm: שם דגם (אופציונלי)
        shnat_yitzur: שנת ייצור (אופציונלי)
        
    Returns:
        מידע נוסף על הדגם
    """
    try:
        # בניית מחרוזת חיפוש
        search_terms = []
        if degem_cd:
            search_terms.append(str(degem_cd))
        if degem_nm:
            search_terms.append(str(degem_nm))
        if shnat_yitzur:
            search_terms.append(str(shnat_yitzur))
            
        search_query = " ".join(search_terms)
        
        if not search_query:
            return None
            
        r = requests.get(GOVIL_API_URL, params={
            "resource_id": RESOURCE_ID_WLTP_MODELS,
            "q": search_query,
            "limit": 5  # ייתכן שיש כמה תוצאות מתאימות
        })
        
        records = r.json().get("result", {}).get("records", [])
        if records:
            print(f"נמצא מידע WLTP עבור דגם {degem_nm} {degem_cd} {shnat_yitzur}")
            return records
        return None
    except Exception as e:
        print(f"שגיאה בקבלת מידע WLTP: {e}")
        return None

def detect_vehicle_type(vehicle_data):
    """
    מזהה סוג רכב מפורט על בסיס הנתונים עם תמיכה באותיות P/M
    
    Args:
        vehicle_data: נתוני הרכב
        
    Returns:
        tuple: (vehicle_type, vehicle_status)
    """
    if not vehicle_data:
        return "לא ידוע", "לא ידוע"
    
    # קביעת סטטוס לפי מקור הנתונים
    data_source = vehicle_data.get('data_source', '')
    if 'לא פעיל' in data_source:
        vehicle_status = "לא פעיל"
    elif 'ירד מהכביש' in data_source:
        vehicle_status = "ירד מהכביש"
    else:
        vehicle_status = "פעיל"
    
    # זיהוי סוג הרכב
    vehicle_type = "לא ידוע"
    
    # בדיקה לפי שדות שונים בסדר עדיפות
    # 1. שדה sug_rechev_nm (כללי) - עדיפות ראשונה
    if vehicle_data.get('sug_rechev_nm'):
        sug_rechev = vehicle_data.get('sug_rechev_nm', '').strip()
        if sug_rechev:
            vehicle_type = sug_rechev
    # 2. זיהוי לפי אות P/M במאגר פרטי (רק אם אין sug_rechev_nm)
    elif vehicle_data.get('data_source') == "מאגר רכב פרטי" and vehicle_data.get('sug_degem'):
        sug_degem = vehicle_data.get('sug_degem', '').strip().upper()
        if sug_degem.startswith('P'):
            vehicle_type = "רכב פרטי"
        elif sug_degem.startswith('M'):
            vehicle_type = "רכב מסחרי קל"
        else:
            vehicle_type = "רכב פרטי/מסחרי"
    # 3. שדה kvutzat_sug_rechev (ברכבים כבדים)
    elif vehicle_data.get('kvutzat_sug_rechev'):
        vehicle_type = vehicle_data.get('kvutzat_sug_rechev')
    # 4. לפי מקור הנתונים
    elif 'דו גלגלי' in data_source:
        vehicle_type = "אופנוע/דו-גלגלי"
    elif 'רכב כבד' in data_source:
        vehicle_type = "רכב כבד"
    elif 'יבוא אישי' in data_source:
        vehicle_type = "יבוא אישי"
    # 5. לפי משקל
    elif vehicle_data.get('mishkal_kolel'):
        try:
            weight = float(vehicle_data.get('mishkal_kolel'))
            if weight > 3500:
                vehicle_type = "רכב כבד (מעל 3.5 טון)"
            else:
                vehicle_type = "רכב קל (עד 3.5 טון)"
        except:
            vehicle_type = "רכב פרטי/מסחרי"
    else:
        vehicle_type = "רכב פרטי/מסחרי"
    
    return vehicle_type, vehicle_status

def merge_wltp_data(main_record, wltp_data):
    """
    ממזג נתוני WLTP עם הרשומה הראשית ומסיר כפילויות
    
    Args:
        main_record: הרשומה הראשית
        wltp_data: נתוני WLTP
        
    Returns:
        רשומה מעודכנת עם נתוני WLTP משולבים
    """
    if not wltp_data:
        return main_record
    
    # שדות שניתן לשלב מ-WLTP אם חסרים או ריקים ברשומה הראשית
    wltp_integration_fields = {
        'mishkal_kolel': 'mishkal_kolel',
        'nefach_manoa': 'nefah_manoa',
        'mispar_moshavim': 'mispar_moshavim', 
        'hanaa_nm': 'hanaa_nm',
        'koah_sus': 'koah_sus',
        'mispar_dlatot': 'mispar_dlatot',
        'gova': 'gova'
    }
    
    # מילוי נתונים חסרים מ-WLTP
    for main_field, wltp_field in wltp_integration_fields.items():
        if wltp_data.get(wltp_field) and (not main_record.get(main_field) or main_record.get(main_field) == ''):
            main_record[main_field] = wltp_data.get(wltp_field)
            main_record[f"{main_field}_source"] = "מאגר WLTP"
    
    # שמירת נתוני WLTP המלאים לתצוגה נפרדת (רק הנתונים שלא שולבו)
    wltp_only_data = {}
    for key, value in wltp_data.items():
        # דלג על שדות שכבר שולבו או שדות מיוחדים
        if key not in wltp_integration_fields.values() and key not in ['_id', 'rank', 'mispar_rechev']:
            wltp_only_data[key] = value
    
    if wltp_only_data:
        main_record['wltp_info'] = wltp_only_data
    
    return main_record

def get_vehicle_complete(license_plate):
    """מחזיר מידע מאוחד מכל המאגרים על הרכב כולל זיהוי כפילויות"""
    # חיפוש רכב בכל המאגרים אפשריים עם זיהוי כפילויות
    vehicle_data = try_all_vehicle_sources(license_plate)
    
    if not vehicle_data:
        return None
    
    try:
        # עבודה עם הרשומה המאוחדת
        main_record = vehicle_data[0]
        
        # זיהוי סוג רכב וסטטוס מפורט (כולל זיהוי P/M)
        vehicle_type, vehicle_status = detect_vehicle_type(main_record)
        main_record['vehicle_type_detailed'] = vehicle_type
        main_record['vehicle_status'] = vehicle_status
        
        # העשרה עם מאגר התוצרים
        main_record = manufacturer_provider.enrich_vehicle_with_manufacturer_data(main_record)
        
        # העשרת מידע נוסף - רק אם המידע מהמאגר הראשי או כבד
        primary_sources = ["מאגר רכב פרטי", "מאגר רכב כבד", "מאגר דו גלגלי"]
        if main_record.get('data_source') in primary_sources:
            # מידע נוסף מהמאגר המעשיר
            extended_data = get_vehicle_extended(license_plate)
            if extended_data:
                # מיזוג המידע הנוסף
                for key, value in extended_data.items():
                    if key not in main_record or not main_record[key]:
                        main_record[key] = value
                        main_record[f"{key}_source"] = "מאגר מידע נוסף"
            
            # חיפוש מידע WLTP - רק לרכבים ממאגר פרטי
            if main_record.get('data_source') == "מאגר רכב פרטי":
                degem_cd = main_record.get('degem_cd')
                degem_nm = main_record.get('degem_nm')
                shnat_yitzur = main_record.get('shnat_yitzur')
                
                wltp_data = get_vehicle_wltp_data(degem_cd, degem_nm, shnat_yitzur)
                if wltp_data and len(wltp_data) > 0:
                    main_record = merge_wltp_data(main_record, wltp_data[0])
        
        # העשרת היסטוריית רכב
        history_data = get_vehicle_history(license_plate)
        if history_data:
            main_record['historia'] = {
                'kilometer_test_aharon': history_data.get('kilometer_test_aharon', ''),
                'shinui_mivne_ind': history_data.get('shinui_mivne_ind', ''),
                'gapam_ind': history_data.get('gapam_ind', ''),
                'shnui_zeva_ind': history_data.get('shnui_zeva_ind', ''),
                'shinui_zmig_ind': history_data.get('shinui_zmig_ind', ''),
                'rishum_rishon_dt': history_data.get('rishum_rishon_dt', ''),
                'mkoriut_nm': history_data.get('mkoriut_nm', ''),
                'makor': 'היסטוריית רכב'
            }
            
        # היסטוריית בעלויות - מתאים לכל סוגי הרכב
        ownership_history = get_vehicle_ownership_history(license_plate)
        if ownership_history:
            main_record['ownership_history'] = ownership_history
            
            # חישוב יד הרכב - מספר הבעלויות ללא סוחרים
            non_dealer_ownerships = [record for record in ownership_history 
                                     if record.get('baalut') != 'סוחר']
            main_record['yad_rechev'] = len(non_dealer_ownerships)
            
        # בדיקת תו נכה
        disability_data = get_disability_tag(license_plate)
        if disability_data:
            main_record['tav_nehe'] = {
                'kiyum': True,
                'sug_tav': disability_data.get('SUG TAV', ''),
                'taarich_hafakat_tag': disability_data.get('TAARICH HAFAKAT TAG', ''),
                'makor': 'תו נכה'
            }
        
        # בדיקת מערכות בטיחות
        safety_data = get_safety_systems(license_plate)
        if safety_data:
            main_record['maarchot_betihut'] = {
                'kiyum': True,
                'updated_dt': safety_data.get('updated_dt', ''),
                'makor': 'מערכות בטיחות'
            }
    except Exception as e:
        print(f"שגיאה בהעשרת מידע על רכב: {e}")
    
    return vehicle_data