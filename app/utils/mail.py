from django.core.mail import EmailMessage
from django.template.loader import get_template

# Envio de correo
def send_email(destination, subject, variables, template):
	template_name = get_template('email/'+ template +'.text')

	to, from_email = destination , 'OWL Express <mail@owlexpress.me>'
	content = template_name.render(variables)
	msg = EmailMessage(subject, content, from_email, [to])
	msg.send()