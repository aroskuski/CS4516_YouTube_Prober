import argparse
import json


class Statistics:

    def __init__(self, results_files):
        self.videos = Video_Group(None)
        self.results_files = results_files
        self.read_all_input()
        self.groups = self.make_video_groups(10)

    def read_all_input(self):
        for file in self.results_files:
            with open(file, 'r') as f:
                contents = f.read()
                parsed = json.loads(contents)
                self.videos.add_videos(parsed)

        print("{0} videos loaded!".format(len(self.videos)))
        return

    def make_video_groups(self, group_count):
        groups = []
        length = len(self.videos)
        group_size = int(length / group_count)

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
        self.sorted_viewcount()

    def sorted_viewcount(self):
        if self.videos == None:
            return
        self.videos.sort(key=lambda x: self.get_video_views(x))

    def make_tag_histogram(self):
        histogram = {}
        for video in self.videos:
            tags = self.get_video_tags(video)
            for tag in tags:
                if tag not in histogram:
                    histogram[tag] = 1
                else:
                    histogram[tag] += 1
        histogram = sorted(histogram.items(), key=lambda x: x[1])
        return histogram

    def average_group_views(self):
        count = 0
        for video in self.videos:
            count += self.get_video_views(video)
        avg = count / self.__len__()
        return avg

    def get_video_tags(self, video):
        try:
            return video['items'][0]['snippet']['tags']
        except KeyError as e:
            return []

    def get_video_views(self, video):
        return int(video['items'][0]['statistics']['viewCount'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", nargs="+",
                        help="Results files to generate statistics from")
    args = parser.parse_args()
    stats = Statistics(args.input)
