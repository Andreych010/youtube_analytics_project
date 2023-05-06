import os
import isodate
from datetime import timedelta
from googleapiclient.discovery import build


class PlayList:
    def __init__(self, playlist_id):
        '''
        Инициализируем класс по id видео, названию, ссылке по плей листу, кол-ву просмотров и лайков
        '''
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)

        self.playlist_id = playlist_id
        self.playlist = youtube.playlists().list(id=playlist_id, part='snippet').execute()
        self.playlist_video = youtube.playlistItems().list(playlistId=playlist_id,
                                                           part='contentDetails,snippet', maxResults=50, ).execute()
        self.video_ids = [video['contentDetails']['videoId'] for video in self.playlist_video['items']]
        self.videos = youtube.videos().list(part='contentDetails,statistics', id=','.join(self.video_ids)).execute()
        self.title = self.playlist['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    @property
    def total_duration(self):
        '''
        Возвращает длителбность плей листа
        '''
        delta_duration = timedelta()
        for i in range(len(self.videos) + 1):
            duration = self.videos['items'][i]['contentDetails']['duration']
            iso_duration = isodate.parse_duration(duration)
            delta_duration += iso_duration
        return delta_duration

    def total_seconds(self):
        return self.total_duration.seconds

    def show_best_video(self):
        '''
        Возвращает ссылку на самое популярное видео из плейлиста
        '''
        videos = {}
        id_ = None
        likes = 0
        for i in range(len(self.playlist_video) + 1):
            videos[self.videos['items'][i]['statistics']['likeCount']] = self.playlist_video['items'][i]
            if likes < int(self.videos['items'][i]['statistics']['likeCount']):
                likes = int(self.videos['items'][i]['statistics']['likeCount'])
                id_ = self.videos['items'][i]['id']
        return f"https://youtu.be/{id_}"
