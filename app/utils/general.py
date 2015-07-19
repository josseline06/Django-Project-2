# Genera un nombre clave 
def create_key_name(string):
	result = string.lowercase()
	return result.replace(' ', '_')