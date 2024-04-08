import cloudinary.uploader

def upload_image(image_file):

    upload_result = cloudinary.uploader.upload(image_file)
    return upload_result