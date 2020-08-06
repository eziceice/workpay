import pathlib
import yaml
import logging


class AppProperties:
    def __init__(self):
        with open(f'{pathlib.Path(__file__).parent}/resources/app.yml', 'r') as stream:
            try:
                self.properties = yaml.safe_load(stream)
            except yaml.YAMLError:
                logging.exception("Couldn't read yaml properties...")

    @property
    def org(self):
        return self.properties['org']

    @property
    def env(self):
        return self.properties['env']

    @property
    def assembly_payment_url(self):
        return self.properties['assembly-payment']['url']