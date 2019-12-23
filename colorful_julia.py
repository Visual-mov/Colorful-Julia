from juliaset import JuliaSet
from random import uniform, randint
from time import tzname
import sys
import tweepy

# Colorful Julia Twitter bot
# Copywrite(c) Ryan Danver 2019
# Go check out the bot: https://twitter.com/colorjulia_bot

# Parameters
C_LIMIT = (-1,1)
RESOLUTION = (1000,1000)
ITERATIONS = 200
ZOOM = 1.8

COLOR_MODES = ("rand_color", "rand_pattern", "rand_glow")

# Twitter API
# REPLACE WITH YOUR OWN KEYS
key = "rw2HSv43rXegHzE9waeAAAzJZ"
key_secret = "BUhErximdlCOTIji97heDUsY1Ll4142XwkqGaIYUTy2lEN5s1L"
token = "1205741908590383104-zUg0S1qE8JHzTzE4DX634sqSomry4t"
token_secret = "ke3TScAe7suDsEZFfpmdg67L65b3ItacG2uLOnOyBsVlg"

def main(argv):
    date_img = False
    tweet_img = True
    path = "saves"
    if len(argv)-1 > 0:
        i = 1
        while i < len(argv):
            if argv[i] == "--date_img":
                date_img = True
            elif argv[i] == "--no_tweet":
                tweet_img = False
            elif argv[i] == "--path":
                if i != len(argv)-1:
                    i+=1
                    path = argv[i]
            else:
                print("Unknown parameter: " + argv[i])
                exit()
            i+=1

    ca = uniform(C_LIMIT[0],C_LIMIT[1])
    cb = uniform(C_LIMIT[0],C_LIMIT[1])
    set = JuliaSet(ca, cb, RESOLUTION, COLOR_MODES[randint(0,len(COLOR_MODES)-1)], date_img)
    set.genImage(ITERATIONS, ZOOM)
    set.saveImage(path)

    if tweet_img:
        auth = tweepy.OAuthHandler(key,key_secret)
        auth.set_access_token(token,token_secret)
        api = tweepy.API(auth)
        try:
            status = f"Julia set generated on {set.date_stamp} at {set.time_stamp} {tzname[0]}\nIterations: {ITERATIONS}\nColoring mode: \"{set.c_mode}\"\nc = {ca} + {cb}i"
            api.update_with_media(f"{path}/{set.file_name}",status)
            print("Successfully tweeted.")
        except tweepy.TweepError as e:
            print(e.reason)

if __name__ == "__main__":
    main(sys.argv)