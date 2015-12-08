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

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                developerKey=DEVELOPER_KEY)

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


def get_matches(prefix, search_response):
    good_results = []
    for search_response in search_response.get("items", []):
        if search_response["id"]["kind"] == "youtube#video":
            if search_response["id"]["videoId"].startswith(prefix):
                good_results.append(search_response["id"]["videoId"])
    return good_results


def youtube_search(prefix):
    query = 'watch?v=' + prefix
    global youtube
    good_results = []

    search_response = youtube.search().list(
        q=query, part="id,snippet", maxResults=50).execute()
    npToken = search_response.get("nextPageToken")
    good_results.extend(get_matches(prefix, search_response))

    while npToken != None:
        search_response = youtube.search().list(
            q=query, part="id,snippet", maxResults=50, pageToken=npToken).execute()
        npToken = search_response.get("nextPageToken")
        good_results.extend(get_matches(prefix, search_response))

    return good_results


def prefix_search(length, amount):
    results = []
    for i in prefix_generator(length, amount):
        results += youtube_search(i)
    print(results)
    detailedResults = [get_video_details(x) for x in results]
    write_json(detailedResults)


def write_json(results):
    outfile = open('res.txt', 'w')
    outfile.write(json.dumps(results))
    outfile.close()


def get_video_details(video_id):
    global youtube
    video_details = youtube.videos().list(
        part="id,snippet,contentDetails,status,statistics", id=video_id).execute()
    return video_details


def prefix_search_from_list(file):
    try:
        results = []
        f = open(file, "r").read()
        prefixes = f.replace('[','').replace(']','').replace("\"",'').split()
        for prefix in prefixes:
            results.extend(youtube_search(prefix))

        detailedResults = [get_video_details(x) for x in results]
        write_json(detailedResults)
    except IOError as e:
        print("error({0}): {1}".format(e.errno, e.strerror))

prefix_search_from_list("prefix.json")
