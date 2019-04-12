import os
import cv2 
import numpy as np
import math
import scipy.stats 
import pickle
Theshold = 100
jointThre = 0.0004
maskThreLow = 2.6  # 2.8
maskThreHigh = 0.8

def hasTable(img, joint):
	if np.mean(joint) < jointThre:
		if np.mean(img) >= maskThreLow:
			return True
		return False
	elif np.mean(img) < maskThreHigh:
		return False
	return True

def getTableFromImage(img, h_size=-1, v_size=-1):
    if len(img.shape) == 2:
        gray_img = img
    elif len(img.shape) == 3:
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    thresh_img = cv2.adaptiveThreshold(~gray_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2)

    h_img = thresh_img.copy()
    v_img = thresh_img.copy()
    scale = 15 # play around with this

    if h_size == -1:
        h_size = int(h_img.shape[1]/scale)

    h_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (h_size,1))
    h_erode_img = cv2.erode(h_img,h_structure, 1)

    h_dilate_img = cv2.dilate(h_erode_img,h_structure, 1)

    if v_size == -1:
	    v_size = int(v_img.shape[0] / scale)

    v_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, v_size))
    v_erode_img = cv2.erode(v_img, v_structure, 1)
    v_dilate_img = cv2.dilate(v_erode_img, v_structure, 1)

    mask_img = h_dilate_img + v_dilate_img
    joints_img = cv2.bitwise_and(h_dilate_img, v_dilate_img)

    return mask_img, joints_img

def normalDistribution(x,m,sd):
    return scipy.stats.norm(m, sd).pdf(x)

def getMean(array):
	result = 0.0
	for i in array:
		result +=i
	return result/len(array)

def getVariance(array,mean):
	result = 0.0
	n = len(array)
	for i in array:
		result += (i-mean)*(i-mean)
	if n < 30:
		print(result)
		return math.sqrt(result/(n-1))
	else:
		return math.sqrt(result/n)

def getDistance(A, B):
	newA = np.copy(A)
	newB = np.copy(B)
	if len(newA.shape) != 1:
		newA = A.flatten()
	if len(newB.shape) != 1:
		newB = B.flatten()
	if newA.shape == newB.shape:
		return np.linalg.norm(newA-newB)/len(newA)
	else:
		return None

def reshapeImage(image, width=2500, hight=3300):
	return cv2.resize(image,(width,hight))

def checkMap(distance,m,v):
	p = normalDistribution(distance,m,v)
	if p > Theshold:
		return True
	else:
		return False