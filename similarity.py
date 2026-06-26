import imagehash

from PIL import Image

def get_image_hash(image_path):

    image = Image.open(image_path)

    return imagehash.phash(image)

def compare_images(hash1, hash2):

    return hash1 - hash2