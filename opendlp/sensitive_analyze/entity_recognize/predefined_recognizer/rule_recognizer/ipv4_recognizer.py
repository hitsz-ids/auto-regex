from typing import Optional, List
import IPy
from opendlp.sensitive_analyze.entity_recognize import Pattern, PatternRecognizer


class Ipv4Recognizer(PatternRecognizer):
    """
    Recognize IP address using regex.

    :param patterns: List of patterns to be used by this recognizer
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "IPV4",
            r"\b((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}\b"
        )
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        supported_entity: str = "IPV4",
    ):
        patterns = patterns if patterns else self.PATTERNS
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns
        )

    def validate_result(self, pattern_text: str):  # noqa D102
        try:
            generate_version = IPy.IP(pattern_text).version()
            if generate_version == 4:
                return True
            else:
                return False
        except:
            return False