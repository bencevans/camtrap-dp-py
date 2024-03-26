from . import Deployment
from tempfile import NamedTemporaryFile


def test_read_from_csv():
    deployments = Deployment.from_csv("fixtures/deployments.csv")
    assert len(deployments) == 4


def test_write_to_csv():
    deployments = Deployment.from_csv("fixtures/deployments.csv")
    with NamedTemporaryFile(mode="w", delete=True) as file:
        Deployment.to_csv(deployments, file.name)
        with open("fixtures/deployments.csv", "r", encoding="utf-8-sig") as original:
            with open(file.name, "r", encoding="utf-8-sig") as new:
                assert original.read() == new.read()


def test_to_from_pandas():
    deployments = Deployment.from_csv("fixtures/deployments.csv")
    dataframe = Deployment.to_pandas(deployments)
    new_deployments = Deployment.from_pandas(dataframe)
    assert len(deployments) == len(new_deployments)
    for old, new in zip(deployments, new_deployments):
        assert old == new
