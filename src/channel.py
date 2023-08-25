from googleapiclient.discovery import build
import json


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.title = None
        self.description = None
        self.url = None
        self.subscriber_count = None
        self.video_count = None
        self.view_count = None
        self.get_channel_info()

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        youtube = build('youtube', 'v3', developerKey='AIzaSyD9AOcIorP6BZnUE6nV6alHpJldiO2iqFU')
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, ensure_ascii=False, indent=4))

    def get_channel_info(self) -> None:
        """Получает информацию о канале по API и заполняет атрибуты."""
        youtube = self.get_service()
        channel_info = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()

        snippet = channel_info['items'][0]['snippet']
        statistics = channel_info['items'][0]['statistics']

        self.title = snippet['title']
        self.description = snippet['description']
        self.url = f"https://www.youtube.com/channel/{self.channel_id}"
        self.subscriber_count = int(statistics['subscriberCount'])
        self.video_count = int(statistics['videoCount'])
        self.view_count = int(statistics['viewCount'])

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API."""
        return build('youtube', 'v3', developerKey='AIzaSyD9AOcIorP6BZnUE6nV6alHpJldiO2iqFU')

    def to_json(self, file_name: str) -> None:
        """Сохраняет значения атрибутов экземпляра в JSON-файл."""
        channel_data = {
            'channel_id': self.channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
        }
        with open(file_name, 'w', encoding='utf-8') as json_file:
            json.dump(channel_data, json_file, ensure_ascii=False, indent=4)
