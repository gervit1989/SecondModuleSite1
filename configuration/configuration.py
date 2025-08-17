import os
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

# Расширение файла
def get_extension(img_name:str)->str:
    ext = os.path.basename()

    ext = img_name.rsplit('.', 1)[1].lower()
    return ext

# Проверить изображение
def check_image(img_name:str):
    if is_allowed_file_format(img_name):
        if is_allowed_file_by_volume(img_name):
            return True, ''
        else:
            return False, 'Image format is correct, but size is too large'
    return False, 'Image is not correct.'

# разрешенные по расширению
def is_allowed_file_format(img_name:str):
    ext = get_extension()

    if ext in ALLOWED_EXTENSIONS:
        return True
    return False

# разрешенные по размеру
def is_allowed_file_by_volume(img_name:str):
    img_size = os.path.getsize(img_name)
    if img_size > MAX_FILE_SIZE:
        return False
    return True

# Detect if running in Docker
def is_docker():
    try:
        with open('/proc/1/cgroup', 'rt') as f:
            # returns True if the script running in Docker or Kubernetes:
            return 'docker' in f.read() or 'kubepod' in f.read()
    except FileNotFoundError:
        return False

# Получить уникальное имя
def secure_filename(filename:str)->str:
    return filename.replace('..', '').replace('/', '').replace('\\', '')

#Получить пути
def get_paths():
    # Set paths based on environment
    if is_docker():
        return '/images',  '/logs/app.log'  # Absolute path for Docker
    return 'images', 'logs/app.log'  # Relative path for non-Docker
