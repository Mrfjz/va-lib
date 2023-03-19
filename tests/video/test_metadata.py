import datetime
import json
import os
import subprocess
from tempfile import NamedTemporaryFile

import pytest
import pytz

from va_lib.video.metadata import WriteMetadataError, write_datetime_metadata


@pytest.fixture
def video_file_path(tmp_path: str) -> str:
    # Create a temporary video file for testing
    path = tmp_path / "test_video.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-f",
            "lavfi",
            "-i",
            "testsrc=size=1920x1080:rate=30",
            "-t",
            "1",
            "-pix_fmt",
            "yuv420p",
            str(path),
        ]
    )
    yield str(path)
    # Remove the temporary video file
    os.remove(str(path))


class TestWriteDatetimeMetadata:
    def test_write_datetime_metadata(self, video_file_path: str) -> None:
        # Set the creation datetime to a known value with a timezone
        creation_datetime = datetime.datetime(2022, 3, 19, 12, 0, 0, tzinfo=pytz.UTC)

        # Write the creation datetime metadata to the video file
        write_datetime_metadata(video_file_path, creation_datetime)

        # Read the creation datetime metadata from the video file
        output = os.popen(
            f"ffprobe -v quiet -print_format json -show_format -show_streams {video_file_path}"
        ).read()
        metadata = json.loads(output)["format"]["tags"]

        # Remove the timezone information from the metadata
        creation_time_str = metadata["creation_time"].replace("Z", "")

        # Convert the metadata to a datetime object with a timezone
        metadata_datetime = datetime.datetime.fromisoformat(creation_time_str).replace(
            tzinfo=pytz.UTC
        )

        # Assert that the metadata datetime matches the creation datetime
        assert metadata_datetime == creation_datetime

    def test_with_invalid_file_path(self):
        # Create a temporary file to use as the video file path
        with NamedTemporaryFile(delete=False) as temp_file:
            # Remove the temporary file so that it no longer exists
            os.remove(temp_file.name)

            # Attempt to write the creation datetime metadata to the non-existent video file
            creation_datetime = datetime.datetime.now()
            with pytest.raises(WriteMetadataError):
                write_datetime_metadata(temp_file.name, creation_datetime)
