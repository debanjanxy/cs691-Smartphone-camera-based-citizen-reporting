#!/usr/bin/python3
import cv2
import os
import sys
import subprocess
import re
import json
import time

DEMO = 'sk_DEMODEMODEMODEMODEMODEMO'
SKEY = 'sk_6a33699ea556abd4e01e2f7d'
LABELS = ['bus','truck','car','motorbike']


#get an image
def load_image():
	img_name = sys.argv[1]
	img_path = '/home/debanjan/Debanjan/GitHub/cs691/week4_6-3-18_13-3-18/data/'+img_name
	img = cv2.imread(img_path,1)
	return img_name,img


#goto /home/debanjan/darknet directory and run the command ./darknet detect cfg/yolo.cfg yolo.weights data/image.jpg
def run_yolo(img,img_name):
	#copy image into /darknet/data directory
	path = '/home/debanjan/darknet/data/'
	cv2.imwrite(os.path.join(path,'my_image.jpg'),img)
	cv2.waitKey(0)

	#executre the command and show in the terminal
	p = subprocess.Popen(['./darknet','detect','cfg/yolo.cfg', 'yolo.weights', 'data/my_image.jpg'],cwd='/home/debanjan/darknet')
	p.wait()


#get the prediction image in my current directory from /home/debanjan/darknet directory
def get_predictions():
	img_path = '/home/debanjan/darknet/predictions.png'
	img = cv2.imread(img_path,1)
	save_path = '/home/debanjan/Debanjan/GitHub/cs691/week4_6-3-18_13-3-18/'
	cv2.imwrite(os.path.join(save_path,'predictions.png'),img)
	cv2.waitKey(0)
	return

# i = 0
#get images of all the objects present in predictions.png
def get_object_images(img_name):
	pred = cv2.imread('/home/debanjan/Debanjan/GitHub/cs691/week4_6-3-18_13-3-18/data/'+img_name,1)

	#load the coordinates.txt file
	file = open("coordinates.txt",'r')

	#for each line in the file and extract top, bottom, left and right values
	i = 0
	file_names = []
	for line in file.readlines():
		tokens = line.split(',')
		label_str = tokens[0]
		label = label_str.split(':')[0]
		if label in LABELS:
			top = int(re.search(r'\d+',tokens[1]).group())
			bottom = int(re.search(r'\d+',tokens[2]).group())
			left = int(re.search(r'\d+',tokens[3]).group())
			right = int(re.search(r'\d+',tokens[4]).group())

			#slice the original image and save the portion as new image in 'result' directory
			temp = pred[top:bottom,left:right]
			cv2.imwrite('/home/debanjan/Debanjan/GitHub/cs691/week4_6-3-18_13-3-18/results/'+str(i)+'.jpg',temp)
			file_names.append(str(i)+'.jpg')
		i = i+1
	return file_names


def run_rest_api(img_name):
	path = os.getcwd()
	f = open('res.json','w')
	p = subprocess.Popen(['curl', '-X', 'POST', '-F', 'image=@'+path+'/results/'+img_name, 
		'https://api.openalpr.com/v2/recognize?recognize_vehicle=1&country=in&secret_key='+SKEY],stdout=f,cwd=path)
	p.wait()


def show_results():
	try:
		json_data = open('res.json')
		d = json.load(json_data)
		res = d['results'][0]
		r = res['candidates']
		for i in r:
			print(i['plate'],"--> confidence: ",i['confidence'])
	except:
		print("Not a vehicle!")


if __name__ == '__main__':
	init_time = time.time()
	img_name, img = load_image()
	run_yolo(img, img_name)
	get_predictions()
	file_names = get_object_images(img_name)
	for name in file_names:
		print("---------------------",name,"---------------------")
		run_rest_api(name)
		show_results()
		print("---------------------------------------------------")
	print("Total time taken (in seconds): ",time.time()-init_time)


