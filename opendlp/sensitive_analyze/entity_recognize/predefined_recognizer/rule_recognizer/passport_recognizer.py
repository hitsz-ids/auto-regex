from typing import List, Optional

from opendlp.sensitive_analyze.entity_recognize import Pattern, PatternRecognizer


class PassportRecognizer(PatternRecognizer):
    """
    Recognize passport number using regex.

    :param patterns: List of patterns to be used by this recognizer
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "PASSPORT",
            r"\b((E|G)\d{8})|(E([A-H]|[J-N]|[P-Z])\d{7})\b"
        ),
    ]

    def __init__(
            self,
            patterns: Optional[List[Pattern]] = None,
            supported_entity: str = "PASSPORT",
    ):
        patterns = patterns if patterns else self.PATTERNS
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns
        )

