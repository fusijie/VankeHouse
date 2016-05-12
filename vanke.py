#!/usr/bin/python
# coding=utf-8

import urllib
import os
import shutil
import socket
import multiprocessing

socket.setdefaulttimeout(30)

rooms = [101, 102, 104, 105, 106, 107, 108, 109, 112]
room_dir_0 = ['b', 'd', 'f', 'l', 'r', 'u']
room_dir_1 = [{'key': 'l1', 'value': [1, 2]}, {'key': 'l2', 'value': [1, 2, 3]}, {'key': 'l3', 'value': [1, 2, 3, 4, 5, 6]}];

panos_img_info = []

def _mkdir():
	if os.path.exists('vanke/panos'):
		shutil.rmtree('vanke/panos')

	os.mkdir('vanke/panos')

	for x in rooms:
		tiles = 'vanke/panos/' + str(x) + '.tiles'
		os.mkdir(tiles)
		for y in room_dir_0:
			tiles_dir_0 = tiles + '/' + y
			os.mkdir(tiles_dir_0)
			for z in room_dir_1:
				tiles_dir_1 = tiles_dir_0 + '/' + z['key']
				os.mkdir(tiles_dir_1)
				for w in z['value']:
					tiles_dir_2 = tiles_dir_1 + '/' + str(w)
					os.mkdir(tiles_dir_2)
					for v in range(len(z['value'])):
						file_name = z['key'] + '_' + y + '_' + str(w) + '_' + str(v+1) + '.jpg'
						file_name = tiles_dir_2 + '/' + file_name
						img_url = file_name.replace('vanke', 'http://vr.yyttww.com/wkc02')
						panos_img_info.append({'file_name': file_name, 'img_url': img_url});


def _download_preview_thumb():
	preview_thumb_panos_img_info = []
	for room in rooms:
		preview_file_name = 'vanke/panos/' + str(room) + '.tiles/preview.jpg'
		preview_img_url = preview_file_name.replace('vanke', 'http://vr.yyttww.com/wkc02')
		preview_thumb_panos_img_info.append({'file_name': preview_file_name, 'img_url': preview_img_url});
		thumb_file_name = 'vanke/panos/' + str(room) + '.tiles/thumb.jpg'
		thumb_img_url = thumb_file_name.replace('vanke', 'http://vr.yyttww.com/wkc02')
		preview_thumb_panos_img_info.append({'file_name': thumb_file_name, 'img_url': thumb_img_url});

	p = multiprocessing.Pool(40)
	for img in preview_thumb_panos_img_info:
		file_name = img['file_name']
		img_url = img['img_url']
		# _download_img(img_url,file_name)
		p.apply_async(_download_img, args=(img_url, file_name))
	p.close()
	p.join()

def _download_panos():
	p = multiprocessing.Pool(40)
	for img in panos_img_info:
		file_name = img['file_name'];
		img_url = img['img_url'];
		# _download_img(img_url,file_name)
		p.apply_async(_download_img, args=(img_url, file_name))
	p.close()
	p.join()

def _download_img(img_url, file_name):
	count = 0
	while True:
		try:
			print 'download: ', img_url
			urllib.urlretrieve(img_url, file_name)
		except socket.timeout:
			print 'timeout: ', img_url
			count += 1
		except Exception, e:
			print 'other fault: ', img_url, e
			count += 1
		else:
			print 'success: ', img_url, ' retry ', str(count) + ' times' 
			break

if __name__ == '__main__':
	_mkdir()
	_download_preview_thumb()
	_download_panos()

