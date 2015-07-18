from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, Group
from .models import Profile

import re

def get_user(backend, strategy, details, response, user=None, *args, **kwargs):
	social = UserSocialAuth.objects.filter(uid=response['id'])

	if social.count() == 0:
		if backend.name === 'twitter':
			return JsonResponse({"response": "email is required to verify"})
		reg_user = User.objects.filter(email=response['email'])
		if reg_user.count() == 0: # Usuario nuevo
			UserSocialAuth.objects.create()

"""	
if backend.name == 'facebook':
	url = "http://graph.facebook.com/%s/picture?type=large"%response['id']
elif backend.name == 'twitter' and response['default_profile_image'] == False:
	url = response['profile_image_url'].replace('_normal','')
elif backend.name == 'google-oauth2':
	url = re.sub('\?sz=.+', '', response['image']['url'])
else:
	print "ERROR!"
print url
print response['id']

return HttpResponseRedirect(url)
"""
