# Media probe

Download the `ffmpeg` suite, and copy the `exe` files from the `bin` folder into this
repo (forming `[repo]/ffprobe.exe`, and so on).

Put the clips being used in the `./clips` folder.
The list of clip names can be found within the `run()` function.

For each clip specified in the list _(TODO: scan the dir for files automatically)_:

- Run `ffprobe`, `ffmpeg`, and `ffplay`, on them
- Output the results to the `output` folder

Run:

```shell
python run.py
```
