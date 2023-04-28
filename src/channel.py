import json
import os

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build


class Channel:
    """
Класс для ютуб-канала
    """
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id):
        """
Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API.
        """
        self.__channel_id = channel_id

        general_data = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        general_data = general_data['items'][0]

        # Задаём атрибуты
        self._title = general_data['snippet']['title']
        self._description = general_data['snippet']['description']
        self._url = 'https://www.youtube.com/channel/' + self.__channel_id
        self._subscriber_count = int(general_data['statistics']['subscriberCount'])
        self._video_count = general_data['statistics']['videoCount']
        self._viewCount = general_data['statistics']['viewCount']

    def __repr__(self):
        '''
Возвращает информацию об обьекте в текстовом формате
        '''
        return f'{self.__class__.__name__}({self.channel_id}, {self._title}, ' \
               f'{self._description}, {self._url}, {self._subscriber_count}, ' \
               f'{self._video_count}, {self._viewCount})'

    def __str__(self):
        '''
Возвращает название канала и ссылку на канал
        '''
        return f"{self._title} ({self._url})"

    def __add__(self, other):
        '''
Возвращает сумму кол-ва подписчиков двух каналов
        '''
        return self._subscriber_count + other._subscriber_count

    def __sub__(self, other):
        '''
Возвращает разность кол-ва подписчиков двух каналов
        '''
        return self._subscriber_count - other._subscriber_count

    def __gt__(self, other):
        '''
Сравнивает кол-во подписчико двух каналов
        '''
        if self._subscriber_count > other._subscriber_count:
            return True
        return False

    def __ge__(self, other):
        '''
Сравнивает кол-во подписчико двух каналов
        '''
        if self._subscriber_count >= other._subscriber_count:
            return True
        return False

    def __lt__(self, other):
        '''
Сравнивает кол-во подписчико двух каналов
        '''
        if self._subscriber_count < other._subscriber_count:
            return True
        return False

    def __le__(self, other):
        '''
Сравнивает кол-во подписчико двух каналов
        '''
        if self._subscriber_count <= other._subscriber_count:
            return True
        return False

    def print_info(self):
        """
Выводит в консоль информацию о канале.
        """
        channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @property
    def channel_id(self):
        '''
    возвращает id канала
        '''
        return self.__channel_id

    @property
    def title(self):
        '''
        возвращает название канала
        '''
        return self._title

    @property
    def description(self):
        '''
        возвращает описание канала
        '''
        return self._description

    @property
    def url(self):
        '''
        возвращает ссылку на канал
        '''
        return self._url

    @property
    def subscriber_count(self):
        '''
        возвращает количество подписчиков
        '''
        return self._subscriber_count

    @property
    def video_count(self):
        '''
        возвращает количество видео
        '''
        return self._video_count

    @property
    def viewCount(self):
        '''
        возвращает количество просмотров
        '''
        return self._viewCount

    @staticmethod
    def get_service():
        '''
        возвращающий объект для работы с YouTube API
        '''
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def to_json(self, _name):
        '''
        записываем полученные данные в файл
        '''
        data = {
            "channel_id": self.channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscriber_count": self.subscriber_count,
            "video_count": self.video_count,
            "viewCount": self.viewCount
        }

        file = open(_name, "w")
        json.dump(data, file, indent=4, ensure_ascii=False)
        file.close()
