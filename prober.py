#!/usr/bin/env python3.5

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

import json
import urllib
import string
import random

DEVELOPER_KEY = "REPLACE_ME"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

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
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

	search_response = youtube.search().list(q=query, part="id,snippet", maxResults=50).execute()

	good_results = []

	for search_result in search_response.get("items", []):
		if search_result["id"]["kind"] == "youtube#video":
			if search_result["id"]["videoId"].startswith(prefix):
				good_results.append(search_result)
	

def prefix_search():
	pass

