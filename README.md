# Animation frame ranges finder

Script that finds all animated sequences in a given directory and prints their frame ranges in the following format if they math a regex expression:
  - 'name: 1001-2000' if there are no gaps
  - 'name: 1001, 1003-1500, 1600-2000' if there are gaps
         
The format for an animated sequence is name.####.ext e.g. /job/.../my_render_v001.1001.jpg

## How to use it

### Help

`python find_animated_sequences_frame_range.py -h`

![GitHub Logo](/static/python_frame_range_tool1.png)

### Running it

`python find_animated_sequences_frame_range.py --folder_path <folder_path>`

### Testing it

`cd python`

`python find_animated_sequences_frame_range.py --folder_path synthetic_data/`

![GitHub Logo](/static/python_frame_range2.png)