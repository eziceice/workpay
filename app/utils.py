import pathlib
import yaml
import typing
import logging


def get_properties() -> typing.Dict[str, str]:
    with open(f'{pathlib.Path(__file__).parent}/resources/app.yml', 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError:
            logging.exception("Couldn't read yaml properties...")
