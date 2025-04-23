class Song:
    def __init__(self, video_id: str, title: str, thumbnail: str, duration: int = 0):
        self.video_id = video_id
        self.title = title
        self.thumbnail = thumbnail
        self.duration = duration
        self.play_count = 0

    def increment_play_count(self):
        self.play_count += 1

    def to_dict(self):
        return {
            "videoId": self.video_id,
            "title": self.title,
            "thumbnail": self.thumbnail,
            "duration": self.duration,
            "playCount": self.play_count
        }
