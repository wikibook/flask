#@PydevCodeAnalysisIgnore# 
# -*- coding: utf-8 -*-

import simplejson as json

# photolog_app : https://twitter.com/photolog_app
APP_KEY    = "966cQr7e1mPx6Axt20uh5gwfR"
APP_SECRET = "HLWQg8DtgMfnEArsnHsIX0DfetozH16vfMNh49nwH4hu1VdVH6"

ACCESS_TOKEN    = "710801291467837440-O5C9nOg5qEgkSrdKRwbgySBF3n1X4Uk"
ACCESS_TOKEN_SECRET = "XPbD15a3cidJ7tjQtXuKc3kUHyHiy1PIdzfFQgaJcQoZj"




from twython import Twython, TwythonError

try:
    twitter = Twython(APP_KEY, APP_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    photo = open('Desert.jpg', 'rb')

    response = twitter.upload_media(media=photo)
    twitter.update_status(status='twit with image!', media_ids=[response['media_id']])

    print (json.dumps(response, indent=2, sort_keys=True))
    
except TwythonError as e:
    print (e)
    
except IOError as e:
    print (e)
    
   





