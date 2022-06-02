from abc import abstractmethod
from typing import List, Dict

from opendlp.sensitive_analyze.entity_recognize import RecognizerResult


class EntityRecognizer:
    """
    A class representing an abstract PII entity recognizer.

    EntityRecognizer is an abstract class to be inherited by
    Recognizers which hold the logic for recognizing specific PII entities.

    :param supported_entities: the entities supported by this recognizer
    (for example, phone number, address, etc.)
    :param name: the name of this recognizer (optional)
    :param version: the recognizer current version
    """

    def __init__(
        self,
        supported_entity: str,
        name: str = None,
        version: str = "0.0.1",
    ):

        self.supported_entity = supported_entity

        if name is None:
            self.name = self.__class__.__name__  # assign class name as name
        else:
            self.name = name

        self.version = version


    @abstractmethod
    def analyze(
        self, text: str
    ):
        """
        Analyze text to identify entities.

        :param text: The text to be analyzed
        :param entities: The list of entities this recognizer is able to detect
        :return: List of results detected by this recognizer.
        """
        return None

    def get_supported_entities(self) -> List[str]:
        """
        Return the list of entities this recognizer can identify.

        :return: A list of the supported entities by this recognizer
        """
        return self.supported_entities

    def get_version(self) -> str:
        """
        Return the version of this recognizer.

        :return: The current version of this recognizer
        """
        return self.version

    def to_dict(self) -> Dict:
        """
        Serialize self to dictionary.

        :return: a dictionary
        """
        return_dict = {
            "supported_entities": self.supported_entities,
            "name": self.name,
            "version": self.version,
        }
        return return_dict

    @classmethod
    def from_dict(cls, entity_recognizer_dict: Dict) -> "EntityRecognizer":
        """
        Create EntityRecognizer from a dict input.

        :param entity_recognizer_dict: Dict containing keys and values for instantiation
        """
        return cls(**entity_recognizer_dict)


    @staticmethod
    def remove_duplicates(results: List[RecognizerResult]) -> List[RecognizerResult]:
        """
        Remove duplicate results.

        Remove duplicates in case the two results
        have identical start and ends and types.
        :param results: List[RecognizerResult]
        :return: List[RecognizerResult]
        """
        results = list(set(results))
        results = sorted(results, key=lambda x: (x.start, -(x.end - x.start)))
        filtered_results = []

        for result in results:
            to_keep = result not in filtered_results  # equals based comparison
            if to_keep:
                for filtered in filtered_results:
                    # If result is contained in one of the other results
                    if (
                        result.contained_in(filtered)
                        and result.entity_type == filtered.entity_type
                    ):
                        to_keep = False
                        break

            if to_keep:
                filtered_results.append(result)

        return filtered_results
