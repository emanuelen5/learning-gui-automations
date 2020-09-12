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

print("Listing monitors")
for m in get_monitors():
    print(str(m))
monitor = get_monitors()[0]

print(f"Using first monitor: {str(monitor)}")

with Timer("MSS"):
    sct = mss.mss()
    mon = dict(top=monitor.y, left=monitor.x, width=monitor.width, height=monitor.height, monitor=1)
    img = np.asarray(sct.grab(mon), dtype=np.uint8)
    img = img[:,:,0:3]

img_gray = cv2.cvtColor(cv2.cvtColor(img.copy(), cv2.COLOR_RGB2GRAY), cv2.COLOR_GRAY2RGB)

with Timer("Read"):
    template = cv2.imread("close_button.png")

with Timer("Array"):
    img = np.asarray(img)

print("Searching")

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

rect_gray1 = img_gray.copy()
with Timer("NMS"):
    bb_locs = []
    h, w, _ = template.shape
    # Transform to x1, x2, y1, y2 points first
    for idx, pt in enumerate(locations):
        x1 = pt[0]
        x2 = x1 + w
        y1 = pt[1]
        y2 = y1 + h
        bb_locs.append([x1, y1, x2, y2])
    nonmaxed = nms.non_max_suppression_fast(np.array(bb_locs), 0.2)
    for pt in nonmaxed:
        print(f"Found: {pt}")
        cv2.rectangle(rect_gray1, (pt[0], pt[1]), (pt[0] + w, pt[1] + h), (255, 0, 0), 1)

fig = plt.figure()
ax = fig.subplots()
ax.imshow(rect_gray1, vmin=-1, vmax=1)
ax.set_title("Nonmax suppression")

print(f"Min: {dec_min}, Max: {dec_max}")

print(f"Found regions: {len(locations)}")
if len(locations) == 0:
    sleep_time = 0.5
else:
    sleep_time = 0.5 / len(locations)

rect_gray = img_gray.copy()
h, w, _ = template.shape
for idx, pt in enumerate(locations):
    print(f"Found: {pt}")
    cv2.rectangle(rect_gray, pt, (pt[0] + w, pt[1] + h), (255, 0, 0), 1)
    if len(locations) < 10:
        mouse.move(pt[0] + w / 2, pt[1] + h / 2, duration=sleep_time)
        time.sleep(sleep_time)

fig: plt.Figure = plt.figure()
ax: plt.Axes = fig.subplots()
ax.imshow(rect_gray)
ax.set_title("Detections in screenshot")
plt.show()
