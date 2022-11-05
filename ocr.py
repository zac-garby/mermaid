import time
import cv2
import pytesseract
import re
import numpy as np
import math

NGRAM_NMIN = 2
NGRAM_NMAX = 6
CLEANUP_REGEX = re.compile("[^a-z ]")

pages = [
    "did you ever go to silversands on a sunny summers day then perhaps you saw the mermaid who sand in the deep blue bay she sang to the fish in the ocean to the haddock the hake and the ling and they flashed their scales and swished their tails to hear the mermaid sing",
    "and sometimes the singing mermaid swam to the silvery shore she sat and combed her golden hair and then she sang some more she sang to the cockles and mussels she sang to the birds on the wing and the seashells clapped and the seagulls flapped to hear the mermaid sing",
    "when sam slys circus came to town sam took a stroll by the sea he heard the mermaid singing and he rubbed his hands with glee he said i can make you famous i can make you rich he said you shall swim in a pool of marble and sleep on a fine leather bed you shall sing for the lords and the ladies you shall sing for the queen and the king and young and old will pay good gold to hear the mermaid sing",
    "dont go dont go cried the seagulls and the seashells warned he lies but the mermaid listened to old sam sly and smiled as she waved her goodbyes",
    "and he took her away to the circus and she sand to the crowds round the ring and more more more came the deafening roar when they heard the mermaid sing",
    "now the mermaid shared a caravan with annie the acrobat and ding and dong the circus dogs and bella the circus cat and she made good friends with the jugglers and the man who swallowed fire and the clown with the tumbledown trousers and the woman who walked on wire",
    "but she wasnt friends with old sam sly no she didnt care for him for he made her live in a fish tank where there wasnt room to swim and there was no pool of marble there was no feather bed and when she begged him set me free he laughed and shook his head",
    "all summer long the circus toured all autumn winter spring and many a crowd cheered long and loud to hear the mermaid sing",
    "but the mermaid dreamed of silversands and she longed for the deep blue sea and her songs grew sad and again she said i beg you set me free but again he laughed and shook his head and he told her no such thing here you will stay while people pay to hear the mermaids sing",
    "at silversands a seagull was flying to his nest when on the breeze he heard a song the song which he loved the best and he followed the song to the caravan sam sly was about to lock it the seagull watched as he turned the key and slipped it inside his pocker",
    "the seagull waited till sam had gone then he perched on the windowsill and taptaptap at the window he tapped with his yellow bill come back come back to silversands its only a mile away i can find the key and set you free if youll come back home to the bay escape barked the dogs escape miaowed the cat but the mermaid sighed id fail for how could i walk to silversands what i only have a tail",
    "like this cried annie the acrobat and she stood upon her hands this is the way the only way to get to silversands right hand left hand tail up high theres really nothing to it if i give you lessons every night youll soon learn how to do it",
    "next week while sam was snoring the seagull stole the key he carried it off to the caravan and set the mermaid free and he flew ahead to guide her as she walked upon her hands all along the moonlit road that led to silversands",
    "and the creatures on the seashore and the fish beneath the foam jumped and splashed and danced with joy to have their mermaid home and she sang to the cockles and mussels she sang to the birds on the wing and the seashells clapped and the seagulls flapped to hear the mermaid sing",
    "and if you go down to silversands and swim in the bay of blue perhaps youll see the mermaid and perhaps shell sing for you",
]

def find_ngrams(s):
    ngrams = {}
    
    for n in range(NGRAM_NMIN, NGRAM_NMAX+1):
        for i in range(len(s) - n):
            ngram = s[i:i+n]
            if ngram not in ngrams:
                ngrams[ngram] = 1
            else:
                ngrams[ngram] += 1
    
    return ngrams

def cleanup(s):
    return re.sub(CLEANUP_REGEX, "", s.lower())

def similarity(ngrams1, ngrams2):
    s = 0
    
    for (ngram, count) in ngrams1.items():
        if ngram in ngrams2:
            s += count * ngrams2[ngram]
        else:
            s -= count
    
    return s

def match(text):
    clean = cleanup(text)
    test_ngrams = find_ngrams(clean)
    sims = enumerate([ similarity(test_ngrams, page_ngrams) for page_ngrams in ngrams ])
    return max(sims, key = lambda p: p[1])

ngrams = [ find_ngrams(page) for page in pages ]

def calibrate(vc):
    corners = []
    rval, frame = vc.read()
    
    def handleClick(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN and len(corners) < 4:
            corners.append((x, y))
            
            cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
            
            if len(corners) > 1:
                cv2.line(frame, corners[-1], corners[-2], (0, 0, 255), 2)
            if len(corners) == 4:
                cv2.line(frame, corners[0], corners[3], (0, 0, 255), 2)

            cv2.imshow("Calibrate", frame)
    
    cv2.namedWindow("Calibrate")
    cv2.setMouseCallback("Calibrate", handleClick)
    cv2.imshow("Calibrate", frame)
    cv2.waitKey(1)
    
    while len(corners) < 4:
        cv2.waitKey(1)
    
    cv2.imshow("Calibrate", frame)
    print("got corners")
    
    
    cv2.destroyWindow("Calibrate")
    
    return corners

def makePerspectiveTransform(c):
    height = int(math.sqrt((c[2][0] - c[1][0]) * (c[2][0] - c[1][0]) + (c[2][1] - c[1][1]) * (c[2][1] - c[1][1])))
    width = height * 2
    points2 = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
    M = cv2.getPerspectiveTransform(np.asarray(c, dtype=np.float32), points2)
    return (M, width, height)

def main():
    cv2.namedWindow("Preview")
    vc = cv2.VideoCapture(1)
    
    if vc.isOpened():
        rval, frame = vc.read()
        rval, frame = vc.read()
        time.sleep(1)
    else:
        print("Could not open webcam stream")
        return
    
    corners = calibrate(vc)
    print("calibrated")
    (M, width, height) = makePerspectiveTransform(corners)
    
    while rval:
        rval, frame = vc.read()
        corrected = cv2.warpPerspective(frame, M, (width, height))
        cv2.imshow("Preview", corrected)
        text = pytesseract.image_to_string(corrected)
        print(cleanup(text))
        page, _ = match(text)
        print("page", page + 1)
        print()
        cv2.waitKey(1)
    
    vc.release()
    cv2.destroyWindow("Preview")

if __name__ == "__main__":
    main()