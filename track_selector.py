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
  # print(f'File: {file}')
  start = time.time()
  probe = ffmpeg.probe(os.path.join(path, file))
  audio_tracks = [stream for stream in probe['streams'] if stream['codec_type'] == 'audio']
  subtitle_tracks = [stream for stream in probe['streams'] if stream['codec_type'] == 'subtitle']
  sub_stream = []
  sub_track = {}
  audio_stream = []
  audio_track = {}
  count = 0

  for index, audio_tracks in enumerate(audio_tracks):
    audio_stream.append(audio_tracks.get('tags', {}).get('language', 'N/A'))

  for index, subtitle_tracks in enumerate(subtitle_tracks):
    sub_stream.append(subtitle_tracks.get('tags', {}).get('language', 'N/A'))

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
  print(f'Execute time: {end-start}')

  selected_audio = inquirer.checkbox(
    message='Select all Audio tracks you want to keep',
    choices=audio_track,
    instruction="([\u2191\u2193]: Select Item. [Space]: Toggle Choice), [Enter]: Confirm",
    validate=lambda result: len(result) >= 1,
    invalid_message="should be at least 1 selection",
    ).execute()
  print(selected_audio)
  selected_subtitles = inquirer.checkbox(
    message='Select all Subtitle tracks you want to keep',
    choices=sub_stream,
    instruction="([\u2191\u2193]: Select Item. [Space]: Toggle Choice), [Enter]: Confirm",
    validate=lambda result: len(result) >= 1,
    invalid_message="should be at least 1 selection",
    ).execute()

  for x in selected_audio:
    print(f'audio track: {audio_track}')
    print(f'selected audio: {x}')
    # for y in audio_track[]
    # del audio_track[x]

  for x in selected_subtitles:
    print(f'subtitle track: {sub_track}')
    print(f'selected subtitles: {x}')
    # del sub_track[x]
    
      
  return audio_track, sub_track
  

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
    tracks, subtitles = data(src_path , x[1])

    # print(videos)
    # print(tracks)
    # print(subtitles)
    
    filename = f'{str(x[1])}'
    filename = filename[:-4]
    output_file = lambda n: os.path.join(f'{src_path}', f'{n}.mkv')
    ep_path = os.path.join(src_path, x[1])

    input_file = ffmpeg.input(ep_path)
    mapped = input_file.output(f'{output_file("a")}', map='0:a:0', c='copy')
    ffmpeg.run(mapped)

    count += 1

if __name__ == "__main__":
  # asyncio.run(main())
  # typer.run(main())
  main()