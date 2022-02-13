import sys, time
import PIL, PIL.ImageGrab, PIL.ImageOps
import pytesseract
#import cv2
#import numpy as np
import re
import string
import json
from typing import Union

print("#" * 20)
print("# MAKE SURE CHROME IS MAXIMISED ON THE LEFT SCREEN")
print("#" * 20)

with open("config.json", "r") as f:
    config = json.load(f)
    config = config["stan_6n22_chrome"] # Current configuration we're using

# valid regexes
re_full = re.compile(config["re_full"])

# sanity settings
allowed_teams = ["FRA", "IRE"] # pulled from db

def sanity_check(items: dict) -> Union[bool, dict]:
    """
    make sure our numbers make some sense, so mins 0-95 etc
    """
    return True

def scorebox_parse(im: PIL.Image.Image) -> Union[int, dict]:
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
        if sanity_check(items) is True:
            items.update({
                "print": f'Time={items["mins"]}:{items["secs"]}, {items["home"]}={items["score_h"]} and {items["away"]}={items["score_a"]}'
            })
            return items
        else:
            return False # TODO return the reason for this
    else:
        return False

def send_to_api(payload: dict) -> bool:
    """
    send payload to the api to update the time and scores (if a valid payload)

    will also obviously be checked on the api side
    """
    pass

def watch(bbox: list) -> None:
    """
    Called every 5s for now

    Grabs the portion of the scorebox
    """
    
    im = PIL.ImageGrab.grab(bbox).convert("RGB")
    #im_inv = PIL.ImageOps.invert(im)

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

    use_bbox = config["bbox"]["score"]

    while True:
        try:
            watch(bbox=use_bbox)
            time.sleep(5)
        except KeyboardInterrupt:
            break
    print("Exiting")