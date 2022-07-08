from typing import List, Optional

from opendlp.sensitive_analyze.entity_recognize import Pattern, PatternRecognizer


class LicensePlateRecognizer(PatternRecognizer):
    """
    Recognize license plate number using regex.

    :param patterns: List of patterns to be used by this recognizer
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "LICENSE_PLATE",
            r"\b[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领][A-Z](([0-9A-Z]{5})|([D|F][0-9A-Z]{5}))\b"
        ),
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        supported_entity: str = "LICENSE_PLATE",
    ):
        patterns = patterns if patterns else self.PATTERNS
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns
        )