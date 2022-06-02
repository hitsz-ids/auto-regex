from typing import Optional, List
import IPy

from opendlp.sensitive_analyze.entity_recognize import Pattern, PatternRecognizer


class Ipv6Recognizer(PatternRecognizer):
    """
    Recognize IP address using regex.

    :param patterns: List of patterns to be used by this recognizer
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "IPV6",
            # presidio
            r"\b(?!.*::.*::)(?:(?!:)|:(?=:))(?:[0-9a-f]{0,4}(?:(?<=::)|(?<!::):)){6}(?:[0-9a-f]{0,4}(?:(?<=::)|(?<!::):)[0-9a-f]{0,4}(?:(?<=::)|(?<!:)|(?<=:)(?<!::):)|(?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)){3})\b" # noqa: E501
        )
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        supported_entity: str = "IPV6",
    ):
        patterns = patterns if patterns else self.PATTERNS
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns
        )

    def validate_result(self, pattern_text: str):  # noqa D102
        try:
            generate_version = IPy.IP(pattern_text).version()
            if generate_version == 6:
                return True
            else:
                return False
        except:
            return False