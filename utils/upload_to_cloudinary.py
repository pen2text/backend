import cloudinary.uploader


def upload_image(image):
    try:
        result = cloudinary.uploader.upload(image)
        return result.get('url')
    except Exception as e:
        return None