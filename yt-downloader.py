print('.')
from pytube import Playlist, YouTube

print('.')
playlist = Playlist(
    'https://www.youtube.com/playlist?list=PLYJXjIs8Os4qCzL-ZudJWEOaRim6WXqYR')
print('Number of videos in playlist: %s' % len(playlist.video_urls))
for video_url in playlist.video_urls:
    print('****** DOWNLOADING SONG ******')
    yt = YouTube(video_url)
    yts = yt.streams.get_audio_only()
    fname = yts.download()
    print(f"Downloaded to {fname}")
