from juliaset import JuliaSet
from random import uniform, randint
from time import tzname
import sys, os, tweepy

# Colorful Julia Twitter bot
# Copywrite(c) Ryan Danver 2019
# Check out the bot! https://twitter.com/colorjulia_bot

# Parameters
C_LIMIT = (-1,1)
(WIDTH, HEIGHT) = (1000,1000)
ITERATIONS = 200
ZOOM = 1.8

COLOR_MODES = ("rand_color", "rand_pattern", "rand_glow")

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
    set = JuliaSet(ca, cb, WIDTH, HEIGHT, COLOR_MODES[randint(0,len(COLOR_MODES)-1)], date_img)
    set.genImage(ITERATIONS, ZOOM)
    set.saveImage(path)

    if tweet_img:
        keys = getkeys(tweet_img)
        auth = tweepy.OAuthHandler(keys[0],keys[1])
        auth.set_access_token(keys[2],keys[3])
        api = tweepy.API(auth)
        try:
            status = f"Julia set generated on {set.date_stamp} at {set.time_stamp} {tzname[0]}\nIterations: {ITERATIONS}\nColoring mode: \"{set.c_mode}\"\nc = {ca} + {cb}i"
            api.update_with_media(f"{path}/{set.file_name}",status)
            print("Successfully tweeted.")
        except tweepy.TweepError as e:
            print(f'Tweepy error:\n  {e.reason}')

def getkeys(tweet_img):
    keys = [''] * 4
    if not tweet_img: return keys
    try: 
        lines = open("keys.txt",'r').readlines()
        for i in range(len(lines)):
            if i < len(keys): keys[i] = lines[i]
    except FileNotFoundError:
        print("keys.txt not found. Please see README.md")
        exit()
    keys = [key.replace('\n','') for key in keys]
    return keys 

if __name__ == "__main__":
    main(sys.argv)
