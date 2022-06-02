from typing import List, Optional

from opendlp.sensitive_analyze.entity_recognize import Pattern, PatternRecognizer


class MacRecognizer(PatternRecognizer):
    """
    Recognize MAC addresses using regex.

    :param patterns: List of patterns to be used by this recognizer
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "MAC_ADDRESS",
            r"\b[0-9A-F]{2}(\:[0-9A-F]{2}){5}\b",
        ),
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        supported_entity: str = "MAC_ADDRESS",
    ):
        patterns = patterns if patterns else self.PATTERNS
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns
        )
