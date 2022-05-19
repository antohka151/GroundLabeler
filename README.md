# Ground Labeler
It's a tool to label body key points that are touching the ground.

## Getting started

### Installation

- Clone this repo
```buildoutcfg
git clone git@github.com:aibodygym/GroundLabeler
cd GroundLabeler
```
- Create and activate a virtual environment to work in, e.g. using Conda
```buildoutcfg
conda create -n GroundLabeler python=3.10
conda activate GroundLabeler
```
```mkdir libs```
- Download tensorflow.
- Install the requirements with pip
```buildoutcfg
pip install -r requirements.txt
```
NOTE: Tensorflow is only needed when you need to generate a video_name.csv file.
### Put videos that you want to label to the ‘assets/videos’ folder

### Run tool

```buildoutcfg
python main.py
```

## Labelling process

### Choose a video that you want to label

- Use automatic choose (a or auto)
```buildoutcfg
a
```

- Select the video manually (this video must be located in the ‘assets/videos’ folder)
```buildoutcfg
vidname.mp4
```

## Start labeling

In folder ‘assets/labelling_video’ would be generated annotated video, use it to see keypoints flags

- Use h or help to get help (to get input formats and key points shortcuts).
```buildoutcfg
h
```
- Use u to update video in ‘assets/labelling_video’.
```buildoutcfg
u
```
- Use e to end labelling process.
```buildoutcfg
e
```

### Choose key points

Input format - keypoints or shortcuts that are separated by a space bar
```buildoutcfg
odd 16 lfoot
```
##### Shortcut list:
- odd - all odd keypoints (left part of the body)
- even - all even keypoints (right part of the body)
- lfoor or rfoot - left or right foot (stopa)
- lhand or rhand - left or right hand (licevaya chast)

### Choose a frame range where to change the flag value

Input format - two integers that are separated by a space bar
They mean the range of frames, where both of them are included (f1<=X<=f2)
```buildoutcfg
1 30
```
NOTE: The first frame has number one
NOTE: If we want to select one frame, we will still need to write 2 numbers (f.e. 25 25)

### Choose a flag value
- 1 - Touching the ground
- 0 - Doesn't touch the ground
