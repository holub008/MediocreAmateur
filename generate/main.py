import urllib
import json
import os
import pandas as pd
import requests

if 'GOOGLE_API_KEY' not in os.environ:
    raise EnvironmentError('Need to set GOOGLE_API_KEY to run this script')

API_KEY = os.environ['GOOGLE_API_KEY']
API_ENDPOINT = 'https://www.googleapis.com/youtube/v3/search'
REPOSITORY_DIRECTORY = "/Users/kholub/MediocreAmateur"


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
        image = video['snippet']['thumbnails']['high']['url']
        title = video['snippet']['title']
        description = video['snippet']['description']
        publish_date = video['snippet']['publishedAt']

        return video_id, image, title, description, publish_date
    return None


def write_generate_content_file(videos_df,
                       append=True,
                       location=REPOSITORY_DIRECTORY + "/generate/adventures.csv"):
    """
    :param videos_df: a dataframe with columns "id", "image", "title", "description", "publish_date"
    :param append: if true, only new (according to "id") videos are added to the content file
    :param location: filepath to the content file
    :return: None
    """
    videos_df['strava_link'] = None
    videos_df['amateurs'] = None
    videos_df['mode'] = None
    videos_df['distance'] = None
    videos_df['latitude'] = None
    videos_df['longitude'] = None

    if os.path.exists(location) and append:
        existing_videos = pd.read_csv(location, index_col=0)
        joined_videos = videos_df.merge(existing_videos[['id']], how="outer", on='id', indicator=True)
        new_videos = joined_videos[joined_videos['_merge'] == 'left_only'].drop('_merge', axis='columns')

        videos_for_write = pd.concat([new_videos, existing_videos])
        if videos_for_write.shape[0] > 0:
            videos_for_write.to_csv(location)
    elif videos_df.shape[0] > 0:
        videos_df.to_csv(location)


def read_content_file(location=REPOSITORY_DIRECTORY + "/generate/adventures.csv"):
    return pd.read_csv(location)


def fetch_images(videos_df,
                 append=True,
                 location=REPOSITORY_DIRECTORY + "/www/images"):
    for _, video in videos_df.iterrows():
        image_path="%s/%s.%s" % (location, video['id'], "jpg")
        if not os.path.exists(image_path) or not append:
            resp = requests.get(video['image'])
            if resp.status_code == 200:
                with open(image_path, 'wb') as handle:
                    handle.write(resp.content)


def write_www_content_file(video_content,
                           location=REPOSITORY_DIRECTORY + '/www/adventures.json'):
    """
    convert a dataframe to json to be served
    :param video_content a dataframe with the usual columns
    """
    rows = []
    json_columns = ['id', 'title', 'description', 'publish_date', 'strava_link', 'amateurs', 'mode',
                    'distance', 'latitude', 'longitude']
    for _, video in video_content.iterrows():
        row = {}
        for col in json_columns:
            if not pd.isnull(video[col]):
                if col == 'amateurs':
                    row[col] = video[col].split(',')
                else:
                    row[col] = video[col]

        rows.append(row)

    with open(location, 'w') as f:
        json.dump(rows, f)


if __name__ == '__main__':
    all_videos = get_all_videos_in_channel('UC-04mJDJUYHEyE8JPIEa0-w')
    parsed_videos = [video_to_row(v) for v in all_videos]
    videos_df = pd.DataFrame([v for v in parsed_videos if v],
                             columns=['id', 'image', 'title', 'description', 'publish_date'])
    write_generate_content_file(videos_df)
    # after some hand entry:
    video_content = read_content_file()
    fetch_images(video_content)
    write_www_content_file(video_content)


