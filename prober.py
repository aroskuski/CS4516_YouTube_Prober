#!/usr/bin/env python3.5

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

import json
import urllib
import string
import random

DEVELOPER_KEY = "REPLACE_ME"
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
	print(prefix)
	search_response = youtube.search().list(q=query, part="id,snippet", maxResults=50).execute()      
	good_results = []

	#TODO: handle pagination
	nextPageToken = search_response.get("nextPageToken")

	for search_result in search_response.get("items", []):
		if search_result["id"]["kind"] == "youtube#video":
			if search_result["id"]["videoId"].startswith(prefix):
				good_results.append(search_result["id"]["videoId"])

	# Look at all of the pages
	while (nextPageToken != None):
		print(nextPageToken)
		search_response = youtube.search().list(q=query, part="id,snippet", maxResults=50, pageToken=nextPageToken).execute()      

		nextPageToken = search_response.get("nextPageToken")

		for search_result in search_response.get("items", []):
			if search_result["id"]["kind"] == "youtube#video":
				if search_result["id"]["videoId"].startswith(prefix):
					good_results.append(search_result["id"]["videoId"])
	return good_results
	

def prefix_search(length, amount):
	results = []
	for i in prefix_generator(length, amount):
		results.append(youtube_search(i))
	return results

def get_video_details(video_id):
	global youtube
	video_details = youtube.videos.list(part="id,snippet",id=video_id).exectute()
	#TODO: Process details into desired format
	return video_details

