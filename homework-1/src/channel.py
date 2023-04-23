import json
import os

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build


class Channel:
    """
Класс для ютуб-канала
    """

    def __init__(self, channel_id):
        """
Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API.
        """
        self.channel_id = channel_id

    def print_info(self):
        """
Выводит в консоль информацию о канале.
        """

        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()

        print(json.dumps(channel, indent=2, ensure_ascii=False))