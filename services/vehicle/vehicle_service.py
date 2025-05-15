import requests
from config import GOVIL_API_URL, RESOURCE_ID_PRIVATE_VEHICLES, RESOURCE_ID_HEAVY_VEHICLES, RESOURCE_ID_MOTORCYCLES, RESOURCE_ID_INACTIVE_VEHICLES, RESOURCE_ID_INACTIVE_HEAVY, RESOURCE_ID_FINAL_CANCELED, RESOURCE_ID_PERSONAL_IMPORT, RESOURCE_ID_EXTENDED_INFO, RESOURCE_ID_VEHICLE_HISTORY, RESOURCE_ID_DISABILITY_TAG, RESOURCE_ID_SAFETY_SYSTEMS, RESOURCE_ID_OWNERSHIP_HISTORY, RESOURCE_ID_WLTP_MODELS

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
            # print(f"מידע ממאגר ראשי: {records}")
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
            records[0]['data_source'] = "מאגר דו-גלגלי"
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
            # print(f"מידע ממאגר משני: {records}")
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
    
    Args:
        license_plate: מספר הרכב לחיפוש
        
    Returns:
        הנתונים מהמקור הראשון שהחזיר תוצאות
    """
    print(f"מחפש רכב {license_plate} בכל המאגרים")
    
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
    
    # ניסיון לפי הסדר
    for func in search_functions:
        try:
            data = func(license_plate)
            if data:
                print(f"נמצא מידע על רכב {license_plate} במקור: {data[0].get('data_source', 'לא ידוע')}")
                return data
        except Exception as e:
            print(f"שגיאה בחיפוש: {e}")
    
    print(f"לא נמצא מידע לרכב {license_plate}")
    return None

def get_vehicle_wltp_data(degem_cd=None, degem_nm=None, shnat_yitzur=None):
    """
    מחזיר מידע WLTP על דגם רכב
    
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

def get_vehicle_complete(license_plate):
    """מחזיר מידע מאוחד מכל המאגרים על הרכב"""
    # חיפוש רכב בכל המאגרים אפשריים
    vehicle_data = try_all_vehicle_sources(license_plate)
    
    if not vehicle_data:
        return None
    
    try:
        # העשרת מידע נוסף - רק אם המידע מהמאגר הראשי
        if vehicle_data[0].get('data_source') == "מאגר רכב פרטי":
            # מידע נוסף מהמאגר המעשיר
            extended_data = get_vehicle_extended(license_plate)
            if extended_data:
                # מיזוג המידע הנוסף
                for key, value in extended_data.items():
                    if key not in vehicle_data[0] or not vehicle_data[0][key]:
                        vehicle_data[0][key] = value
            
            # חיפוש מידע WLTP על הדגם
            degem_cd = vehicle_data[0].get('degem_cd')
            degem_nm = vehicle_data[0].get('degem_nm')
            shnat_yitzur = vehicle_data[0].get('shnat_yitzur')
            
            wltp_data = get_vehicle_wltp_data(degem_cd, degem_nm, shnat_yitzur)
            if wltp_data and len(wltp_data) > 0:
                vehicle_data[0]['wltp_info'] = wltp_data[0]
        
        # העשרת היסטוריית רכב
        history_data = get_vehicle_history(license_plate)
        if history_data:
            vehicle_data[0]['historia'] = {
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
            vehicle_data[0]['ownership_history'] = ownership_history
            
            # חישוב יד הרכב - מספר הבעלויות ללא סוחרים
            non_dealer_ownerships = [record for record in ownership_history 
                                     if record.get('baalut') != 'סוחר']
            vehicle_data[0]['yad_rechev'] = len(non_dealer_ownerships)
            
        # בדיקת תו נכה
        disability_data = get_disability_tag(license_plate)
        if disability_data:
            vehicle_data[0]['tav_nehe'] = {
                'kiyum': True,
                'sug_tav': disability_data.get('SUG TAV', ''),
                'taarich_hafakat_tag': disability_data.get('TAARICH HAFAKAT TAG', ''),
                'makor': 'תו נכה'
            }
        
        # בדיקת מערכות בטיחות
        safety_data = get_safety_systems(license_plate)
        if safety_data:
            vehicle_data[0]['maarchot_betihut'] = {
                'kiyum': True,
                'updated_dt': safety_data.get('updated_dt', ''),
                'makor': 'מערכות בטיחות'
            }
    except Exception as e:
        print(f"שגיאה בהעשרת מידע על רכב: {e}")
    
    return vehicle_data
