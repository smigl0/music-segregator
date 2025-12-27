#!venv/Scripts/python

import sys,os,subprocess
import json
import shutil
import shlex
import re

__dirname = os.getcwd()

__outdir = "./out"

__ffprobe_path = os.path.join(__dirname,'bin','ffprobe.exe')

__ffprobe_command = ''

if sys.platform == "win32":
    __ffprobe_command = __ffprobe_path
elif sys.platform == "linux":
    __ffprobe_command = 'ffprobe'

def urlify(urlString: str):
    return re.sub(r'[\\/:*?"<>|\'`$&;(){}[\]#!~]', '', urlString)

if(len(sys.argv)<2):
    raise KeyError('Please pass a path to segregate')
else:
    __music_path = sys.argv[1]
    if(len(sys.argv)==2):
        __outdir = sys.argv[1]
    else:
        __outdir = sys.argv[2]

if __name__ == '__main__':
    for file in os.listdir(__music_path):
        if os.path.isfile(os.path.join(__music_path,file)) and file.split('.')[-1] in ["mp3"]: 
            cmd = [
                    __ffprobe_command,
                    "-v", "quiet",
                    "-print_format", "json",
                    "-show_format",
                    "-show_streams",os.path.join(__music_path, file)]

            fileMetadata=json.loads(subprocess.run(cmd,capture_output=True, text=True).stdout)['format']['tags'] 
            try:
                __album_dir = os.path.join(os.path.join(__outdir,urlify(fileMetadata['album_artist'])),urlify(fileMetadata['album']))
            except KeyError:
                try:
                    __album_dir = os.path.join(os.path.join(__outdir,urlify(fileMetadata['artist'])),urlify(fileMetadata['album']))
                except:
                    pass
            print(__album_dir) 
            try:
                if not(os.path.exists(__album_dir) and os.path.isdir(__album_dir)):
                    os.makedirs(__album_dir)

                shutil.move(os.path.join(__music_path,file),os.path.join(__album_dir,file))
            except:
                pass
