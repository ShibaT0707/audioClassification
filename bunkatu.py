from moviepy.editor import VideoFileClip
from yt_dlp import YoutubeDL
from spleeter.separator import Separator

download_resolution = 360

ROOT_PATH = 'AI/'
full_video_path = ROOT_PATH + 'videos/full_video.mp4'
input_clip_path = ROOT_PATH + 'videos/input_clip.mp4'
input_audio_path = ROOT_PATH + 'audios/input_clip.wav'

video_url = 'https://www.youtube.com/watch?v=eEi6zjSCN0U'



ydl_opts = {'format': f'best[height<={download_resolution}]', 'overwrites': True, 'outtmpl': full_video_path}
with YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])

video = VideoFileClip(full_video_path)
audio = video.audio

audio_file = 'audios/output.wav'
audio.write_audiofile(audio_file,codec='pcm_s16le')

# # Separatorオブジェクトの作成
separator = Separator('spleeter:2stems')

# # 分離の実行
separator.separate_to_file(audio_file, 'output/')
