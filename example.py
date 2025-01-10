import ffmpeg

m3u8_url = 'https://d3du34tj8zwe0z.cloudfront.net/19561-607664/index.m3u8'
output_file = 'output.mp4'
ffmpeg_path = '/opt/homebrew/bin/ffmpeg'  # Replace this with the actual path from `which ffmpeg`

try:
    # Download and convert the m3u8 file to mp4
    ffmpeg.input(m3u8_url).output(output_file).run(cmd=ffmpeg_path)
    print("Conversion successful!")
except ffmpeg.Error as e:
    print("An error occurred:", e)

import ffmpeg 
import m3u8_To_MP4 as m3 

def get_m3u8_link(url: str) -> str:
    """Get's the m3u8 asset link given a brighttalk video URL

    To be implemented in the future 

    For now we just expect to be given the m3u8 url
    
    Potentially solve using a wget, curl, request, etc. and filtering for m3u8.mpg assets 

    Probably need to set a fake UserAgent
    """

def download_video(url: str, output: str = output.mp4):
    m3u8_url = url 
    output_file = output

    ffmpeg_path = 'opt/homebrew/bin/ffmpeg'

    try: 
        ffmpeg.input(m3u8_url).output(output_file).run(cmd=ffmpeg_path)
    except ffmpeg.Error as e:
        print("An error ocurred:", e)


if __name__ == '__main__':

    m3u8_url = 'https://d3du34tj8zwe0z.cloudfront.net/19561-607664/index.m3u8'
    output_file = 'output.mp4'
    ffmpeg_path = '/opt/homebrew/bin/ffmpeg'  # Replace this with the actual path from `which ffmpeg`

    try:
        # Download and convert the m3u8 file to mp4
        ffmpeg.input(m3u8_url).output(output_file).run(cmd=ffmpeg_path)
        print("Conversion successful!")
    except ffmpeg.Error as e:
        print("An error occurred:", e)