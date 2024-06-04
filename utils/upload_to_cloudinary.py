import cloudinary.uploader
import os
import requests


ML_MODEL_URL = os.environ.get('ML_MODEL_URL')

def upload_image(image):
    try:
        result = cloudinary.uploader.upload(image)
        return result.get('url')
    except Exception as e:
        raise RuntimeError("Request failed: {e}")


def convert_image_to_text(image_file):
    try:
        image_file.seek(0)
        
        files = {'file': ('image.jpg', image_file, 'image/jpeg')}
        
        request_url = ML_MODEL_URL + "/predict" 
        
        response = requests.post(request_url, files=files)
        
        response.raise_for_status()
        response_json = response.json()
        return response_json.get('text')
    except requests.exceptions.RequestException as e:
         raise RuntimeError("Request failed: {e}")
    except Exception as e:
        raise RuntimeError(f"Request failed: {e}")
  
    