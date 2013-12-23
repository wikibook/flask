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
    result = twitter.update_status_with_media(status='twit with image!', media=photo)

    print json.dumps(result, indent=2, sort_keys=True)
    
except TwythonError as e:
    print e
    
except IOError as e:
    print e
    
# auth_tokens = twitter.get_authorized_tokens(oauth_verifier)
# print auth_tokens


# auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
# auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
# api = tweepy.API(auth)
# 
# dirpath = os.path.dirname(os.path.abspath(__file__))
# file_path = dirpath + "jobs.jpg"
# api.status_update_with_media(file_path, status='Stay hungry, stay foolish')



# api.update_status("test twit!");
# api = setup_api()
# dir = os.path.dirname(os.path.abspath(__file__))
# file_path = os.path.join(dir, 'data', 'sample.png')
# status = 'Test Media Upload'
# api.status_update_with_media(file_path, status=status)
    





