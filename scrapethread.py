#!/usr/bin/env python2

import requests
import argparse
import os.path

def main():
	#TODO: argument for thread url (regex cap)
	#TODO: argument for saving as original filename (can't wget -i, possible duplicate names)
	#TODO: test youtube embeds, flash vids, pdfs, webms, ...
	#TODO: thread watching

	board, thread_num = get_args()
	thread_api_url = "http://8ch.net/{0}/res/{1}.json".format(board, thread_num)
	thread = requests.get(thread_api_url).json()
	
	images = []
	for post in thread["posts"]:
		#no image when filename does not exist
		if "filename" not in post:
			continue
		image_url = post["tim"] + post["ext"]
		image_original = post["filename"] + post["ext"]
		images.append({
			"url": image_url,
			"filename": image_original
		})
		#check for extra images
		if "extra_files" not in post:
			continue
		for extra in post["extra_files"]:
			image_url = extra["tim"] + extra["ext"]
			image_original = extra["filename"] + extra["ext"]
			images.append({
				"url": image_url,
				"filename": image_original
			})
	
	#print out all images found
	for img in images:
		final_url = "http://8ch.net/{0}/src/{1}".format(board, img["url"])
		download_image(final_url)

def download_image(url):
	local_fname = url.split('/')[-1]

	if (os.path.isfile(local_fname)):
		print("file " + url + " exists, skipping")
		return local_fname

	print("Getting file " + url)
	r = requests.get(url, stream=True)
	with open(local_fname, "wb") as f:
		for chunk in r.iter_content(chunk_size=1024):
			if chunk:
				f.write(chunk)
	return local_fname

def get_args():
	parser = argparse.ArgumentParser(description='Download some 8ch images.')
	parser.add_argument("board", help="the board (e.g. b)", )
	parser.add_argument("thread_num", help="the post number of the thread (e.g. 2314462)")
	args = parser.parse_args()
	return (args.board, args.thread_num)


if __name__ == "__main__":
	main()
