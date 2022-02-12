import sys, time
import PIL, PIL.ImageGrab, PIL.ImageOps
import pytesseract
#import cv2
#import numpy as np
import re
import string

#from reader import reader

# Text detection

print("#" * 20)
print("# MAKE SURE CHROME IS MAXIMISED ON THE LEFT SCREEN")
print("#" * 20)

# TODO see if we can get the coordinates of the chrome window, (will be useful for exapunks minigame solver)
chrome_box = (60,130,1920,1200)
score_box = (430,200,805,265)

# valid regexes
re_full = re.compile("(?P<mins>\d{2})\:(?P<secs>\d{2})\s+(?P<home>\w{3})\s+(?P<score_h>\d+)\-(?P<score_a>\d+)\s+(?P<away>\w{3})")

def scorebox_parse(im):
    text = pytesseract.image_to_string(im).strip()
    if not text or text == "":
        return False

    # proper filter
    allowed = set("".join([string.ascii_uppercase, string.digits, ":", "-", " "]))
    text = "".join(filter(lambda x: x in allowed, text))

    # print(text)
    m = re_full.match(text)
    if m is None:
        return False

    if len(m.groups()) == 6:
        # Found all the info we need
        items = m.groupdict()
        items.update({
            "print": f'Time={items["mins"]}:{items["secs"]}, {items["home"]}={items["score_h"]} and {items["away"]}={items["score_a"]}'
        })
        return items
    else:
        return False
    # print(len(m.groups()), m.groupdict())
    # print(dir(m))


def watch():
    
    im = PIL.ImageGrab.grab(score_box).convert("RGB")
    im_inv = PIL.ImageOps.invert(im)

    score = scorebox_parse(im)
    if not score:
        print("- No score detected properly")
    else:
        print(score["print"])

    #im.show()
    # convert im to cv2
    #cv_im = np.asarray(im_inv)
    #print(cv_im.shape)
    # grayscale? slash threshold

    #im2 = PIL.Image.fromarray(cv_im)
    #im2 = im.crop()
    #print(cv_im.shape)
    #im.save("idktest.png")
    #print(cv_im[1:2])
    # cv2.imshow("cv", cv_im)
    #im2.show()

if __name__ == "__main__":

    # Input match ID so we can call the api too
    mid = False
    if len(sys.argv) == 1:
        print("Remember to add a mid")
    else:
        mid = int(sys.argv[1])

    while True:
        try:
            watch()
            time.sleep(5)
        except KeyboardInterrupt:
            break
    print("Exiting")