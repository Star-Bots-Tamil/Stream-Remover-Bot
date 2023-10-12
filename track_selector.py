from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.validator import PathValidator
import ffmpeg
import os
import subprocess
import typer

app = typer.Typer()

def data(path, file):
  try:
    # print(f'File: {file}')
    probe = ffmpeg.probe(os.path.join(path, file))
    audio_tracks = [stream for stream in probe['streams'] if stream['codec_type'] == 'audio']
    subtitle_tracks = [stream for stream in probe['streams'] if stream['codec_type'] == 'subtitle']
    subs_streams = []
    subtitles = {}
    streams = []
    tracks = {}
    count = 0

    for index, audio_track in enumerate(audio_tracks):
      streams.append(audio_track.get('tags', {}).get('language', 'N/A'))

    for index, subtitle_track in enumerate(subtitle_tracks):
      subs_streams.append(subtitle_track.get('tags', {}).get('language', 'N/A'))
    
    for x in subs_streams:
      subtitles[count][x] = f'0:s:{count}'
      count+=1
    print(subtitles)
    count=0
    for x in streams:
      tracks[x] = f'0:a:{count}'
      count += 1
    selected_streams = inquirer.checkbox(
      message='Select all Audio tracks you want to keep',
      choices=tracks,
      instruction="([\u2191\u2193]: Select Item. [Space]: Toggle Choice), [Enter]: Confirm",
      validate=lambda result: len(result) >= 1,
      invalid_message="should be at least 1 selection",
      ).execute()
    
    selected_subtitles = inquirer.checkbox(
      message='Select all Subtitle tracks you want to keep',
      choices=subs_streams,
      instruction="([\u2191\u2193]: Select Item. [Space]: Toggle Choice), [Enter]: Confirm",
      validate=lambda result: len(result) >= 1,
      invalid_message="should be at least 1 selection",
      ).execute()

    for x in selected_subtitles:
      del subtitles[x]
    
    for x in selected_streams:
      del tracks[x]

    return tracks, subtitles
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
    tracks, subtitles = data(src_path , x[1])

    # print(tracks)
    # print(subtitles)
    # audio_map=''.join([f'-map {tracks[stream]} ' for stream in tracks])
    # filename = f'{str(x[1])}'
    # filename = filename[:-4]
    # output_file = os.path.join(f'{src_path}', f'{filename}-eng.mkv')
    # ep_path = os.path.join(src_path, x[1])
# 
    # command = f'''ffmpeg -i "{ep_path}" -map 0 {audio_map}-map 0:s:0 -c copy "{output_file}"'''
    # subprocess.run(command)
    # print(command)
# 
    # count += 1

    # input_file = ffmpeg.input(ep_path)
    # mapped = input_file.output(f'{output_file}', map='v:0,a:1', c='copy')
    # ffmpeg.run(mapped)


if __name__ == "__main__":
  # asyncio.run(main())
  # typer.run(main())
  main()