import urllib
import json
import os
import pandas as pd

if 'GOOGLE_API_KEY' not in os.environ:
    raise EnvironmentError('Need to set GOOGLE_API_KEY to run this script')

API_KEY = os.environ['GOOGLE_API_KEY']
API_ENDPOINT = 'https://www.googleapis.com/youtube/v3/search'


def get_all_videos_in_channel(channel_id):
    first_url = '{}?key={}&channelId={}&part=snippet,id&order=date&maxResults=25'.format(API_ENDPOINT, API_KEY,
                                                                                         channel_id)

    videos = []
    url = first_url
    while True:
        inp = urllib.request.urlopen(url)
        resp = json.load(inp)

        videos += [i for i in resp['items']]

        if 'nextPageToken' in resp:
            url = first_url + '&pageToken={}'.format(resp['nextPageToken'])
        else:
            break

    return videos


def video_to_row(video):
    if video['id']['kind'] == 'youtube#video':
        video_id = video['id']['videoId']
        image = video['snippet']['thumbnails']['high']
        title = video['snippet']['title']
        description = video['id']['videoId']
        publish_date = video['snippet']['publishedAt']

        return video_id, image, title, description, publish_date
    return None


def write_content_file(videos_df,
                       location="/Users/kholub/MediocreAmateur/generate/adventures.csv"):
    videos_df['youtube_url'] = ['https://www.youtube.com/watch?v=%s' % (v['id'],) for _,v in videos_df.iterrows()]
    videos_df['strava_link'] = None
    videos_df['amateurs'] = None
    videos_df['method'] = None

    videos_df.to_csv(location)

if __name__ == '__main__':
    all_videos = get_all_videos_in_channel('UC-04mJDJUYHEyE8JPIEa0-w')
    parsed_videos = [video_to_row(v) for v in all_videos]
    videos_df = pd.DataFrame([v for v in parsed_videos if v],
                             columns=['id', 'image', 'title', 'description', 'publish_date'])
