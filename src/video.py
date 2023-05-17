import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class Video:

    def __init__(self, video_id):

        '''
        инициализация класса по id видео,
        названию, количество просмотров и лайков
        '''
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        try:
            self.video_id = youtube.videos().list(id=video_id, part='snippet,contentDetails,statistics').execute()
            self.url = f'https://youtu.be/{self.video_id}'
            self.title = self.video_id["items"][0]["snippet"]["title"]
            self.video = self.video_id["items"][0]["id"]
            self.video_views = self.video_id["items"][0]["statistics"]["viewCount"]
            self.like_count = self.video_id["items"][0]["statistics"]["likeCount"]
        except IndexError:
            self.url = None
            self.video = None
            self.title = None
            self.video_views = None
            self.like_count = None
        except HttpError:
            self.video_id = video_id
            self.url = None
            self.video = None
            self.title = None
            self.video_views = None
            self.like_count = None


    def __repr__(self):
        '''
        возвращает информацию об обьекте в текстовом формате
        '''
        return f"{self.__class__.__name__}({self.video}, {self.video_id}, {self.title}," \
               f"{self.title}, {self.video_views}, {self.title})"

    def __str__(self):
        '''
        возвращает название канала
        '''
        return f'{self.title}'

class PLVideo(Video):
    def __init__(self, video, playlist):
        '''
        инициализация подкласса по id видео, и id плейлиста
        '''
        super().__init__(video)
        api_key: str = os.getenv('YT_API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.playlist = playlist
        self.playlist_name = self.get_playlist_name()

    def __repr__(self):
        '''
        Переопределили метод репр в дочернем классе
        '''
        return f"{self.__class__.__name__}({self.video}, {self.youtube}, " \
               f"{self.playlist}, {self.playlist_name})"

    def get_playlist_name(self):
        '''
        возвращает название плейлиста
        '''
        self.playlist = self.youtube.playlists().list(id=self.playlist, part='snippet').execute()
        self.playlist_name = self.playlist['items'][0]['snippet']['title']
        return self.playlist_name
