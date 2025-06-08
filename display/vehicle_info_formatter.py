from display.formatters.date_formatter import format_date, format_road_date
from display.formatters.basic_info_formatter import format_basic_info
from display.formatters.technical_info_formatter import format_technical_info
from display.formatters.wltp_info_formatter import format_wltp_info
from display.formatters.enriched_info_formatter import format_enriched_info
from display.formatters.ownership_history_formatter import format_ownership_history
from services.vehicle.duplicate_detector import DuplicateDetector

# יצירת מופע של מזהה הכפילויות
duplicate_detector = DuplicateDetector()

def format_vehicle_info(vehicle_info, plate_number, show_all_fields=False):
   """
   יוצר טקסט מפורמט של מידע על רכב
   
   Args:
       vehicle_info: מילון עם נתוני הרכב
       plate_number: מספר הרכב
       show_all_fields: האם להציג גם שדות ריקים
       
   Returns:
       טקסט מפורמט של המידע על הרכב
   """
   # קבלת מקור המידע אם קיים
   data_source = vehicle_info.get('data_source', 'מאגר מידע רכב')
   
   # סוג רכב וסטטוס מפורט
   vehicle_type = vehicle_info.get('vehicle_type_detailed', 'לא ידוע')
   vehicle_status = vehicle_info.get('vehicle_status', 'לא ידוע')
   
   # כותרת ומידע בסיסי
   header = "📋 תצוגה מפורטת" if show_all_fields else "🚗 מידע על רכב"
   info_text = f"{header} - רכב מספר {plate_number}\n"
   info_text += f"מקור המידע: {data_source}\n"
   info_text += f"סוג רכב: {vehicle_type}\n"
   info_text += f"סטטוס רכב: {vehicle_status}\n\n"
   
   # מידע על כפילויות אם נמצאו
   duplicate_summary = duplicate_detector.get_duplicate_summary(vehicle_info)
   if duplicate_summary:
       info_text += duplicate_summary
   
   # הוספת מידע על יד וסוג בעלות נוכחית אם קיים
   current_hand = vehicle_info.get('current_hand')
   current_ownership = vehicle_info.get('current_ownership_type')
   
   if current_hand or show_all_fields:
       hand_display = current_hand if current_hand else 'לא ידוע'
       ownership_display = current_ownership if current_ownership else 'לא ידוע'
       info_text += f"יד נוכחית: {hand_display}"
       info_text += f" | סוג בעלות: {ownership_display}\n\n"
   
   # הוספת מידע בסיסי
   info_text += format_basic_info(vehicle_info, show_all_fields)
   
   # הוספת מידע טכני
   info_text += format_technical_info(vehicle_info, show_all_fields)
   
   # הוספת מידע WLTP
   wltp_info = format_wltp_info(vehicle_info, show_all_fields)
   if wltp_info or show_all_fields:
       info_text += wltp_info
   
   # הוספת מידע מועשר
   enriched_info = format_enriched_info(vehicle_info, show_all_fields)
   if enriched_info or show_all_fields:
       info_text += enriched_info
   
   # הוספת היסטוריית בעלויות
   ownership_history = format_ownership_history(vehicle_info, show_all_fields)
   if ownership_history or show_all_fields:
       info_text += ownership_history
   
   # אם תצוגה מפורטת, הוספת כל השדות הגולמיים
   if show_all_fields:
       info_text += format_raw_data(vehicle_info)
   
   return info_text

def format_raw_data(vehicle_info):
   """
   מעצב נתונים גולמיים לתצוגה מפורטת
   
   Args:
       vehicle_info: מילון עם נתוני הרכב
       
   Returns:
       טקסט עם כל הנתונים הגולמיים
   """
   info_text = "\nנתונים גולמיים (כל השדות):\n"
   
   # רשימת שדות שכבר הוצגו (כדי לא לכפול)
   displayed_fields = {
       'mispar_rechev', 'misgeret', 'mispar_shilda', 'shilda',
       'tozeret_nm', 'tozeret_cd', 'degem_nm', 'degem_cd',
       'sug_rechev_nm', 'sug_degem', 'kinuy_mishari', 'ramat_gimur',
       'degem_manoa', 'shnat_yitzur', 'moed_aliya_lakvish', 'bitul_dt',
       'sug_delek_nm', 'tzeva_rechev', 'tzeva_cd', 'data_source',
       'current_hand', 'current_ownership_type', 'wltp_info',
       'historia', 'ownership_history', 'tav_nehe', 'maarchot_betihut',
       'yad_rechev', 'vehicle_type_detected', 'vehicle_type_detailed',
       'vehicle_status', 'manufacturer_info', 'brand', 'country_of_origin', 
       'duplicate_info', 'rank', '_id', 'id',
       # הוספת שדות WLTP שכבר שולבו
       'mishkal_kolel', 'nefach_manoa', 'mispar_moshavim', 'hanaa_nm',
       'koah_sus', 'mispar_dlatot', 'gova'
   }
   
   # הצגת כל השדות שלא הוצגו עדיין
   for key, value in sorted(vehicle_info.items()):
       if key not in displayed_fields and not key.startswith('_') and not key.endswith('_source') and key not in ['rank', 'id']:
           # ניקוי הערך לתצוגה
           if value is None:
               display_value = "ריק"
           elif value == "":
               display_value = "ריק"
           elif isinstance(value, (dict, list)):
               display_value = f"מבנה נתונים ({type(value).__name__})"
           else:
               display_value = str(value)
           
           # תרגום שם השדה לעברית אם אפשר
           hebrew_key = translate_field_name(key)
           
           # הוספת מידע על מקור השדה אם קיים
           source_key = f"{key}_source"
           source_info = ""
           if source_key in vehicle_info:
               source_info = f" (מקור: {vehicle_info[source_key]})"
           
           info_text += f"{hebrew_key}: {display_value}{source_info}\n"
   
   # הצגת שדות חלופיים אם קיימים
   alternative_fields = [k for k in vehicle_info.keys() if k.endswith('_alternative')]
   if alternative_fields:
       info_text += "\nשדות עם ערכים חלופיים (סתירות בין מאגרים):\n"
       for alt_field in alternative_fields:
           base_field = alt_field.replace('_alternative', '')
           original_value = vehicle_info.get(base_field, 'לא ידוע')
           alternative_value = vehicle_info.get(alt_field, 'לא ידוע')
           alt_source = vehicle_info.get(f"{alt_field}_source", 'לא ידוע')
           
           hebrew_key = translate_field_name(base_field)
           info_text += f"{hebrew_key}:\n"
           info_text += f"  • ערך ראשי: {original_value}\n"
           info_text += f"  • ערך חלופי: {alternative_value} (מ{alt_source})\n"
   
   return info_text

def translate_field_name(field_name):
   """
   מתרגם שמות שדות לעברית
   
   Args:
       field_name: שם השדה באנגלית
       
   Returns:
       שם השדה בעברית או המקורי אם אין תרגום
   """
   translations = {
       'mishkal_kolel': 'משקל כולל',
       'mishkal_azmi': 'משקל עצמי',
       'mishkal_mitan_harama': 'משקל מטען הרמה',
       'mispar_manoa': 'מספר מנוע',
       'mispar_mekomot': 'מספר מקומות',
       'mispar_mekomot_leyd_nahag': 'מספר מקומות ליד הנהג',
       'nefach_manoa': 'נפח מנוע',
       'tkina_EU': 'תקינה אירופאית',
       'kvutzat_sug_rechev': 'קבוצת סוג רכב',
       'vehicle_status': 'סטטוס',
       'vehicle_type_detailed': 'סוג רכב',
       'vehicle_type_detected': 'מידע נוסף',
       'tokef_dt': 'תוקף רישיון',
       'mivchan_acharon_dt': 'מבחן אחרון',
       'baalut': 'בעלות',
       'horaat_rishum': 'הוראת רישום',
       'sug_yevu': 'סוג יבוא',
       'kvutzat_zihum': 'קבוצת זיהום',
       'ramat_eivzur_betihuty': 'רמת אבזור בטיחותי',
       'zmig_kidmi': 'צמיגים קדמיים',
       'zmig_ahori': 'צמיגים אחוריים',
       'grira_nm': 'מידע גרירה',
       'nefah_manoa': 'נפח מנוע',
       'koah_sus': 'כוח סוס',
       'mispar_dlatot': 'מספר דלתות',
       'mispar_moshavim': 'מספר מושבים',
       'gova': 'גובה',
       'hanaa_nm': 'סוג הנעה',
       'delek_nm': 'סוג דלק',
       'merkav': 'מרכב',
       'updated_dt': 'תאריך עדכון',
       'rishum_rishon_dt': 'רישום ראשון',
       'mkoriut_nm': 'מקוריות',
       'mida_zmig_kidmi': 'מידת צמיג קדמי',
       'mida_zmig_ahori': 'מידת צמיג אחורי',
       'kod_omes_zmig_kidmi': 'קוד עומס צמיג קדמי',
       'kod_omes_zmig_ahori': 'קוד עומס צמיג אחורי',
       'kod_mehirut_zmig_kidmi': 'קוד מהירות צמיג קדמי',
       'kod_mehirut_zmig_ahori': 'קוד מהירות צמיג אחורי',
       'taxun': 'תחנה',
       'erech_rechev': 'ערך רכב',
       'status_rechev': 'סטטוס רכב'
   }
   
   return translations.get(field_name, field_name)