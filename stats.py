import argparse
import json
import string
import re
import math

class Statistics:

    def __init__(self, results_files):
        self.videos = Video_Group(None)
        self.results_files = results_files
        self.read_all_input()
        self.groups = self.make_video_groups(10)

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
        group_size = int(math.ceil(float(length / group_count)))

        for i in range(0, length, group_size):
            new_group = Video_Group(self.videos[i: i + group_size])
            groups.append(new_group)
            
        return groups


class Video_Group:

    def __init__(self, videos):
        if videos == None:
            self.videos = []
        else:
            self.videos = videos
        self.sorted_viewcount()

    def __len__(self):
        return len(self.videos)

    def __getitem__(self, index):
        return self.videos[index]

    def add_videos(self, videos):
        self.videos.extend(videos)
        self.sorted_viewcount()\


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
        categories = {
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
        histogram = {}
        for video in self.videos:
            try:
                category = categories[self.get_video_category_id(video)]
            except KeyError as e:
                category = "Other (Unknown)"
            if category not in histogram:
                histogram[category] = 1
            else:
                histogram[category] += 1
        histogram = sorted(histogram.items(), key=lambda x: x[1])
        return histogram

    def average_group_views(self):
        '''
        Get the average number of videos in this group
        '''
        count = 0
        for video in self.videos:
            count += self.get_video_views(video)
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", nargs="+",
                        help="Results files to generate statistics from")
    args = parser.parse_args()
    stats = Statistics(args.input)
