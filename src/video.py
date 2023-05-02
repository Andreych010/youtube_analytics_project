import os
from googleapiclient.discovery import build


class Video:

    def __init__(self, video):
        '''
        инициализация класса по id видео,
        названию, количество просмотров и лайков
        '''
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.video = youtube.videos().list(id=video, part='snippet,contentDetails,statistics').execute()
        self.video_id = self.video["items"][0]["id"]
        self.video_title = self.video["items"][0]["snippet"]["title"]
        self.video_views = self.video["items"][0]["statistics"]["viewCount"]
        self.video_likes = self.video["items"][0]["statistics"]["likeCount"]

    def __repr__(self):
        '''
        возвращает информацию об обьекте в текстовом формате
        '''
        return f"{self.__class__.__name__}({self.video}, {self.video_id}, {self.video_title}," \
               f"{self.video_title}, {self.video_views}, {self.video_likes})"

    def __str__(self):
        '''
        возвращает название канала
        '''
        return f'{self.video_title}'


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
