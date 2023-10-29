from InquirerPy import inquirer
from InquirerPy.validator import PathValidator
import ffmpeg
import time
import av
import os

def data(path:str, file:str):
  """Uses ffprobe to get data of video/audio file

  Args:
      path (str): path to file(not including filename)
      file (str): filename you want to use

  Returns:
      list: A list of all selected tracks
  """
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
  print(f'Execute time: {end-start:.2f}')

  # selected_audio = inquirer.checkbox(
    # message='Select all Audio tracks you want to keep',
    # choices=audio_list,
    # instruction="([\u2191\u2193]: Select Item. [Space]: Toggle Choice), [Enter]: Confirm",
    # validate=lambda result: len(result) >= 1,
    # invalid_message="should be at least 1 selection",
    # ).execute()
  # 
  # selected_subtitles = inquirer.checkbox(
    # message='Select all Subtitle tracks you want to keep',
    # choices=sub_list,
    # instruction="([\u2191\u2193]: Select Item. [Space]: Toggle Choice), [Enter]: Confirm",
    # validate=lambda result: len(result) >= 1,
    # invalid_message="should be at least 1 selection",
    # ).execute()
  for x in audio_list:
    print(f'')
  
  for x in sub_list:
    print(x)    
  
  # for x in selected_audio:
    # returned_list.append(audio_track[x])
# 
  # for x in selected_subtitles:
    # returned_list.append(sub_track[x])
    
  return returned_list

def seperate(tracks, input_file, output_file):
  """Seperate selected audio/subtitles into different tracks

  Args:
      tracks (list): List of all selected tracks
      input_file (str): File to take out of
      output_file (str): output path
  """
  start = time.time()  
  files = []
  count = 0
  for x in tracks:
    mapped = input_file.output(f'{output_file(str(x)[2:-2], count)}', map=x, c='copy')
    ffmpeg.run(mapped)
    files.append(f'{str(x)[2:-2]}{count}.mkv')
    count += 1
  
  end = time.time()
  print(f'Seperate time: {end-start:.2f}')
  return files

def concat(path:str, files:list, output:str):
  """Combine multiple files into one file

  Args:
      path (str): Path to directory
      files (list): A list of file paths to combine
      Output (str): Name of output file (uses_path)
  """
  # print(path)
  # print(files)
  # print(output)
  start = time.time()
  ipc = 0
  output_streams = {}  # Dictionary to store output streams
  output = os.path.join(path, output)
  output_container = av.open(f'{output}-eng.mkv', 'w')

  for x in files:
    xp = os.path.join(path, x)
    input_container = av.open(xp)
    stream_type = x[:-5]  # Get the stream type from the filename
    if x[:-5] == 'v':
      # print(input_container.streams.video) 
      in_stream = input_container.streams.video[0]
    elif x[:-5] == 'a': 
      # print(input_container.streams.audio) 
      in_stream = input_container.streams.audio[0]
    elif x[:-5] == 's': 
      # print(input_container.streams.subtitles) 
      in_stream = input_container.streams.subtitles[0]
    
    out_stream = output_container.add_stream(template=in_stream)

    if stream_type not in output_streams:
        out_stream = output_container.add_stream(template=in_stream)
        output_streams[stream_type] = out_stream
    else:
        out_stream = output_streams[stream_type]
    print(f'out streams: {output_streams}')
    for packet in input_container.demux():
      # try:
        if packet.dts is None:
          continue
        packet.stream = out_stream
        # output_container.add_stream(packet)
        output_container.mux(packet)
      # except ValueError as e:
        # continue
    input_container.close()
    ipc += 1
  output_container.close
  print(f"Merge complete. {ipc} files merged into {output}-eng.mkv")
  end = time.time()
  print(f'Concat Time: {end-start:.2f}')

def remove_files(dirname, filename):
  os.remove(os.path.join(dirname, filename))

def main():
  while True:
    src_path = inquirer.filepath(
          message="Enter filepath to use:",
          validate=PathValidator(is_dir=True, message="Input is not a Directory"),
          only_directories=True,
      ).execute()
    src_list = os.listdir(src_path)

    for x in enumerate(src_list):
      tracks = data(src_path , x[1])
      tracks.insert(0, '0:v:0')
      filename = f'{str(x[1])}'
      filename = filename[:-4]
      output_file = lambda n, c: os.path.join(f'{src_path}', f'{n}{c}.mkv')
      output_file2 = lambda n: os.path.join(f'{src_path}', f'{n}.mkv')
      ep_path = os.path.join(src_path, x[1])
      input_file = ffmpeg.input(ep_path)
      # files = seperate(tracks, input_file, output_file)
      files = ['v0.mkv', 'a1.mkv', 's2.mkv', 's3.mkv']
      # concat(src_path, files, filename)
      # for fname in files:
        # remove_files(src_path, fname)


      # audio_map=''.join([f'{output_file2({f"{os.path.join(src_path, x)}"})}, ' for x in files])
      # concat = ffmpeg.concat(audio_map)
      # cmd = ffmpeg.output(concat, f'{filename}.mkv')
      # ffmpeg.run(cmd, quiet=True)


if __name__ == "__main__":
  main()