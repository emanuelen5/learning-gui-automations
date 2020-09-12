import pyscreenshot as ps
import numpy as np
from timer import Timer
import gradient
import cv2
import keyboard, mouse
import time
import nms
import sys
import mss
from matplotlib import pyplot as plt
from screeninfo import get_monitors

for m in get_monitors():
    print(str(m))

with Timer("MSS"):
    sct = mss.mss()
    mon = dict(top=0, left=0, width=1920 * 2, height=1080, monitor=-1)
    printscreen = np.asarray(sct.grab(mon))


def find_template(img, template):
    h, w, _ = img.shape
    ht, wt, _ = template.shape
    matches = []
    for hi in range(h - ht + 1):
        for wi in range(w - wt + 1):
            import pdb;
            pdb.set_trace()
            if (img[hi:hi + ht, wi:wi + wt] == template).all():
                matches.append((hi, wi))
    return matches


with Timer("Read"):
    template = cv2.imread("close_button.png")

with Timer("Grab"):
    img = ps.grab()

with Timer("Array"):
    img = np.asarray(img)

print("Searching")
# matches = find_template(img, template)
# print(matches)
# sys.exit(0)

with Timer("Search"):
    detection = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.38
    loc = np.where(detection >= threshold)
    locations = list(zip(*loc[::-1]))

fig: plt.Figure = plt.figure()
ax1, ax2 = fig.subplots(2, 1, sharex=True, sharey=True)
ax1.imshow(detection, vmin=-1, vmax=1)
ax1.set_title("Detection heatmap")

strel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
detection_maxsup = cv2.dilate(detection, strel)
detection_maxsup = cv2.erode(detection_maxsup, strel)
dec_min = np.amin(detection)
dec_max = np.amax(detection)
ax2.imshow(detection_maxsup, vmin=-1, vmax=1)
ax2.set_title("Open")

fig2: plt.Figure = plt.figure()
ax1, ax2 = fig2.subplots(2, 1)
ax1: plt.Axes
ax1.hist(detection.ravel(), 512, (-1, 1), log=True)
ax2.hist(detection_maxsup.ravel(), 512, (-1, 1), log=True)

amp, orien = gradient.gradient(detection)
nonmaxed = nms.maximum(amp, orien)
fig = plt.figure()
ax = fig.subplots()
ax.imshow(nonmaxed, vmin=-1, vmax=1)
ax.set_title("Nonmax suppression")

print(f"Min: {dec_min}, Max: {dec_max}")

print(f"Found regions: {len(locations)}")
if len(locations) == 0:
    sleep_time = 0.5
else:
    sleep_time = 0.5 / len(locations)

img_gray = cv2.cvtColor(cv2.cvtColor(img.copy(), cv2.COLOR_RGB2GRAY), cv2.COLOR_GRAY2RGB)
h, w, _ = template.shape
for idx, pt in enumerate(locations):
    print(f"Found: {pt}")
    cv2.rectangle(img_gray, pt, (pt[0] + w, pt[1] + h), (255, 0, 0), 4)
    if len(locations) < 10:
        mouse.move(pt[0] + w / 2, pt[1] + h / 2, duration=sleep_time)
        time.sleep(sleep_time)

fig: plt.Figure = plt.figure()
ax: plt.Axes = fig.subplots()
ax.imshow(img_gray)
ax.set_title("Detections in screenshot")
plt.show()
