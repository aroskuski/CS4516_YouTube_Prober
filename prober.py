#!/usr/bin/env python3.5

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

import json
import urllib
import string
import random

DEVELOPER_KEY = "AIzaSyDbZ8GyKj2-xoGZeBA9_EZcz-lxWEtOQYM"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

charSet = string.ascii_letters + string.digits + '_'

def prefix_generator(length, amount):
	
	usedprefixes = ['']
	for i in range(0, amount):
		prefix = gen_prefix(length)
		
		while prefix in usedprefixes:
			prefix = gen_prefix(length)

		usedprefixes.append(prefix)
		
		yield prefix

def gen_prefix(length):
	prefix = ''
	global charSet
	for i in range(0, length):
		prefix = prefix + random.choice(charSet)
	return prefix


def youtube_search(prefix):
	query = 'watch?v=' + prefix
	global youtube
	search_response = youtube.search().list(q=query, part="id,snippet", maxResults=50).execute()

	good_results = []

	#TODO: handle pagination

	for search_result in search_response.get("items", []):
		if search_result["id"]["kind"] == "youtube#video":
			if search_result["id"]["videoId"].startswith(prefix):
				good_results.append(search_result["id"]["videoId"])

	return good_results
	

def prefix_search(length, amount):
	results = []
	for i in prefix_generator(length, amount):
		results += youtube_search(i)
	print(results)
	detailedResults = [get_video_details(x) for x in results]	
	outfile = open('res.txt','w')
	outfile.write(json.dumps(detailedResults))
	outfile.close()

def get_video_details(video_id):
	global youtube
	video_details = youtube.videos().list(part="id,snippet,contentDetails,status,statistics",id=video_id).execute()
	return video_details

