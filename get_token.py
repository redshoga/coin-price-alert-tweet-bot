import tweepy
import json

consumer_file = open("./consumer.json", "r")
key = json.load(consumer_file)
auth = tweepy.OAuthHandler(key["CONSUMER_KEY"], key["CONSUMER_SECRET"])

try:
    redirect_url = auth.get_authorization_url()
    print(redirect_url)
    verifier = input('oauth_verifier:')
    auth.get_access_token(verifier)


    token = {
        "ACCESS_TOKEN": auth.access_token,
        "ACCESS_TOKEN_SECRET": auth.access_token_secret
    }
    token_file = open("./token.json", "w")
    json.dump(token, token_file)

    print('Success!')

except tweepy.TweepError:
    print('Error!')
