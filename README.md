# brighttalk-recover
Recover your uploaded BrightTalk videos by downloading them using ffmpeg and python.

## Dependencies 

This program requires you have ffmpeg installed on your system. 

For MacOS 

```zsh
brew install ffmpeg
```

For Debian based 

```sh
apt-get update
apt-get install ffmpeg
```

For Windows 

```cmd 

```

## Architecture 

This application uses FFMPEG to blah. m3u8_To_MP4 is the python library used to convert the m3u8 stream to MP4 and requires FFMPEG. We also require FFMPEG python itself because we need to set the specific path for m3u8 to use. 

## Usage 

## Installation 

Just download this repository, install dependencies, and run! 

1. Dowload 

```sh 
# Clone via Git
git clone https://
# or Download Zip
wget -wLo https://
```

2. Install the dependencies 

```sh 
# Change directory to project download location 
cd brighttalk-recover
# Use pip to install requirements from requirements.txt file: 
pip install -r requirements.txt
```

3. Run the program 

```sh
# From the program directory
python btalk-recover --url https://cloudfront.com/something.m3u8 --output /tmp/video.mp4
```
