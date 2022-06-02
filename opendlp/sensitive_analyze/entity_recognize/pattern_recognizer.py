from typing import List
import datetime
import logging
import re

from opendlp.sensitive_analyze.entity_recognize import Pattern
from opendlp.sensitive_analyze.entity_recognize.entity_recognizer import EntityRecognizer
from opendlp.sensitive_analyze.entity_recognize.recognizer_result import RecognizerResult

LOGGER = logging.getLogger('SENSITIVE_DATA_ANALYZER')


class PatternRecognizer(EntityRecognizer):
    def __init__(
            self,
            supported_entity: str,
            name: str = None,
            patterns: List[Pattern] = None,
            version: str = "0.0.1",
    ):

        if not supported_entity:
            raise ValueError("Pattern recognizer should be initialized with entity")

        super().__init__(
            supported_entity=supported_entity,
            name=name,
            version=version,
        )
        if patterns is None:
            self.patterns = []
        else:
            self.patterns = patterns

    def load(self) -> None:
        pass

    def analyze(
            self, text: str, flags: int = None
    ) -> List[RecognizerResult]:
        """
        Evaluate all patterns in the provided text.

        Including words in the provided deny-list

        :param text: text to analyze
        :param flags: regex flags
        :return: A list of RecognizerResult
        """
        flags = flags if flags else re.DOTALL | re.MULTILINE
        results = []
        for pattern in self.patterns:
            match_start_time = datetime.datetime.now()
            matches = re.finditer(pattern.regex, text, flags=flags)
            match_time = datetime.datetime.now() - match_start_time
            LOGGER.debug(
                "--- match_time[%s]: %s.%s seconds",
                pattern.name,
                match_time.seconds,
                match_time.microseconds,
            )

            for match in matches:
                start, end = match.span()
                current_match = text[start:end]

                # Skip empty results
                if current_match == "":
                    continue

                if current_match[0] == ' ':
                    start = start + 1
                    current_match = current_match[1:]

                validation_result = True
                if hasattr(self, 'validate_result'):
                    validation_result = self.validate_result(current_match)

                pattern_result = RecognizerResult(
                    self.supported_entity, start, end
                )

                if validation_result is True:
                    results.append(pattern_result)

        results = EntityRecognizer.remove_duplicates(results)
        return results