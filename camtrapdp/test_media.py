from . import Media
from tempfile import NamedTemporaryFile


def test_read_from_csv():
    media = Media.from_csv("fixtures/media.csv")
    print(media)
    assert len(media) == 423


def test_write_to_csv():
    media = Media.from_csv("fixtures/media.csv")
    with NamedTemporaryFile(mode="w", delete=False) as file:
        Media.to_csv(media, file.name)
        with open("fixtures/media.csv", "r") as original:
            with open(file.name, "r") as new:
                assert original.read() == new.read()


def test_to_from_pandas():
    media = Media.from_csv("fixtures/media.csv")
    dataframe = Media.to_pandas(media)
    new_media = Media.from_pandas(dataframe)
    assert len(media) == len(new_media)
    for old, new in zip(media, new_media):
        assert old == new
