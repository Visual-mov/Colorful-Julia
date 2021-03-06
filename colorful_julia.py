from juliaset import JuliaSet
from random import uniform, randint
from time import tzname
import sys, os, tweepy

# Colorful Julia Twitter bot
# Copywrite(c) Ryan Danver 2019
# Check out the bot! -> https://twitter.com/colorjulia_bot

# Parameters
C_LIMIT = (-1,1)
(WIDTH, HEIGHT) = (1000,1000)
ITER_RANGE = (50, 200)
ZOOM = 1.8
DECIMALS = 4

COLOR_MODES = ("rand_color", "rand_pattern", "rand_glow", "multi_color")

def main(argv):
    date_img = False
    tweet_img = True
    img_path = "saves"
    if len(argv) > 1:
        i = 1
        while i < len(argv):
            if argv[i] == "--date_img":
                date_img = True
            elif argv[i] == "--no_tweet":
                tweet_img = False
            elif argv[i] == "--path":
                if i != len(argv)-1:
                    i+=1
                    img_path = argv[i]
            else:
                print("Unknown parameter: " + argv[i])
                exit()
            i+=1

    ca = round(uniform(C_LIMIT[0],C_LIMIT[1]), DECIMALS)
    cb = round(uniform(C_LIMIT[0],C_LIMIT[1]), DECIMALS)

    set = JuliaSet(ca, cb, WIDTH, HEIGHT, COLOR_MODES[randint(0,len(COLOR_MODES)-1)], date_img)

    max_iterations = randint(ITER_RANGE[0],ITER_RANGE[1])
    set.genImage(max_iterations, ZOOM)
    set.saveImage(img_path)

    if tweet_img:
        keys = list(getkeys())
        auth = tweepy.OAuthHandler(keys[0],keys[1])
        auth.set_access_token(keys[2],keys[3])
        api = tweepy.API(auth)
        try:
            status = f"Julia set generated on {set.date_stamp} at {set.time_stamp} {tzname[0]}\nIterations: {max_iterations}\nColoring mode: \"{set.c_mode}\"\nc = {ca} + {cb}i"
            api.update_with_media(f"{img_path}/{set.file_name}",status)
            print("Successfully tweeted.")
        except tweepy.TweepError as e:
            print(f"Tweepy error:\n{e.reason}")

def getkeys():
    try: 
        lines = open(f"{os.path.dirname(os.path.realpath(__file__))}/keys.txt",'r').readlines()
        for i in range(len(lines)):
            if i < 4:
                yield lines[i].replace('\n','')
    except FileNotFoundError:
        print("keys.txt not found. Please see README.md")
        exit()

if __name__ == "__main__":
    main(sys.argv)
