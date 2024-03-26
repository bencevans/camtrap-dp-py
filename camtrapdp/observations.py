"""
Camtrap Data Package observations module
"""

from dataclasses import dataclass, asdict
from typing import Optional, List
from enum import Enum
from csv import DictReader, DictWriter
from pandas import DataFrame


@dataclass
class Observation:
    """
    An observation is a classification of an individual or group of individuals
    in a media file or event.
    """

    observationID: str
    """
    Unique identifier of the observation.
    """

    deploymentID: str
    """
    Identifier of the deployment the observation belongs to. Foreign key to
    `deployments.deploymentID`.
    """

    mediaID: Optional[str]
    """
    Identifier of the media file that was classified. Only applicable for
    media-based observations (`observationLevel` = `media`). Foreign key to
    `media.mediaID`.
    """

    eventID: Optional[str]
    """
    Identifier of the event the observation belongs to. Facilitates linking
    event-based and media-based observations with a permanent identifier.
    """

    eventStart: str
    """
    Date and time at which the event started. Formatted as an ISO 8601 string
    with timezone designator (YYYY-MM-DDThh:mm:ssZ or
    YYYY-MM-DDThh:mm:ss±hh:mm).
    """

    eventEnd: str
    """
    Date and time at which the event ended. Formatted as an ISO 8601 string with
    timezone designator (YYYY-MM-DDThh:mm:ssZ or YYYY-MM-DDThh:mm:ss±hh:mm).
    """

    class ObservationLevel(Enum):
        """
        Level of the observation. Can be either `event` or `media`.
        """

        EVENT = "event"
        MEDIA = "media"

    observationLevel: ObservationLevel
    """
    Level at which the observation was classified. media for media-based
    observations that are directly associated with a media file (mediaID). These
    are especially useful for machine learning and don’t need to be mutually
    exclusive (e.g. multiple classifications are allowed). event for event-based
    observations that consider an event (comprising a collection of media files).
    These are especially useful for ecological research and should be mutually
    exclusive, so that their count can be summed.
    """

    class ObservationType(Enum):
        """
        Type of the observation.
        """

        ANIMAL = "animal"
        HUMAN = "human"
        VEHICLE = "vehicle"
        BLANK = "blank"
        UNKNOWN = "unknown"
        UNCLASSIFIED = "unclassified"

    observationType: ObservationType
    """
    Type of the observation. All categories in this vocabulary have to be
    understandable from an AI point of view. unknown describes classifications
    with a classificationProbability below some predefined threshold i.e. neither
    humans nor AI can say what was recorded.
    """

    class CameraSetupType(Enum):
        """
        Type of the camera setup.
        """

        SETUP = "setup"
        CALIBRATION = "calibration"

    cameraSetupType: Optional[CameraSetupType]
    """
    Type of the camera setup action (if any) associated with the observation.
    """

    scientificName: Optional[str]
    """
    Scientific name of the observed individual(s).
    """

    count: Optional[int]
    """
    Number of observed individuals (optionally of given life stage, sex and
    behavior).
    """

    class LifeStage(Enum):
        """
        Life stage of the observed individual(s).
        """

        ADULT = "adult"
        SUBADULT = "subadult"
        JUVENILE = "juvenile"

    lifeStage: Optional[LifeStage]
    """
    Age class or life stage of the observed individual(s).
    """

    class Sex(Enum):
        """
        Sex of the observed individual(s).
        """

    sex: Optional[Sex]
    """
    Sex of the observed individual(s)
    """

    behavior: Optional[str]
    """
    Dominant behavior of the observed individual(s), preferably expressed as
    controlled values (e.g. grazing, browsing, rooting, vigilance, running,
    walking). Formatted as a pipe (|) separated list for multiple values, with
    the dominant behavior listed first.
    """

    individualID: Optional[str]
    """
    Identifier of the observed individual.
    """

    individualPositionRadius: Optional[float]
    """
    Distance from the camera to the observed individual identified by
    individualID. Expressed in meters. Required for distance analyses (e.g. Howe
    et al. 2017) and random encounter modelling (e.g. Rowcliffe et al. 2011).
    """

    individualPositionAngle: Optional[float]
    """
    Angular distance from the camera view centerline to the observed individual
    identified by individualID. Expressed in degrees, with negative values left,
    0 straight ahead and positive values right. Required for distance analyses
    (e.g. Howe et al. 2017) and random encounter modelling (e.g. Rowcliffe et
    al. 2011).
    """

    individualSpeed: Optional[float]
    """
    Average movement speed of the observed individual identified by individualID.
    Expressed in meters per second. Required for random encounter modelling (e.g.
    Rowcliffe et al. 2016).
    """

    bboxX: Optional[float]
    """
    Horizontal position of the top-left corner of a bounding box that
    encompasses the observed individual(s) in the media file identified by
    mediaID. Or the horizontal position of an object in that media file.
    Measured from the left and relative to media file width.
    """

    bboxY: Optional[float]
    """
    Vertical position of the top-left corner of a bounding box that encompasses
    the observed individual(s) in the media file identified by mediaID. Or the
    vertical position of an object in that media file. Measured from the top and
    relative to the media file height.
    """

    bboxWidth: Optional[float]
    """
    Width of a bounding box that encompasses the observed individual(s) in the
    media file identified by mediaID. Measured from the left of the bounding box
    and relative to the media file width.
    """

    bboxHeight: Optional[float]
    """
    Height of the bounding box that encompasses the observed individual(s) in
    the media file identified by mediaID. Measured from the top of the bounding
    box and relative to the media file height.
    """

    class ClassificationMethod(Enum):
        """
        Method used for the classification.
        """

        HUMAN = "human"
        MACHINE = "machine"

    classificationMethod: Optional[ClassificationMethod]
    """
    Method (most recently) used to classify the observation.
    """

    classifiedBy: Optional[str]
    """
    Name or identifier of the person or AI algorithm that (most recently)
    classified the observation.
    """

    classificationTimestamp: Optional[str]
    """
    Date and time of the (most recent) classification. Formatted as an ISO 8601
    string with timezone designator (YYYY-MM-DDThh:mm:ssZ or
    YYYY-MM-DDThh:mm:ss±hh:mm).
    """

    classificationProbability: Optional[float]
    """
    Degree of certainty of the (most recent) classification. Expressed as a
    probability, with 1 being maximum certainty. Omit or provide an approximate
    probability for human classifications.
    """

    observationTags: Optional[str]
    """
    Tag(s) associated with the observation. Formatted as a pipe (|) separated
    list for multiple values, with values optionally formatted as key:value
    pairs.
    """

    observationComments: Optional[str]
    """
    Comments or notes about the observation.
    """

    @staticmethod
    def from_csv(file_path: str) -> List["Observation"]:
        """
        Read observation objects from a CSV file.

        Args:
            file_path: Path to the CSV file.

        Returns:
            List of observation objects.
        """

        with open(file_path, "r", encoding="utf-8-sig") as file:
            reader = DictReader(file)
            return [Observation(**row) for row in reader]

    @staticmethod
    def to_csv(observations: List["Observation"], file_path: str):
        """
        Write observation objects to a CSV file.

        Args:
            observations: List of observation objects.
            file_path: Path to the CSV file.
        """
        with open(file_path, "w") as file:
            writer = DictWriter(
                file, fieldnames=Observation.__dataclass_fields__.keys()
            )
            writer.writeheader()
            writer.writerows([asdict(m) for m in observations])

    @staticmethod
    def to_pandas(observations: List["Observation"]):
        """
        Convert observation objects to a pandas DataFrame.

        Args:
            observations: List of observation objects.

        Returns:
            DataFrame of observation objects.
        """
        return DataFrame([observation.__dict__ for observation in observations])

    @staticmethod
    def from_pandas(dataframe: DataFrame) -> List["Observation"]:
        """
        Convert observation objects from a pandas DataFrame.

        Args:
            dataframe: DataFrame of observation objects.

        Returns:
            List of observation objects.
        """

        return [Observation(**row) for index, row in dataframe.iterrows()]
