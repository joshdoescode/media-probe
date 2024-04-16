# Media probe

Download the `ffmpeg` suite from `https://ffmpeg.org` and copy the `exe` files from the `bin` folder into this
folder (forming `[repo]/ffprobe.exe`, and so on).

Put the clips being used in the `./clips` folder.
The list of clip names to use can be found within the `run()` function.

_TODO: scan the dir for files automatically._

For each clip specified in the list:

- Run `ffprobe`, `ffmpeg`, and `ffplay`, on them
- Output the results to the `output` folder

Run:

```shell
python run.py
```
