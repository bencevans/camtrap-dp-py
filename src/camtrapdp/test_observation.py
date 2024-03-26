from . import Observation
from tempfile import NamedTemporaryFile


def test_read_from_csv():
    print(Observation.__annotations__)
    observations = Observation.from_csv("fixtures/observations.csv")
    print(observations)
    assert len(observations) == 549


def test_write_to_csv():
    observations = Observation.from_csv("fixtures/observations.csv")
    with NamedTemporaryFile(mode="w", delete=True) as file:
        Observation.to_csv(observations, file.name)
        with open("fixtures/observations.csv", "r", encoding="utf-8-sig") as original:
            with open(file.name, "r", encoding="utf-8-sig") as new:
                assert original.read() == new.read()


def test_to_from_pandas():
    observations = Observation.from_csv("fixtures/observations.csv")
    dataframe = Observation.to_pandas(observations)
    new_observations = Observation.from_pandas(dataframe)
    assert len(observations) == len(new_observations)
    for old, new in zip(observations, new_observations):
        assert old == new
