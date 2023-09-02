from flask_uploads import UploadSet, IMAGES, configure_uploads

photos = UploadSet('photos', IMAGES)

def upload_image(image):
    filename = photos.save(image)
    return filename

def delete_image(filename):
    photos.delete(filename)
