#!venv/Scripts/python

import sys,os,subprocess

__dirname = os.getcwd()

__ffprobe_path = os.path.join(__dirname,'bin','ffprobe.exe')
__ffmpeg_path  = os.path.join(__dirname,'bin','ffmpeg.exe')


print(len(sys.argv))

if(len(sys.argv)==1):
    raise KeyError('Please pass a path to segregate')
else:
    __music_path = sys.argv[len(sys.argv)-1]

for subdir,dirs,files in os.walk(__music_path):
    # print(subdir)
    for file in files:
        print(os.path.join(subdir,file))
        print(subprocess.getoutput(f"{__ffprobe_path} \"{os.path.join(subdir,file)}\"") )