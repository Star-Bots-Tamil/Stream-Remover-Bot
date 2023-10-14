from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.validator import PathValidator
import ffmpeg
import os
import subprocess
import typer
import time
app = typer.Typer()

def data(path, file):
  try:
    # print(f'File: {file}')
    start = time.time()
    probe = ffmpeg.probe(os.path.join(path, file))
    video_tracks = [stream for stream in probe['streams'] if stream['codec_type'] == 'video']
    audio_tracks = [stream for stream in probe['streams'] if stream['codec_type'] == 'audio']
    subtitle_tracks = [stream for stream in probe['streams'] if stream['codec_type'] == 'subtitle']
    video_stream = []
    video_track = {}
    sub_stream = []
    sub_track = {}
    audio_stream = []
    audio_track = {}
    count = 0

    for index, video_tracks in enumerate(video_tracks):
      video_stream.append(video_track.get('tags', {}).get('language', 'N/A'))

    for index, audio_tracks in enumerate(audio_tracks):
      audio_stream.append(audio_tracks.get('tags', {}).get('language', 'N/A'))

    for index, subtitle_tracks in enumerate(subtitle_tracks):
      sub_stream.append(subtitle_tracks.get('tags', {}).get('language', 'N/A'))


    for x in video_stream:
      if x not in video_track:
        video_track[x] = []
      video_track[x].append(f'0:s:{count}') 
      count+=1

    count=0
    for x in audio_stream:
      if x not in audio_track:
        audio_track[x] = []
      audio_track[x].append(f'0:a:{count}')  
      count += 1
    
    count=0
    for x in sub_stream:
      if x not in sub_track:
        sub_track[x] = []
      sub_track[x].append(f'0:s:{count}') 
      count+=1
    end = time.time()
    print(end-start)

    selected_video = inquirer.checkbox(
      message='Select all Video tracks you want to keep',
      choices=video_stream,
      instruction="([\u2191\u2193]: Select Item. [Space]: Toggle Choice), [Enter]: Confirm",
      validate=lambda result: len(result) >= 1,
      invalid_message="should be at least 1 selection",
      ).execute()
    
    selected_audio = inquirer.checkbox(
      message='Select all Audio tracks you want to keep',
      choices=audio_stream,
      instruction="([\u2191\u2193]: Select Item. [Space]: Toggle Choice), [Enter]: Confirm",
      validate=lambda result: len(result) >= 1,
      invalid_message="should be at least 1 selection",
      ).execute()
    
    selected_subtitles = inquirer.checkbox(
      message='Select all Subtitle tracks you want to keep',
      choices=sub_stream,
      instruction="([\u2191\u2193]: Select Item. [Space]: Toggle Choice), [Enter]: Confirm",
      validate=lambda result: len(result) >= 1,
      invalid_message="should be at least 1 selection",
      ).execute()


    for x in selected_video:
      print(f'video track: {video_track}')
      print(f'selected video: {x}')
      # del video_track[x]
    
    for x in selected_audio:
      print(f'audio track: {audio_track}')
      print(f'selected audio: {x}')
      # del audio_track[x]

    for x in selected_subtitles:
      print(f'subtitle track: {sub_track}')
      print(f'selected subtitles: {x}')
      # del sub_track[x]
      
    
    return video_track, audio_track, sub_track
  except ffmpeg.Error as e:
    # print(f'stdrr: {e.stderr}\n')
    # print(f'stdout:{e.stdout}')
    pass

# def subtitles(path, file):
  # probe = ffmpeg.probe(os.path.join(path, file))
  

# def main(input_list, input_file):
# @typer.command()
def main():

  src_path = inquirer.filepath(
        message="Enter filepath to use:",
        validate=PathValidator(is_dir=True, message="Input is not a Directory"),
        only_directories=True,
    ).execute()
  
  src_list = os.listdir(src_path)
  # print(src_path)
  count = 1
  
  for x in enumerate(src_list):
    videos, tracks, subtitles = data(src_path , x[1])

    # print(videos)
    # print(tracks)
    # print(subtitles)
    
    audio_map=''.join([f'-map {tracks[stream]} ' for stream in tracks])
    filename = f'{str(x[1])}'
    filename = filename[:-4]
    output_file = os.path.join(f'{src_path}', f'{filename}-eng.mkv')
    ep_path = os.path.join(src_path, x[1])

    # command = f'''ffmpeg -i "{ep_path}" -map 0 {audio_map}-map 0:s:0 -c copy "{output_file}"'''
    # subprocess.run(command)
    # print(command)

    count += 1

    # input_file = ffmpeg.input(ep_path)
    # mapped = input_file.output(f'{output_file}', map='v:0,a:1', c='copy')
    # ffmpeg.run(mapped)


if __name__ == "__main__":
  # asyncio.run(main())
  # typer.run(main())
  main()