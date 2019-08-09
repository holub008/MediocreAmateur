import urllib
import json
import os

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


if __name__ == '__main__':
    all_videos = get_all_videos_in_channel('UC-04mJDJUYHEyE8JPIEa0-w')
