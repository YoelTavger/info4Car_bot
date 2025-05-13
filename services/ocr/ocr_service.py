from services.ocr.plate_recognizer import recognize_license_plate

class OCRService:
    """
    שירות לזיהוי לוחיות רישוי באמצעות OCR
    """
    
    def recognize_plate(self, image_file):
        """
        זיהוי לוחית רישוי מתמונה
        
        Args:
            image_file: קובץ התמונה (בינארי)
            
        Returns:
            dict: תוצאות הזיהוי או None אם נכשל
        """
        return recognize_license_plate(image_file)
    
    def extract_ocr_results(self, ocr_result):
        """
        חילוץ תוצאות מפורטות מתוצאות ה-OCR
        
        Args:
            ocr_result: תוצאות ה-OCR מה-API
            
        Returns:
            dict: מילון עם מפתח 'full_plates' המכיל רשימת מספרי לוחיות שזוהו
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
                if plate_text and plate_text not in result['full_plates']:
                    result['full_plates'].append(plate_text)
                    
        return result