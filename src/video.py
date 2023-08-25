from googleapiclient.discovery import build


class Video:

    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.video_id = video_id
        self.title = None
        self.url = None
        self.view_count = None
        self.like_count = None
        self.get_video_info()

    def __str__(self):
        return self.title

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API."""
        return build('youtube', 'v3', developerKey='AIzaSyD9AOcIorP6BZnUE6nV6alHpJldiO2iqFU')

    def get_video_info(self) -> None:
        """Получает информацию о видео по API и заполняет атрибуты."""
        youtube = self.get_service()
        video_info = youtube.videos().list(id=self.video_id, part='snippet,statistics').execute()

        snippet = video_info['items'][0]['snippet']
        statistics = video_info['items'][0]['statistics']
        self.title = snippet['title']
        self.url = f"https://www.youtube.com/channel/{self.video_id}"
        self.like_count = int(statistics['likeCount'])
        self.view_count = int(statistics['viewCount'])


class PLVideo(Video):

    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __add__(self, other):
        playlist_id = self.get_playlist_info(other)
        if isinstance(self.video_id, playlist_id):
            return self.get_playlist_name(playlist_id)

    def get_playlist_info(self, playlist_id):
        youtube = self.get_service()
        playlist_info = youtube.playlistItems().list(playlistId=playlist_id, part='contentDetails', maxResults=50).execute()
        return playlist_info

    def get_playlist_name(self, playlist_id):
        playlist_info = self.get_playlist_info(playlist_id)
        snippet = playlist_info['items'][0]['snippet']
        self.title = snippet['title']
        return self.title


