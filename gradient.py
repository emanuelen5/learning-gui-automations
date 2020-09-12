import cv2
import numpy as np

def gradient(img):
    sobelx = cv2.Scharr(img, cv2.CV_64F, 1, 0)
    sobely = cv2.Scharr(img, cv2.CV_64F, 0, 1)
    amp = np.sqrt(np.power(sobelx, 2) + np.power(sobely, 2))
    orien = cv2.phase(np.array(sobelx), np.array(sobely))
    return amp, orien
