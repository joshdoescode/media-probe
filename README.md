# Media probe

Each run deletes the old output files (by deleting the folder itself recursively).

For each clip in the clips folder:

- Run `ffprobe` and `ffmpeg` against them
- Output the results to the `output` folder
- Run `ffplay` against them
- After X seconds, stop the `ffplay` and output the results to the `output` folder
- Output any failed runs to the `output/_failed.txt` file

## Setup

Download the `ffmpeg` suite from `https://ffmpeg.org` and copy the `exe` files from the resulting `bin` folder into this
folder (forming `[repo]/ffprobe.exe`, and so on).

Put the clips to be used in the `./clips` folder.

## Run

```shell
python run.py
```

## Notes

This project forms absolute paths based on the `run.py` file itself, so you should be able to call it from any 
other directory, and have it still work.
