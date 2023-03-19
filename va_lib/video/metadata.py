import os
import subprocess
from datetime import datetime


class WriteMetadataError(Exception):
    """
    Exception raised when writing metadata to a video file fails.

    Attributes:
        cmd: The command that was executed.
        returncode: The exit code that was returned by the command.
        output: The output of the command as a string.
    """

    def __init__(self, cmd: list[str], returncode: int, output: str) -> None:
        self.cmd = cmd
        self.returncode = returncode
        self.output = output
        super().__init__(
            f"Error executing command: {cmd}. Returned {returncode} with output: {output}"
        )


def write_datetime_metadata(video_file_path: str, creation_datetime: datetime) -> None:
    """Write the creation datetime metadata to a video file using FFmpeg and subprocess.
    Note: When reading the creation datetime metadata from the video file using FFprobe or a similar tool,
    the timezone information should be ignored and the datetime should be treated as UTC.

    Args:
        video_file_path (str): The path to the video file.
        creation_datetime (datetime.datetime): The creation datetime to write to the video file.
            Note that this function is timezone unaware, and any timezone information in the creation_datetime
            argument will be ignored.

    Returns:
        None

    Raises:
        Exception: If the metadata writing fails.
    """
    # Format the creation datetime as an ISO-formatted string and add a "Z" character to indicate UTC
    creation_datetime_str = creation_datetime.replace(tzinfo=None).isoformat() + "Z"
    # Construct the FFmpeg command to write the creation datetime metadata
    # Use a new output file
    output_file_path = f"{os.path.splitext(video_file_path)[0]}_new.mp4"
    command = [
        "ffmpeg",
        "-i",
        video_file_path,
        "-metadata",
        f"creation_time={creation_datetime_str}",
        "-map_metadata",
        "0",
        "-c",
        "copy",
        "-y",  # Overwrite output file without asking
        output_file_path,
    ]

    # Execute the ffprobe command and capture the output
    try:
        subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
    except subprocess.CalledProcessError as error:
        raise WriteMetadataError(command, error.returncode, error.output) from error

    # Replace the original video file with the new output file
    os.replace(output_file_path, video_file_path)


# def read_datetime_metadata(video_file_path: str) -> datetime:
#     """Read the creation datetime metadata from a video file using ffprobe and subprocess.

#     Args:
#         video_file_path (str): The path to the video file.

#     Returns:
#         datetime.datetime: The creation datetime stored in the video file metadata.

#     Raises:
#         Exception: If the metadata reading fails or the metadata is not found.
#     """
#     # Construct the ffprobe command to read the creation datetime metadata
#     command = [
#         'ffprobe',
#         '-v', 'error',
#         '-select_streams', 'v:0',
#         '-show_entries', 'stream_tags=creation_time',
#         '-of', 'json',
#         video_file_path
#     ]

#     # Run the ffprobe command using subprocess
#     process = subprocess.run(command, capture_output=True)

#     # Check if the command was successful
#     if process.returncode != 0:
#         raise Exception(
#             f'Error reading datetime metadata for {video_file_path}: {process.stderr.decode("utf-8")}')

#     # Parse the ffprobe output as JSON
#     output_json = json.loads(process.stdout.decode('utf-8'))

#     # Try to extract the creation datetime from the ffprobe output
#     try:
#         datetime_str = output_json['streams'][0]['tags']['creation_time']
#     except (KeyError, IndexError):
#         raise Exception(
#             f'Error reading datetime metadata for {video_file_path}: metadata not found')

#     # Try to convert the datetime string to a datetime object
#     try:
#         creation_datetime = datetime.fromisoformat(datetime_str)
#     except ValueError:
#         raise Exception(
#             f'Error reading datetime metadata for {video_file_path}: invalid datetime format ({datetime_str})')

#     return creation_datetime
