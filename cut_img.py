#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys
import json
from bs4 import BeautifulSoup
import requests
from urllib import FancyURLopener
from PIL import Image
from PIL import ImageChops
import math
from fake_useragent import UserAgent




def compare(file1, file2):
	image1 = Image.open(file1).convert('L')
	image2 = Image.open(file2).convert('L')
	diff = ImageChops.difference(image1, image2)
	h = diff.histogram()
	sq = (value*(idx**2) for idx, value in enumerate(h))
	sum_of_squares = sum(sq)
	rms = math.sqrt(sum_of_squares/float(image1.size[0] * image1.size[1]))
	return rms

def getprice(divlist,selectors_dictionary):
	price = ''
	yval = 0
	xval = 0
	j=0
	#os.system('rm *.png')
	#print divlist
	for div in divlist:
		classy= str(div).replace('<div class="','').replace('/','').replace('div','').replace('<>','').replace('$','').replace('">','').split(' ')
		widthslist = []
		for classed in classy:
			#try:
			dict_key = '.'+classed.replace('\xa0','').replace('\xc2','')
			#print dict_key, selectors_dictionary[dict_key]

			try:
				yval = selectors_dictionary[dict_key]['bp-yval']
			except:
				pass
			try:
				xval = selectors_dictionary[dict_key]['bp-xval']
			except:
				pass
			try:
				width = selectors_dictionary[dict_key]['bp-width']
				widthslist.append(width)
			except:
				pass
			try:
				height = selectors_dictionary[dict_key]['bp-height']
			except:
				pass

		if str(yval) =='2': #white tiles

			small_str='tile_'+str(j)+'.png'

			complist = []
			width = min(widthslist)
			cmd = 'convert '+str(big_img)+' -crop '+str(width)+'x'+str(height)+'+'+str(xval)+'+'+str(yval)+' '+str(small_str)
			os.system(cmd)
			k=0
			for k in range(0,10):
				if width =='7':
					compimg = 'img/true'+str(k)+'.png'
					diff = compare(compimg,small_str)
					#print 'comparing '+str(small_str)+' to '+str(compimg),diff
					complist.append(diff)


			if width != '3':
				price+= str(complist.index(min(complist)))
			else:
				price+= '.'

		if str(yval) =='21': #blue tiles
			small_str='tile_'+str(j)+'.png'

			yval+=4
			#yval = -1*yval
			#xval = -1*xval
			complist = []
			width = min(widthslist)

			cmd = 'convert '+str(big_img)+' -crop '+str(width)+'x'+str(height)+'+'+str(xval)+'+'+str(yval)+' '+str(small_str)
			os.system(cmd)
			k=0
			for k in range(0,10):
				if width =='7':
					compimg = 'img/trueblue'+str(k)+'.png'
					diff = compare(compimg,small_str)
					#print 'comparing '+str(small_str)+' to '+str(compimg),diff
					complist.append(diff)
			if width != '3':
				price+= str(complist.index(min(complist)))
			else:
				price+= '.'
		j+=1
#	print ''
	return price


#http://www.phpied.com/imagmagick-crop-and-center/
#https://github.com/reworkcss/css
#http://iamdustan.com/reworkcss_ast_explorer/#/U7u84Z2LOr

class MyOpener(FancyURLopener):
	version = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
myopener = MyOpener()


currentDirectory = os.getcwd()

# get image and css
search_term = 'Jeskai Ascendancy'
#print sys.argv
search_term = sys.argv[1]
scgurl = 'http://sales.starcitygames.com/search.php?substring='+search_term

ua = UserAgent(cache=False)

headers = {
    'User-Agent': ua.random
}

html_doc = requests.get(scgurl, headers=headers)

soup = BeautifulSoup(html_doc.text, "html.parser")

css = soup.style
cssurl = currentDirectory+"/css/scg_code.css"
jsonurl = currentDirectory+"/css/scg_css.json"
with open(cssurl,'w') as file:
	file.write(str(css).replace("<style>","")[:-8])

#print soup.find('td',{"class":"deckdbbody2 search_results_9"})
broke = 0 # for decimal exception

os.system('node '+currentDirectory+'/css2json.js '+str(cssurl)+'> '+jsonurl) #convert stylesheet to css AST object. uses reworkcss node module

big_img = currentDirectory+'/img/price_icons.png'
with open("css/scg_css.json","r") as file:
	jsond = json.load(file)
j=0

selectors_dictionary = {}
broke = 0
for x in jsond["stylesheet"]["rules"]:

	if x["type"] == "rule":

		for selector in x['selectors']:
			if selector not in selectors_dictionary:
				selectors_dictionary[selector] = {}

			for y in x["declarations"]:
				if(y['value']):
					if y['property']=='background-position':

						xval = int(y['value'].split(' ')[0].replace('px','').replace('-',''))
						yval = int(y['value'].split(' ')[1].replace('px','').replace('-',''))
						selectors_dictionary[selector]['bp-xval'] = xval
						selectors_dictionary[selector]['bp-yval'] = yval
					if y['property'] == 'background-image':
						big_img_url = "http://"+str(y['value'][6:-1])
						path = currentDirectory+"/img/price_icons.png"

						myopener.retrieve(big_img_url, path)

					if y['property'] == 'height':
						height = y['value'].replace('px','')
						selectors_dictionary[selector]['bp-height'] = height

					if y['property'] == 'width':
						width = y['value'].replace('px','')

						selectors_dictionary[selector]['bp-width'] = width


j=0
broke = 0
yval = 0
xval = 0
width = 0
height = 0

tdlist= soup.findAll('td')
result = {}
item={}

for ted in tdlist:
	if ted.get('class') != None:
		if str(ted.get('class')[0]) == 'deckdbbody2' or str(ted.get('class')[0]) == 'deckdbbody':  #the blueones
			if str(ted.get('class')[1]) == 'search_results_1':
				if ted.find('a') != None:
					card_name = ted.find('a').text.replace('\n','')

			if str(ted.get('class')[1]) == 'search_results_2':
				if ted.find('a') != None:
					card_set =  ted.find('a').text

			if str(ted.get('class')[1]) == 'search_results_6':
				rarity = ted.text

			if str(ted.get('class')[1]) == 'search_results_7':
				condition = ted.text

			if str(ted.get('class')[1]) == 'search_results_9':
					bigdivlist =  ted.findAll('div')
					for smalldiv in bigdivlist:
						divlist = smalldiv.findAll('div')
					#print divlist
						price = getprice(divlist,selectors_dictionary)
						if price != '':
							if card_name not in result:
								result[card_name] = {}
							if card_set not in result[card_name]:
								result[card_name][card_set] = {}
							result[card_name][card_set][condition] = price


print json.dumps(result)
