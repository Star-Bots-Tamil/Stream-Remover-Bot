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
  start = time.time()
  probe = ffmpeg.probe(os.path.join(path, file))
  audio_tracks = [stream for stream in probe['streams'] if stream['codec_type'] == 'audio']
  subtitle_tracks = [stream for stream in probe['streams'] if stream['codec_type'] == 'subtitle']
  sub_stream = []
  sub_track = {}
  sub_list = []
  audio_stream = []
  audio_list = []
  audio_track = {}
  returned_list = []
  count = 0

  for index, audio_tracks in enumerate(audio_tracks):
    audio_stream.append(f"{audio_tracks.get('tags', {}).get('language', 'N/A')}{count}")
    count +=1
     
  count = 0
  for index, subtitle_tracks in enumerate(subtitle_tracks):
    sub_stream.append(f"{subtitle_tracks.get('tags', {}).get('language', 'N/A')}{count}")
    count +=1

  count=0
  for x in audio_stream:
    if x in audio_track:
      x = f'{x}{count}'
    audio_track[x] = f'0:a:{count}'
    count += 1
  
  count=0
  for x in sub_stream:
    if x in sub_stream:
      x = f'{x}'
    sub_track[x] = f'0:s:{count}'
    count+=1
  
  count=0
  for x in audio_stream:
    audio_list.append(x)
    count += 1

  count=0
  for x in sub_stream:
    sub_list.append(x)
    count += 1

  end = time.time()
  print(f'Execute time: {end-start}')

  selected_audio = inquirer.checkbox(
    message='Select all Audio tracks you want to keep',
    choices=audio_list,
    instruction="([\u2191\u2193]: Select Item. [Space]: Toggle Choice), [Enter]: Confirm",
    validate=lambda result: len(result) >= 1,
    invalid_message="should be at least 1 selection",
    ).execute()
  
  selected_subtitles = inquirer.checkbox(
    message='Select all Subtitle tracks you want to keep',
    choices=sub_list,
    instruction="([\u2191\u2193]: Select Item. [Space]: Toggle Choice), [Enter]: Confirm",
    validate=lambda result: len(result) >= 1,
    invalid_message="should be at least 1 selection",
    ).execute()

  for x in selected_audio:
    returned_list.append(audio_track[x])
      

  for x in selected_subtitles:
    returned_list.append(sub_track[x])
    
  return returned_list
  

def main():

  src_path = inquirer.filepath(
        message="Enter filepath to use:",
        validate=PathValidator(is_dir=True, message="Input is not a Directory"),
        only_directories=True,
    ).execute()
  
  src_list = os.listdir(src_path)
  # print(src_path)
  
  for x in enumerate(src_list):
    files = []
    tracks = data(src_path , x[1])
    tracks.append('0:v:0')
    
    filename = f'{str(x[1])}'
    filename = filename[:-4]
    output_file = lambda n, c: os.path.join(f'{src_path}', f'{n}{c}.mkv')
    output_file2 = lambda n: os.path.join(f'{src_path}', f'{n}.mkv')
    ep_path = os.path.join(src_path, x[1])

    input_file = ffmpeg.input(ep_path)
    count = 0
    for x in tracks:
      mapped = input_file.output(f'{output_file(str(x)[2:-2], count)}', map=x, c='copy')
      ffmpeg.run(mapped)
      files.append(f'{str(x)[2:-2]}{count}.mkv')
      count += 1
    
    audio_map=''.join([f'{output_file2({f"{os.path.join(src_path, x)}"})}, ' for x in files])
    concat = ffmpeg.concat(audio_map)
    cmd = ffmpeg.output(concat, f'{filename}.mkv')
    ffmpeg.run(cmd)

if __name__ == "__main__":
  # asyncio.run(main())
  # typer.run(main())
  main()