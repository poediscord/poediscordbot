from abc import ABC, abstractmethod

from poediscordbot.pob_xml_parser.models.build import Build


class AbstractAggregator(ABC):

    def __init__(self, build: Build) -> None:
        self.build = build

    @abstractmethod
    def get_output(self) -> (str, str):
        pass
