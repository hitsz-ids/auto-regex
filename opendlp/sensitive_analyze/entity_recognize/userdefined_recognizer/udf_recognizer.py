from typing import List

from opendlp.sensitive_analyze.entity_recognize import Pattern, PatternRecognizer


class UDFRecognizer(PatternRecognizer):
    """
    Recognize user defined entity using regex defined by user.

    :param patterns: List of patterns to be used by this recognizer
    :param supported_entity: The entity this recognizer can detect
    """

    def __init__(
        self,
        patterns: List[Pattern],
        supported_entity: str,
    ):
        if not patterns:
            raise ValueError("UDFRecognizer should be initialized with patterns")

        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns
        )
