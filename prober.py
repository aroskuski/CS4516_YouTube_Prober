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



def prefix_generator(length, amount):
	charSet = string.ascii_letters + string.digits + '_'
	usedprefixes = []
	for i in range(0, amount):
		prefix = ''
		for j in range(0, length):
			prefix = prefix + charSet[random.randint(0,len(charSet) - 1)]
		yield prefix


def youtube_search(prefix):
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

	search_response = youtube.search().list(q=query, part="id,snippet", maxResults=50).execute()

	good_results = []

	for search_result in search_response.get("items", []):
		if search_result["id"]["kind"] == "youtube#video":
			if search_result["id"]["videoId"].startswith(prefix):
				pass
	

def prefix_search():
	pass

