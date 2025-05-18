#!venv/Scripts/python

import sys,os,subprocess
import json

__dirname = os.getcwd()

__outdir = "./out"

__ffprobe_path = os.path.join(__dirname,'bin','ffprobe.exe')

__ffprobe_command = ''

print(sys.platform)

if sys.platform == "win32":
    __ffprobe_command = __ffprobe_path
elif sys.platform == "linux":
    __ffprobe_command = 'ffprobe'

print(len(sys.argv))

def urlify(urlString: str):
    print(urlString)
    urlString = urlString.replace(" ","_")
    print(urlString)
    return urlString

if(len(sys.argv)==1):
    raise KeyError('Please pass a path to segregate')
else:
    __music_path = sys.argv[len(sys.argv)-1]

for subdir,dirs,files in os.walk(__music_path):
    for file in files:
        if len(subdir.split('\\')) == 1:
            fileMetadata = json.loads(subprocess.getoutput(f"{__ffprobe_command} -v quiet -print_format json -show_format -show_streams \"{os.path.join(subdir,file)}\""))['format']['tags']
    
            __album_dir = os.path.join(os.path.join(__outdir,urlify(fileMetadata['album_artist'])),urlify(fileMetadata['album']))
    
            if not(os.path.exists(__album_dir) and os.path.isdir(__album_dir)):
                os.makedirs(__album_dir)
            
            os.rename(os.path.join(subdir,file),os.path.join(__album_dir,file))
