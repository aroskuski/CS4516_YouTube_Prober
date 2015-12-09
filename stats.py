# -*- coding:UTF-8 -*-
import argparse
import json
import string
import re
import math
import sys
import datetime


class Statistics:

    def __init__(self, results_files):
        self.videos = Video_Group(None)
        self.results_files = results_files
        self.read_all_input()
        self.groups = self.make_video_groups(10)
        self.million_group = self.make_million_group(self.groups[9])

    def read_all_input(self):
        '''
        Reads all files provided as input and parses the videos
        '''
        for file in self.results_files:
            with open(file, 'r') as f:
                contents = f.read()
                parsed = json.loads(contents)
                self.videos.add_videos(parsed)

        print("{0} videos loaded!".format(len(self.videos)))
        return

    def make_video_groups(self, group_count):
        '''
        Splits the videos into 'group_count' groups of equal size`
        '''
        groups = []
        length = len(self.videos)

        group_size = int(length / group_count)
        remainder = int(math.ceil(float((length % group_size)) / group_count))
        group_size += remainder

        for i in range(0, length, group_size):
            new_group = Video_Group(self.videos[i: i + group_size])
            groups.append(new_group)
        return groups

    def make_cat_histogram_per_group(self):
        histograms = []
        for group in self.groups:
            histograms.append(group.make_category_histogram())
        return histograms

    def make_year_per_group(self):
        histograms = []
        for group in self.groups:
            histograms.append(group.make_year_histogram())
        return histograms

    def make_tag_histogram_per_group(self, numTags=0):
        histograms = []
        for group in self.groups:
            histograms.append(group.make_tag_histogram(numTags))
        return histograms

    def make_cat_view_histogram_per_group(self, numTags=0):
        histograms = []
        for group in self.groups:
            histograms.append(group.make_category_view_histogram())
        return histograms

    def make_million_group(self, video_group):
        million_group = Video_Group(None)

        for i in video_group.videos:
            if (video_group.get_video_views(i) >= 1000000):
                million_group.add_videos([i])
        return million_group


class Video_Group:

    def __init__(self, videos):
        if videos == None:
            self.videos = []
        else:
            self.videos = videos
        self.sorted_viewcount()

        self.categories = {
            1: "Film & Animation",
            2: "Autos & Vehicles",
            10: "Music",
            15: "Pets & Animals",
            17: "Sports",
            18: "Short Movies",
            19: "Travel & Events",
            20: "Gaming",
            21: "Videoblogging",
            22: "People & Blogs",
            23: "Comedy",
            24: "Entertainment",
            25: "News & Politics",
            26: "Howto & Style",
            27: "Education",
            28: "Science & Technology",
            29: "Nonprofits & Activism",
            30: "Movies",
            31: "Anime/Animation",
            32: "Action/Adventure",
            33: "Classics",
            34: "Comedy",
            35: "Documentary",
            36: "Drama",
            37: "Family",
            38: "Foreign",
            39: "Horror",
            40: "Sci-Fi/Fantasy",
            41: "Thriller",
            42: "Shorts",
            43: "Shows",
            44: "Trailers"
        }

    def __len__(self):
        return len(self.videos)

    def __getitem__(self, index):
        return self.videos[index]

    def add_videos(self, videos):
        self.videos.extend(videos)
        self.sorted_viewcount()

    def sorted_viewcount(self):
        '''
        Sorts the list of videos by ascending view count
        '''
        if self.videos == None:
            return
        self.videos.sort(key=lambda x: self.get_video_views(x))

    def make_tag_histogram(self, num=0):
        '''
        Returns a frequency histogram list of tags within the group
        '''
        histogram = {}
        for video in self.videos:
            tags = self.get_video_tags(video)
            for tag in tags:
                if tag not in histogram:
                    histogram[tag] = 1
                else:
                    histogram[tag] += 1
        histogram = sorted(histogram.items(), key=lambda x: x[1])

        if num == None or num == 0:
            return histogram
        else:
            return histogram[-1 * num:]

    def make_category_histogram(self):
        '''
        Returns a frequency histogram list of categories within the group
        '''
        histogram = {}
        for video in self.videos:
            try:
                category = self.categories[self.get_video_category_id(video)]
            except KeyError as e:
                category = "Other (Unknown)"
            if category not in histogram:
                histogram[category] = 1
            else:
                histogram[category] += 1
        histogram = sorted(histogram.items(), key=lambda x: x[1])
        return histogram

    def make_category_view_histogram(self):
        histogram = {}
        for video in self.videos:
            try:
                category = self.categories[self.get_video_category_id(video)]
                views = self.get_video_views(video)
            except KeyError as e:
                category = "Other (Unknown)"
            if category not in histogram:
                histogram[category] = views
            else:
                histogram[category] += views
        histogram = sorted(histogram.items(), key=lambda x: x[1])
        return histogram

    def make_month_histogram(self):
        histogram = {}
        months = {
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December"
        }
        for video in self.videos:
            try:
                month = months[self.get_video_upload_month(video)]
            except KeyError as e:
                month = "Other (Unknown)"
            if month not in histogram:
                histogram[month] = 1
            else:
                histogram[month] += 1
        histogram = sorted(histogram.items(), key=lambda x: x[1])
        return histogram

    def make_year_histogram(self):
        histogram = {}
        for video in self.videos:
            year = self.get_video_upload_year(video)
            if year not in histogram:
                histogram[year] = 1
            else:
                histogram[year] += 1
        histogram = sorted(histogram.items(), key=lambda x: x[1])
        return histogram

    def make_weekday_histogram(self):
        histogram = {}
        # For whatever reason, Monday is 0
        weekdays = {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday",
        }
        for video in self.videos:
            try:
                weekday = weekdays[self.get_video_upload_weekday(video)]
            except KeyError as e:
                weekday = "Other (Unknown)"
            if weekday not in histogram:
                histogram[weekday] = 1
            else:
                histogram[weekday] += 1
        histogram = sorted(histogram.items(), key=lambda x: x[1])
        return histogram

    def average_group_views(self):
        '''
        Get the average number of views in this group
        '''
        count = 0
        for video in self.videos:
            count += self.get_video_views(video)
        avg = count / self.__len__()
        return avg

    def median_group_views(self):
        '''
        Get the median number of views in this group
        '''
        medianIndex = len(self.videos) / 2
        median = int(medianIndex)
        if ((medianIndex % 2) == 1):
            median = int((int(math.floor(medianIndex)) +
                          int(math.ciel(medianIndex))) / 2)
        return self.get_video_views(self.videos[median])

    def average_like_ratio(self):
        count = 0.0
        for video in self.videos:
            count += self.get_video_like_pct(video)
        avg = count / self.__len__()
        return avg

    def average_view_favorite_ratio(self):
        count = 0.0
        for video in self.videos:
            count += self.get_video_favorite_view_ratio(video)
        avg = count / self.__len__()
        return avg

    def average_view_comment_ratio(self):
        count = 0.0
        for video in self.videos:
            count += self.get_video_comment_view_ratio(video)
        avg = count / self.__len__()
        return avg

    def average_group_video_length(self):
        '''
        Gets the average length of the video
        '''
        count = 0
        for video in self.videos:
            count += self.get_video_length(video)
        avg = count / self.__len__()
        return avg

    def max_group_video_length(self):
        maxLength = 0

        for video in self.videos:
            if (self.get_video_length(video) > maxLength):
                maxLength = self.get_video_length(video)

        return maxLength

    def min_group_video_length(self):
        minLength = int(sys.maxsize)

        for video in self.videos:
            if (self.get_video_length(video) < minLength):
                minLength = self.get_video_length(video)

        return minLength

    def average_num_tags(self):
        total = 0
        for video in self.videos:
            total += len(self.get_video_tags(video))
        average = total / self.__len__()
        return average

    def num_videos_w_tags(self):
        count = 0
        for video in self.videos:
            if (len(self.get_video_tags(video)) > 0):
                count += 1

        return count

    def average_group_video_quality(self):
        '''
        Gets the average length of the video
        '''
        count = 0
        for video in self.videos:
            if self.get_video_quality(video) == 'sd':
                count += 1
        stat = float(count) / self.__len__()
        return stat

    def average_licensed_pct(self):
        '''
        Gets the average length of the video
        '''
        count = 0
        for video in self.videos:
            if self.get_licensed_content(video) == True:
                count += 1
        stat = float(count) / self.__len__()
        return stat

    def iso8601_duration_to_seconds(self, duration):
        '''
        Converts an ISO 8601 formatted duration to seconds
        '''
        # http://stackoverflow.com/questions/16742381/how-to-convert-youtube-api-duration-to-seconds
        ISO_8601_period_rx = re.compile(
            'P'
            '(?:T'  # time part must begin with a T
            '(?:(?P<hours>\d+)H)?'   # hourss
            '(?:(?P<minutes>\d+)M)?'  # minutes
            '(?:(?P<seconds>\d+)S)?'  # seconds
            ')?'   # end of time part
        )
        int_hours, int_minutes, int_seconds = 0, 0, 0
        t_dict = ISO_8601_period_rx.match(duration).groupdict()
        if 'hours' in t_dict:
            if t_dict['hours'] != None:
                int_hours = int(t_dict['hours']) * 3600
        if 'minutes' in t_dict:
            if t_dict['minutes'] != None:
                int_minutes = int(t_dict['minutes']) * 60
        if 'seconds' in t_dict:
            if t_dict['seconds'] != None:
                int_seconds = int(t_dict['seconds'])

        result = int_hours + int_minutes + int_seconds
        return result

    def readable_seconds(self, seconds):
        sToHours = int(math.floor(seconds / 3600))
        leftover = seconds % 3600
        sToMinutes = int(math.floor(leftover / 60))
        sec = leftover % 60
        time = {'hours': sToHours, 'minutes': sToMinutes, 'seconds': sec}
        return time

    def get_video_category_id(self, video):
        '''
        Gets the video category (the id, not the actual name of the category)
        '''
        categoryId = int(video['items'][0]['snippet']['categoryId'])
        return categoryId

    def get_video_tags(self, video):
        '''
        Get the tags associated with a video
        '''
        try:
            return video['items'][0]['snippet']['tags']
        except KeyError as e:
            return []

    def get_video_length(self, video):
        '''
        Gets the length of the video in seconds
        '''
        duration = video['items'][0]['contentDetails']['duration']
        return self.iso8601_duration_to_seconds(duration)

    def get_video_views(self, video):
        '''
        Get the number of views that a video has
        '''
        return int(video['items'][0]['statistics']['viewCount'])

    def get_video_upload_date(self, video):
        full_upl_date = video['items'][0]['snippet']['publishedAt']
        date = full_upl_date.split("T")[0]

        # 2015-09-22T04:57:45.000Z
        parsed = datetime.datetime.strptime(date, "%Y-%m-%d")
        return parsed

    def get_video_upload_year(self, video):
        date = self.get_video_upload_date(video)
        return date.year

    def get_video_upload_month(self, video):
        date = self.get_video_upload_date(video)
        return date.month

    def get_video_upload_weekday(self, video):
        date = self.get_video_upload_date(video)
        return date.weekday()

    def get_video_quality(self, video):
        '''
        Gets the best available quality of video
        '''
        return video['items'][0]['contentDetails']['definition']

    def get_licensed_content(self, video):
        '''
        Gets whether or not the video contains licensed content
        '''
        return video['items'][0]['contentDetails']['licensedContent']

    def get_video_like_pct(self, video):
        likes, dislikes = 0, 0
        if 'likeCount' in video['items'][0]['statistics']:
            likes = int(video['items'][0]['statistics']['likeCount'])

        if 'dislikeCount' in video['items'][0]['statistics']:
            dislikes = int(video['items'][0]['statistics']['dislikeCount'])

        total = likes + dislikes
        if total == 0:
            # video has same number of likes and dislikes, even though it's 0
            # of each
            return 0.50

        if dislikes == 0:
            return 1.0

        return float(likes) / total

    def get_video_favorite_view_ratio(self, video):
        views, favorites = 0, 0
        views = self.get_video_views(video)

        if 'favoriteCount' in video['items'][0]['statistics']:
            favorites = int(video['items'][0]['statistics']['favoriteCount'])

        total = views + favorites
        if total == 0:
            # video has same number of likes and favorites
            return 0.50

        if favorites == 0:
            return 1.0

        return float(views) / total

    def get_video_comment_view_ratio(self, video):
        views, comments = 0, 0
        views = self.get_video_views(video)

        if 'commentCount' in video['items'][0]['statistics']:
            comments = int(video['items'][0]['statistics']['commentCount'])

        total = views + comments
        if total == 0:
            # video has same number of likes and favorites
            return 0.50

        if comments == 0:
            return 1.0

        return float(views) / total

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", nargs="+",
                        help="Results files to generate statistics from")
    args = parser.parse_args()
    stats = Statistics(args.input)

    print("Total Views per Category Histogram")
    print(stats.videos.make_category_view_histogram())

    histograms = stats.make_cat_histogram_per_group()
    j = 0
    for hist in histograms:
        print("Group #{0} Category Histogram".format(j))
        for i in hist:
            print(i)
        print()
        j += 1
    tHists = stats.make_tag_histogram_per_group(10)
    j = 0
    for tHist in tHists:
        print("Group #{0} Tag Histogram".format(j))
        for i in tHist:
            print(i)
        print()
        j += 1
    millions = stats.million_group
    j = 0
    for group in stats.groups:
        print("Group {0} View/Favorite Ratio".format(j))
        print(group.average_view_favorite_ratio())
        j += 1
    j = 0
    for group in stats.groups:
        readTime = group.readable_seconds(group.max_group_video_length())
        print("Max video length = %d hours, %d minutes, %d seconds" %
              (readTime['hours'], readTime['minutes'], readTime['seconds']))

    j = 0
    for group in stats.groups:
        readTime = group.readable_seconds(group.min_group_video_length())
        print("Min video length = %d hours, %d minutes, %d seconds" %
              (readTime['hours'], readTime['minutes'], readTime['seconds']))

    j = 0
    for group in stats.groups:
        averageTags = group.average_num_tags()
        print("Average tags = %d" % averageTags)

    j = 0
    for group in stats.groups:
        numVidsWithTags = group.num_videos_w_tags()
        print("Videos with tags = %d" % numVidsWithTags)
    tHists = stats.make_year_per_group()
    j = 0
    for tHist in tHists:
        print("Group #{0} Year upload Histogram".format(j))
        for i in tHist:
            print(i)
        print()
        j += 1
