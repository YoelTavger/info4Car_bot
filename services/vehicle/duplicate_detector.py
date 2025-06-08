import logging
from collections import defaultdict
from typing import Dict, List, Any, Optional

class DuplicateDetector:
    """
    מזהה כפילויות וממזג נתונים ממאגרים שונים
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # שדות שמזהים כפילויות
        self.key_fields = [
            'mispar_rechev',    # מספר רכב
            'misgeret',         # מספר שילדה
            'mispar_shilda',    # מספר שילדה (שדה אלטרנטיבי)
            'shilda'            # מספר שילדה (שדה אלטרנטיבי נוסף)
        ]
        
        # שדות שעדיף למזג (לא להחליף)
        self.merge_fields = [
            'historia', 'ownership_history', 'tav_nehe', 
            'maarchot_betihut', 'wltp_info', 'manufacturer_info'
        ]
        
        # שדות עם עדיפות לפי מקור
        self.source_priority = {
            "מאגר רכב פרטי": 1,
            "מאגר רכב כבד": 2,
            "מאגר דו גלגלי": 3,
            "מאגר יבוא אישי": 4,
            "מאגר רכב לא פעיל": 5,
            "מאגר רכב כבד לא פעיל": 6,
            "מאגר רכב שירד מהכביש": 7
        }
    
    def detect_and_merge_duplicates(self, search_results: List[Dict]) -> List[Dict]:
        """
        מזהה כפילויות וממזג נתונים מכמה מאגרים
        
        Args:
            search_results: רשימת תוצאות מכמה מאגרים
            
        Returns:
            רשימה מאוחדת לאחר מיזוג כפילויות
        """
        if not search_results:
            return search_results
        
        # קיבוץ לפי מפתחות זיהוי
        groups = self._group_by_identity(search_results)
        
        merged_results = []
        
        for group_key, records in groups.items():
            if len(records) == 1:
                # אין כפילויות
                merged_results.append(records[0])
            else:
                # יש כפילויות - צריך למזג
                self.logger.info(f"זוהו {len(records)} כפילויות עבור {group_key}")
                merged_record = self._merge_records(records)
                merged_results.append(merged_record)
        
        return merged_results
    
    def _group_by_identity(self, records: List[Dict]) -> Dict[str, List[Dict]]:
        """
        מקבץ רשומות לפי מפתחות זיהוי
        
        Args:
            records: רשימת רשומות
            
        Returns:
            מילון של קבוצות רשומות
        """
        groups = defaultdict(list)
        
        for record in records:
            # יצירת מפתח זיהוי ייחודי
            identity_key = self._create_identity_key(record)
            groups[identity_key].append(record)
        
        return dict(groups)
    
    def _create_identity_key(self, record: Dict) -> str:
        """
        יוצר מפתח זיהוי ייחודי לרשומה
        
        Args:
            record: רשומת הרכב
            
        Returns:
            מפתח זיהוי ייחודי
        """
        # נסה למצוא את המזהה הטוב ביותר
        for field in self.key_fields:
            value = record.get(field)
            if value and str(value).strip():
                return f"{field}:{str(value).strip()}"
        
        # אם לא נמצא מזהה טוב, השתמש במספר הרכב הבסיסי
        vehicle_number = record.get('mispar_rechev', 'unknown')
        return f"mispar_rechev:{vehicle_number}"
    
    def _merge_records(self, records: List[Dict]) -> Dict:
        """
        ממזג מספר רשומות לרשומה אחת מאוחדת
        
        Args:
            records: רשימת רשומות למיזוג
            
        Returns:
            רשומה מאוחדת
        """
        if not records:
            return {}
        
        if len(records) == 1:
            return records[0]
        
        # מיון הרשומות לפי עדיפות המקור
        sorted_records = sorted(records, key=lambda r: self._get_source_priority(r))
        
        # התחלה עם הרשומה בעדיפות הגבוהה ביותר
        merged = sorted_records[0].copy()
        
        # הוספת מידע על כפילויות
        merged['duplicate_info'] = {
            'sources_count': len(records),
            'sources': [r.get('data_source', 'לא ידוע') for r in records],
            'merged_from': len(records)
        }
        
        # מיזוג נתונים מהרשומות האחרות
        for record in sorted_records[1:]:
            merged = self._merge_single_record(merged, record)
        
        self.logger.info(f"מוזגו {len(records)} רשומות ממקורות: {merged['duplicate_info']['sources']}")
        
        return merged
    
    def _get_source_priority(self, record: Dict) -> int:
        """
        מחזיר את העדיפות של מקור הנתונים
        
        Args:
            record: רשומת הרכב
            
        Returns:
            מספר עדיפות (נמוך יותר = עדיפות גבוהה יותר)
        """
        source = record.get('data_source', '')
        return self.source_priority.get(source, 999)
    
    def _merge_single_record(self, target: Dict, source: Dict) -> Dict:
        """
        ממזג רשומה אחת לתוך רשומת המטרה
        
        Args:
            target: רשומת המטרה
            source: רשומת המקור למיזוג
            
        Returns:
            רשומה מאוחדת
        """
        for key, value in source.items():
            if key in ['data_source']:
                # דלג על שדות מיוחדים
                continue
            
            if key in self.merge_fields:
                # שדות שצריך למזג ולא להחליף
                target[key] = self._merge_field_value(target.get(key), value, key)
            elif key not in target or not target[key]:
                # השדה ריק ברשומת המטרה - מלא אותו
                target[key] = value
                # סמן מאיזה מקור הגיע השדה
                target[f"{key}_source"] = source.get('data_source', 'לא ידוע')
            elif target[key] != value and value:
                # יש סתירה בין הרשומות - שמור את שתי הגרסאות
                target[f"{key}_alternative"] = value
                target[f"{key}_alternative_source"] = source.get('data_source', 'לא ידוע')
        
        return target
    
    def _merge_field_value(self, existing_value: Any, new_value: Any, field_name: str) -> Any:
        """
        ממזג ערכי שדה מיוחדים
        
        Args:
            existing_value: הערך הקיים
            new_value: הערך החדש
            field_name: שם השדה
            
        Returns:
            ערך מאוחד
        """
        if not existing_value:
            return new_value
        
        if not new_value:
            return existing_value
        
        # מיזוג מיוחד לפי סוג השדה
        if field_name == 'ownership_history':
            return self._merge_ownership_history(existing_value, new_value)
        elif field_name in ['historia', 'tav_nehe', 'maarchot_betihut', 'wltp_info', 'manufacturer_info']:
            return self._merge_dict_values(existing_value, new_value)
        else:
            # ברירת מחדל - שמור את הקיים
            return existing_value
    
    def _merge_ownership_history(self, existing: List, new: List) -> List:
        """
        ממזג היסטוריית בעלויות
        
        Args:
            existing: רשימה קיימת
            new: רשימה חדשה
            
        Returns:
            רשימה מאוחדת
        """
        if not isinstance(existing, list):
            existing = []
        if not isinstance(new, list):
            new = []
        
        # איחוד ללא כפילויות
        merged = existing.copy()
        
        for new_record in new:
            # בדוק אם הרשומה כבר קיימת
            exists = any(
                existing_record.get('baalut_dt') == new_record.get('baalut_dt') and
                existing_record.get('baalut') == new_record.get('baalut')
                for existing_record in merged
            )
            
            if not exists:
                merged.append(new_record)
        
        return merged
    
    def _merge_dict_values(self, existing: Dict, new: Dict) -> Dict:
        """
        ממזג ערכי מילון
        
        Args:
            existing: מילון קיים
            new: מילון חדש
            
        Returns:
            מילון מאוחד
        """
        if not isinstance(existing, dict):
            return new if isinstance(new, dict) else existing
        
        if not isinstance(new, dict):
            return existing
        
        merged = existing.copy()
        
        for key, value in new.items():
            if key not in merged or not merged[key]:
                merged[key] = value
        
        return merged
    
    def get_duplicate_summary(self, vehicle_info: Dict) -> Optional[str]:
        """
        מחזיר סיכום על כפילויות שנמצאו
        
        Args:
            vehicle_info: מידע הרכב
            
        Returns:
            טקסט סיכום או None אם אין כפילויות
        """
        duplicate_info = vehicle_info.get('duplicate_info')
        
        if not duplicate_info or duplicate_info.get('sources_count', 1) <= 1:
            return None
        
        sources = duplicate_info.get('sources', [])
        count = duplicate_info.get('sources_count', 0)
        
        summary = f"\n*🔍 זוהו כפילויות:*\n"
        summary += f"נמצא מידע על רכב זה ב-{count} מאגרים שונים:\n"
        
        for i, source in enumerate(sources, 1):
            summary += f"{i}. {source}\n"
        
        summary += f"\nהמידע אוחד אוטומטית ממקורות מרובים ✅\n"
        
        return summary