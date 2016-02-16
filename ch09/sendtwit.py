#@PydevCodeAnalysisIgnore# 
# -*- coding: utf-8 -*-

import simplejson as json

APP_KEY    = "h7z1Th6xwhiftyR1r1HDxA"
APP_SECRET = "SJRvUNJ5miUVIeKXS1td8lqTHPrjhkRxsFiIk5bzFw"

OAUTH_TOKEN    = "49258051-GZoHG2w1pBARHFXRS5Nc4KwGCvJxF0M3CDrBAYOz7"
OAUTH_TOKEN_SECRET = "hUKCYuIZL9rlVAUs0xGHU3K5HHV6AA6bkGX6fAGnfa0"



from twython import Twython, TwythonError

try:
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    photo = open('Desert.jpg', 'rb')

    response = twitter.upload_media(media=photo)
    twitter.update_status(status='twit with image!', media_ids=[response['media_id']])

    print (json.dumps(response, indent=2, sort_keys=True))
    
except TwythonError as e:
    print (e)
    
except IOError as e:
    print (e)
    
   





