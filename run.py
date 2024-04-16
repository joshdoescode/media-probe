import subprocess
from os.path import abspath, normpath, dirname, join, isdir
from os import mkdir
from shutil import rmtree
from time import sleep


this_folder = normpath(abspath(dirname(__file__)))

output_folder = normpath(
    join(this_folder, 'output')
)

clips_folder = normpath(
    join(this_folder, 'clips')
)

ffprobe = normpath(
    join(this_folder, 'ffprobe.exe')
)
ffmpeg = normpath(
    join(this_folder, 'ffmpeg.exe')
)
ffplay = normpath(
    join(this_folder, 'ffplay.exe')
)

    
def to_file(output: str, cmd: str, file_name: str, failed: bool = False):    
    if not isdir(output_folder):
        mkdir(output_folder)
    
    file_name = file_name.split('/')[-1].split('\\')[-1].strip()
    
    file_name = file_name.replace('.exe', '').strip()
    file_name = '-'.join(file_name.split('"')).strip('-').strip()
    file_name = '-'.join(file_name.split("'")).strip('-').strip()
    file_name = '-'.join(file_name.split(" ")).strip('-').strip()
    file_name = '-'.join(file_name.split(".")).strip('-').strip()
    file_name = ''.join(file_name.split("--")).strip('-').strip()
    
    if failed:
        file_path = normpath(
            join(output_folder, "_failed.txt")
        )
    else:
        file_path = normpath(
            join(output_folder, f"{file_name}.txt")
        )
    
    try:
        with open(file_path, "a+") as f:
            if failed:
                f.write(
                    f'{cmd}\n\n' +
                    f'{output}\n' +
                    f'\n--- --- ---\n\n'
                )
                print(f'\nOutput saved to: "{file_path}"')
            else:
                f.writelines(f'{cmd}\n--- --- ---\n\n{output}\n\n')
                print(f'\nOutput saved to: "{file_path}"')
    except (Exception, FileExistsError) as ex:
        print(f'Failed to save file: {ex}')        


def _call(cmd: str, file_name: str):
    print(f'{cmd}:\n\n')
    output = subprocess.getoutput(cmd).strip()
    print(output)
    
    output_lower = output.lower()
    failed = (
        "error opening" in output_lower
        or "file does not contain any stream" in output_lower
        or "invalid argument" in output_lower
    )
    
    to_file(output, cmd, file_name, failed)
        
    print('\n---\n')
    
    
def call_probe(clip: str):    
    clip_path = normpath(
        join(clips_folder, clip)
    )
    _call(f'"{ffprobe}" -i "{clip_path}"', f'ffprobe-{clip}')
    
    
def call_play(clip: str):    
    clip_path = normpath(
        join(clips_folder, clip)
    )
    wait = 5
    print(f'ffplay.exe will take {wait} seconds to finish.\nPlaying "{clip}".')
    _call(f'"{ffplay}" -infbuf -loop 1 -autoexit -cpucount 1 -nodisp -volume 0 -t {wait} -i "{clip_path}"', f'ffplay-{clip}')
    
    
def call_mpeg(clip: str):    
    clip_path = normpath(
        join(clips_folder, clip)
    )
    _call(f'"{ffmpeg}" "{clip_path}"', f'ffmpeg-{clip}')


def run():
    if isdir(output_folder):
        print(f'Deleting old output folder ("{output_folder}").')
        rmtree(output_folder)

    # TODO - Scan a media folder for the clips list automatically
    files = [
        '2160p50 Flash and Beep.mov',
        'Audio Track Test - XDCAM 1080i50 16 tracks.mxf',
        'TSOutput.ts',
        'UMO - Ben Howard.mxf',
        'V00001.mp4',
        'PebbleActionTrailer_720p60.mxf',
        'Motor_720p5994DF.mxf',
        'Music Audio Shuffle Test - XDCAM 1080i50 8 Track.mxf'
    ]
    
    for file in files:
        call_probe(file)
        call_mpeg(file)
    
    for file in files:
        call_play(file)
    

run()

