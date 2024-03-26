"""
Camtrap Data Package
"""

from dataclasses import dataclass
from typing import Optional, List
from enum import Enum
from csv import DictReader, DictWriter
from pandas import DataFrame


@dataclass
class Deployment:
    """
    A deployment is a period of time during which a camera trap is active at a specific location.
    """

    deploymentID: str
    """Unique identifier of the deployment."""

    locationID: Optional[str]
    """Identifier of the deployment location."""

    locationName: Optional[str]
    """Name given to the deployment location."""

    latitude: float
    """Latitude of the deployment location in decimal degrees, using the WGS84 datum."""

    longitude: float
    """Longitude of the deployment location in decimal degrees, using the WGS84 datum."""

    coordinateUncertainty: Optional[float]
    """Horizontal distance from the given latitude and longitude describing the smallest circle containing the deployment location. Expressed in meters. Especially relevant when coordinates are rounded to protect sensitive species."""

    deploymentStart: str
    """Date and time at which the deployment was started. Formatted as an ISO 8601 string with timezone designator (YYYY-MM-DDThh:mm:ssZ or YYYY-MM-DDThh:mm:ss±hh:mm)."""
    # TODO: Add datetime type

    deploymentEnd: str
    """Date and time at which the deployment was ended. Formatted as an ISO 8601 string with timezone designator (YYYY-MM-DDThh:mm:ssZ or YYYY-MM-DDThh:mm:ss±hh:mm)."""
    # TODO: Add datetime type

    setupBy: Optional[str]
    """Name or identifier of the person or organization that deployed the camera."""

    cameraID: Optional[str]
    """Identifier of the camera used for the deployment (e.g. the camera device serial number)."""

    cameraModel: Optional[str]
    """Manufacturer and model of the camera. Formatted as `manufacturer-model`."""

    cameraDelay: Optional[int]
    """Predefined duration after detection when further activity is ignored. Expressed in seconds."""

    cameraHeight: Optional[float]
    """Height at which the camera was deployed. Expressed in meters. Not to be combined with cameraDepth."""

    cameraDepth: Optional[float]
    """Depth at which the camera was deployed. Expressed in meters. Not to be combined with cameraHeight."""

    cameraTilt: Optional[int]
    """Angle at which the camera was deployed in the vertical plane. Expressed in degrees, with -90 facing down, 0 horizontal and 90 facing up."""

    cameraHeading: Optional[int]
    """Angle at which the camera was deployed in the horizontal plane. Expressed in decimal degrees clockwise from north, with values ranging from 0 to 360: 0 = north, 90 = east, 180 = south, 270 = west."""

    detectionDistance: Optional[float]
    """Maximum distance at which the camera can reliably detect activity. Expressed in meters. Typically measured by having a human move in front of the camera."""

    timestampIssues: Optional[bool]
    """true if timestamps in the media resource for the deployment are known to have (unsolvable) issues (e.g. unknown timezone, am/pm switch)."""

    baitUse: Optional[bool]
    """true if bait was used for the deployment. More information can be provided in tags or comments."""

    class FeatureType(str, Enum):
        """
        Type of the feature (if any) associated with the deployment.
        """

        ROAD_PAVED = "roadPaved"
        ROAD_DIRT = "roadDirt"
        TRAIL_HIKING = "trailHiking"
        TRAIL_GAME = "trailGame"
        ROAD_UNDERPASS = "roadUnderpass"
        ROAD_OVERPASS = "roadOverpass"
        ROAD_BRIDGE = "roadBridge"
        CULVERT = "culvert"
        BURROW = "burrow"
        NEST_SITE = "nestSite"
        CARCASS = "carcass"
        WATER_SOURCE = "waterSource"
        FRUITING_TREE = "fruitingTree"

    featureType: Optional[FeatureType]
    """Type of the feature (if any) associated with the deployment."""

    habitat: Optional[str]
    """Short characterization of the habitat at the deployment location."""

    deploymentGroups: Optional[str]
    """Deployment group(s) associated with the deployment. Deployment groups can have a spatial (arrays, grids, clusters), temporal (sessions, seasons, months, years) or other context. Formatted as a pipe (|) separated list for multiple values, with values preferably formatted as key:value pairs."""

    deploymentTags: Optional[str]
    """Tag(s) associated with the deployment. Formatted as a pipe (|) separated list for multiple values, with values optionally formatted as key:value pairs."""

    deploymentComments: Optional[str]
    """Comments or notes about the deployment."""

    @staticmethod
    def from_csv(file_path: str) -> List["Deployment"]:
        deployments = []
        with open(file_path, "r") as file:
            reader = DictReader(file)
            for row in reader:
                deployment = Deployment(**row)
                deployments.append(deployment)

        return deployments

    @staticmethod
    def to_csv(observations: List["Deployment"], file_path: str):
        with open(file_path, "w") as file:
            writer = DictWriter(file, fieldnames=Deployment.__dataclass_fields__.keys())
            writer.writeheader()
            for deployment in observations:
                writer.writerow(deployment.__dict__)

    @staticmethod
    def to_pandas(observations: List["Deployment"]):
        return DataFrame([deployment.__dict__ for deployment in observations])

    @staticmethod
    def from_pandas(dataframe: DataFrame) -> List["Deployment"]:
        deployments = []
        for index, row in dataframe.iterrows():
            deployment = Deployment(**row)
            deployments.append(deployment)

        return deployments
