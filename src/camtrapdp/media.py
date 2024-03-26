"""
Camtrap Data Package media module
"""

from dataclasses import dataclass, asdict
from typing import Optional, List
from enum import Enum
from csv import DictReader, DictWriter
from pandas import DataFrame


@dataclass
class Media:
    """
    A media object represents a single image or video file captured by a camera
    trap.
    """

    mediaID: str
    """
    Unique identifier of the media object.
    """

    deploymentID: str
    """
    Identifier of the deployment the media file belongs to. Foreign key to
    deployments.deploymentID.
    """

    class CaptureMethod(Enum):
        ACTIVITY_DETECTION = "activityDetection"
        TIME_LAPSE = "timeLapse"

    captureMethod: Optional[CaptureMethod]
    """
    Method used to capture the media file.
    """

    timestamp: str
    """
    Date and time at which the media file was recorded. Formatted as an ISO
    8601 string with timezone designator (YYYY-MM-DDThh:mm:ssZ or
    YYYY-MM-DDThh:mm:ss±hh:mm).
    """

    filePath: str
    """
    URL or relative path to the media file, respectively for externally hosted
    files or files that are part of the package.
    """

    filePublic: bool
    """
    false if the media file is not publicly accessible (e.g. to protect the
    privacy of people).
    """

    fileName: Optional[str]
    """
    Name of the media file. If provided, one should be able to sort media files
    chronologically within a deployment on timestamp (first) and fileName
    (second).
    """

    fileMediatype: str
    """
    Mediatype of the media file. Expressed as an IANA Media Type.
    """

    exifData: Optional[dict]
    """
    EXIF data of the media file. Formatted as a valid JSON object.
    """

    favorite: Optional[bool]
    """
    true if the media file is deemed of interest (e.g. an exemplar image of an individual).
    """

    mediaComments: Optional[str]
    """
    Comments or notes about the media file.
    """

    @staticmethod
    def from_csv(file_path: str) -> List["Media"]:
        """
        Read media objects from a CSV file.

        Args:
            file_path: Path to the CSV file.

        Returns:
            List of media objects.
        """

        with open(file_path, "r", encoding="utf-8-sig") as file:
            reader = DictReader(file)
            return [Media(**row) for row in reader]

    @staticmethod
    def to_csv(media: List["Media"], file_path: str):
        """
        Write media objects to a CSV file.

        Args:
            media: List of media objects.
            file_path: Path to the CSV file.
        """

        with open(file_path, "w") as file:
            writer = DictWriter(file, fieldnames=Media.__dataclass_fields__.keys())
            writer.writeheader()
            writer.writerows([asdict(m) for m in media])

    @staticmethod
    def to_pandas(media: List["Media"]) -> DataFrame:
        """
        Convert media objects to a pandas DataFrame.

        Args:
            media: List of media objects.

        Returns:
            DataFrame of media objects.
        """

        return DataFrame([asdict(m) for m in media])

    @staticmethod
    def from_pandas(dataframe: DataFrame) -> List["Media"]:
        """
        Convert media objects from a pandas DataFrame.

        Args:
            dataframe: DataFrame of media objects.

        Returns:
            List of media objects.
        """

        return [Media(**row) for index, row in dataframe.iterrows()]
