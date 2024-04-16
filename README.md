# Media probe

Download the `ffmpeg` suite, and copy the `exe` files from the `bin` folder into this
repo (forming `[repo]/ffprobe.exe`, and so on).

For each clip specified in the list _(TODO: scan the dir for files automatically)_, run `ffprobe`, `ffmpeg`,
and `ffplay`, on them, and output the results to the `output` folder.

Put the clips in the `./clips` folder.

Run:

```shell
python run.py
```
