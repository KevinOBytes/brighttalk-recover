import ffmpeg 
import m3u8_To_MP4 as m3
import argparse
import os
import sys
from . import __version__ as version

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Download a BrightTalk video')
    parser.add_argument('--url', type=str, required=True, help='The BrightTalk video URL')
    parser.add_argument('--output', type=str, required=True, help='The output file name')
    parser.add_argument('--dry-run', action='store_true', help='Do not download the video, just print the command that would be run')
    parser.add_argument('--force', action='store_true', help='Force the download even if the output file already exists')
    parser.add_argument('--os', type=str, help='The operating system to use (e.g. linux, mac, windows)')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--quiet', action='store_true', help='Enable quiet output')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    parser.add_argument('--ffmpeg', type=str, help='Path to the ffmpeg binary (e.g. like /opt/homebrew/bin/ffmpeg)')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing files')
    parser.add_argument('--version', action='version', version=version, help='Print the version number and exit')
    return parser.parse_args()

def check_args(args):
    if args.verbose:
        print('Verbose output enabled')
    if args.quiet:
        print('Quiet output enabled')
    if args.debug:
        print('Debug output enabled')
    if args.dry_run:
        print('Dry run enabled')
    if args.force:
        print('Force enabled')
    if args.os:
        print(f'Operating system: {args.os}')
    if args.ffmpeg:
        print(f'Using ffmpeg binary: {args.ffmpeg}')
    if args.overwrite:
        print('Overwrite enabled')

def check_ffmpeg(ffmpeg_path=None):
    """Check if ffmpeg binary is available."""
    if ffmpeg_path:
        if not os.path.isfile(ffmpeg_path) or not os.access(ffmpeg_path, os.X_OK):
            print(f'ffmpeg binary at {ffmpeg_path} is not executable or does not exist.')
            sys.exit(1)
    else:
        if os.system('which ffmpeg') != 0:
            print('ffmpeg is not installed. Please install it before running this script. See https://ffmpeg.org/download.html for instructions or README.md')
            sys.exit(1)

def ensure_output_directory(output_file):
    """Ensure the output directory exists."""
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

if __name__ == '__main__': 
    print(f'Starting BrightTalk-Recover version {version}')
    
    # Parse the command line arguments
    args = parse_arguments()
    check_args(args)

    # Ensure the output directory exists
    ensure_output_directory(args.output)

    # Set the m3u8_url and output_file for where we get the video stream from and where we save it
    m3u8_url = args.url
    output_file = args.output

    print(f'Downloading video from {m3u8_url} to {output_file}')

    if args.ffmpeg:
        check_ffmpeg(args.ffmpeg)
        ffmpeg_cmd = args.ffmpeg
    else:
        check_ffmpeg()
        ffmpeg_cmd = 'ffmpeg'

    if not args.dry_run:
        try:
            ffmpeg.input(m3u8_url).output(output_file).run(cmd=ffmpeg_cmd)
        except ffmpeg.Error as e:
            print(f'Error running ffmpeg: {e}')
            sys.exit(1)

    print('Finished!')
