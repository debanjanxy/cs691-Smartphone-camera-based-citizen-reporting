#!/usr/bin/python3
import json
import subprocess
import os
import sys


def run_rest_api(img_name):
	path = os.getcwd()
	f = open('res.json','w')
	p = subprocess.Popen(['curl', '-X', 'POST', '-F', 'image=@'+path+'/results/'+img_name, 
		'https://api.openalpr.com/v2/recognize?recognize_vehicle=1&country=in&secret_key=sk_DEMODEMODEMODEMODEMODEMO'],stdout=f,cwd=path)
	p.wait()


if __name__=='main':
	run_rest_api('5.jpg')
	json_data = open('res.json')
	d = json.load(json_data)
	res = d['results'][0]
	r = res['candidates']
	for i in r:
		print(i['plate'],"--> confidence: ",i['confidence'])