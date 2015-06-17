from nap.url import Url
import requests
import hmac
import sys
import simplejson as json
from hashlib import sha1


brightness = int(sys.argv[1])

class JsonApi(Url):
    def after_request(self, response):
        if response.status_code != 200:
            return response.json()
            # response.raise_for_status()

        return response.json()

api_url = 'http://mafreebox.freebox.fr/api/v3/'
api = JsonApi(api_url)

app_token = u'kg2QlhFxsQznwnce+yMoftHLsGkEJfNZxFndAdsL15V5KGH9bEgNQUIZkdYE85wR'
app_id = "fr.freebox.brightness"

# print(api.post('/login/authorize', json = {
#   "app_id": "fr.freebox.brightness",
#   "app_name": "Freebox Brightness",
#   "app_version": "0.0.2",
#   "device_name": "Pc de Benoit"
# }))
# {u'result': {u'app_token': u'kg2QlhFxsQznwnce+yMoftHLsGkEJfNZxFndAdsL15V5KGH9bEgNQUIZkdYE85wR', u'track_id': 1}, u'success': True


# 1st stage: get challenge*

# resp = api.get('/login/authorize/1')
# print(resp)

resp = api.get('/login/')
if resp['success']:
    if not resp['result']['logged_in']:
        challenge = resp['result']['challenge']

# 2nd stage: open a session

# Hashing token with key
password = hmac.new(str(challenge), str(app_token), digestmod=sha1).hexdigest()
print(password)
password = hmac.new(str(app_token), str(challenge), digestmod=sha1).hexdigest()
print(password)

resp = api.post('/login/session/', json = {
        'app_id': str(app_id),
        'password': password,
    })

session_token = resp['result']['session_token']
print(session_token)

print(api.put('lcd/config/', json={'brightness': brightness}, headers={ 'X-Fbx-App-Auth': session_token }))
