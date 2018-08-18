import random, string
from django.conf import settings
from .validators import validate_file_extension

def handle_uploaded_file(file_to_upload):
	N = 20
	generated_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=N))
	generated_filename += validate_file_extension(file_to_upload)
	with open(settings.MEDIA_ROOT+generated_filename, 'wb+') as destination:
		for chunk in file_to_upload.chunks():
			destination.write(chunk)
		destination.close()
	return generated_filename