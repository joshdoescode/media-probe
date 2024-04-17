import subprocess
from os.path import abspath, normpath, dirname, join, isdir, isfile
from os import mkdir, listdir
from shutil import rmtree


_this_folder = normpath(abspath(dirname(__file__)))

_output_folder = normpath(
    join(_this_folder, 'output')
)

_clips_folder = normpath(
    join(_this_folder, 'clips')
)

_ffprobe = normpath(
    join(_this_folder, 'ffprobe.exe')
)
_ffmpeg = normpath(
    join(_this_folder, 'ffmpeg.exe')
)
_ffplay = normpath(
    join(_this_folder, 'ffplay.exe')
)

    
def to_file(output: str, cmd: str, file_name: str, failed: bool = False):    
    if not isdir(_output_folder):
        mkdir(_output_folder)
    
    file_name = file_name.split('/')[-1].split('\\')[-1].strip()
    
    file_name = file_name.replace('.exe', '').strip()
    file_name = '-'.join(file_name.split('"')).strip('-').strip()
    file_name = '-'.join(file_name.split("'")).strip('-').strip()
    file_name = '-'.join(file_name.split(" ")).strip('-').strip()
    file_name = '-'.join(file_name.split(".")).strip('-').strip()
    file_name = ''.join(file_name.split("--")).strip('-').strip()
    
    if failed:
        file_path = normpath(
            join(_output_folder, "_failed.txt")
        )
    else:
        file_path = normpath(
            join(_output_folder, f"{file_name}.txt")
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
        join(_clips_folder, clip)
    )
    _call(f'"{_ffprobe}" -i "{clip_path}"', f'ffprobe-{clip}')
    
    
def call_play(clip: str):    
    clip_path = normpath(
        join(_clips_folder, clip)
    )
    wait = 5
    print(f'ffplay.exe will take {wait} seconds to finish.\nPlaying "{clip}".')
    _call(f'"{_ffplay}" -infbuf -loop 1 -autoexit -cpucount 1 -nodisp -volume 0 -t {wait} -i "{clip_path}"', f'ffplay-{clip}')
    
    
def call_mpeg(clip: str):    
    clip_path = normpath(
        join(_clips_folder, clip)
    )
    _call(f'"{_ffmpeg}" "{clip_path}"', f'ffmpeg-{clip}')


def _run():
    if isdir(_output_folder):
        print(f'Deleting old output folder ("{_output_folder}").')
        rmtree(_output_folder)

    files = [
        f for f in listdir(_clips_folder) 
        if isfile(
            normpath(join(_clips_folder, f))
        )
        and 'git' not in f
        and 'thumb' not in f
    ]
    
    for file in files:
        call_probe(file)
        call_mpeg(file)
    
    for file in files:
        call_play(file)
    
    print('Done.')
    

if 'main' in __name__:
    _run()

