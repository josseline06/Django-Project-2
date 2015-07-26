from django.core.files.storage import FileSystemStorage
from django_gravatar import helpers as gravatar
from django.conf import settings
import os

# Almacenar imagenes en Profile:
class MyFileSystemStorage(FileSystemStorage):
	def get_available_name(self, name):
		if os.path.exists(self.path(name)):
			os.remove(self.path(name))
		return name

# Retorna ruta de archivo:
def upload_file(instance, filename):
	os.rename(filename, gravatar.calculate_gravatar_hash(instance.email))
	return os.path.join("avatars", filename)