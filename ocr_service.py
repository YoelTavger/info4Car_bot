import requests
from config import PLATE_RECOGNIZER_TOKEN, PLATE_RECOGNIZER_API_URL, REGIONS

class OCRService:
    """
    שירות לזיהוי לוחיות רישוי באמצעות PlateRecognizer API
    """
    
    def __init__(self):
        """אתחול השירות"""
        self.token = PLATE_RECOGNIZER_TOKEN
        self.api_url = PLATE_RECOGNIZER_API_URL
        self.regions = REGIONS
    
    def recognize_plate(self, image_file):
        """
        זיהוי לוחית רישוי מתמונה
        
        Args:
            image_file: קובץ התמונה (בינארי)
            
        Returns:
            dict: תוצאות הזיהוי או None אם נכשל
        """
        try:
            # שליחת התמונה ל-API
            response = requests.post(
                self.api_url,
                data=dict(regions=self.regions),
                files=dict(upload=image_file),
                headers={'Authorization': f'Token {self.token}'},
                timeout=30  # הגדרת timeout למניעת תקיעות
            )
            
            # בדיקת תקינות התגובה
            if response.status_code == 200 or response.status_code == 201:  # תגובה תקינה
                result = response.json()
                # print(f"תוצאת זיהוי לוחית: {result}")
                return result
            else:
                print(f"שגיאה בזיהוי לוחית: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.Timeout:
            print("פסק הזמן לזיהוי לוחית הסתיים")
            return None
        except requests.exceptions.ConnectionError:
            print("שגיאת חיבור בזיהוי לוחית")
            return None
        except Exception as e:
            print(f"שגיאה בזיהוי לוחית: {e}")
            return None
    
    def extract_ocr_results(self, ocr_result):
        """
        חילוץ תוצאות מפורטות מתוצאות ה-OCR
        
        Args:
            ocr_result: תוצאות ה-OCR מה-API
            
        Returns:
            dict: מילון עם שני מפתחות:
                'full_plates': רשימת מספרי לוחיות מלאים שזוהו
        """
        result = {
            'full_plates': [],
        }
        
        # בדיקה אם יש תוצאות
        if not ocr_result or 'results' not in ocr_result:
            return result
        
        # עיבוד כל התוצאות
        for plate_result in ocr_result['results']:
            plate_text = plate_result.get('plate', '').replace('-', '').replace(' ', '')
            
            # הוספת הלוחית המלאה
            if plate_text:
                # ניקוי ואחידות מספר הלוחית
                # plate_text = self._normalize_plate_number(plate_text)
                if plate_text and plate_text not in result['full_plates']:
                    result['full_plates'].append(plate_text)
                    
        return result
    
    def _normalize_plate_number(self, plate_text):
        """
        נרמול מספר לוחית רישוי
        
        Args:
            plate_text: טקסט הלוחית
            
        Returns:
            str: מספר לוחית מנורמל
        """
        # הסרת תווים לא רצויים
        plate_text = ''.join(c for c in plate_text if c.isalnum())
        
        # אם הלוחית מכילה יותר מדי או מעט מדי תווים, ייתכן שזו שגיאת זיהוי
        if len(plate_text) < 5 or len(plate_text) > 10:
            return plate_text
        
        # זיהוי לוחיות ישראליות טיפוסיות
        # אם יש מספר 7 או 8 ספרות, זו כנראה לוחית ישראלית חדשה
        if len(plate_text) in [6, 7, 8] and plate_text.isdigit():
            # פורמט לוחית ישראלית חדשה: XX-XXX-XX
            if len(plate_text) == 7:
                return plate_text[:2] + '-' + plate_text[2:5] + '-' + plate_text[5:]
            elif len(plate_text) == 8:  # 8 ספרות
                return plate_text[:3] + '-' + plate_text[3:5] + '-' + plate_text[5:]
            else:  # 6 ספרות
                return plate_text[:2] + '-' + plate_text[2:5] + '-' + plate_text[5:]
        
        return plate_text
