from typing import List, Optional
import json
import itertools

from opendlp.sensitive_analyze.entity_recognize import Pattern, PatternRecognizer
from opendlp.sensitive_analyze.entity_recognize.conf import config


class TelephoneRecognizer(PatternRecognizer):
    """
    Recognize telephone number using regex.

    :param patterns: List of patterns to be used by this recognizer
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "TELEPHONE",
            r"\s*((\(0\d{2,3}\))|(0\d{2,3}))-?\d{7,8}((-\d{1,6})?)\b"
        )
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        supported_entity: str = "TELEPHONE",
    ):
        patterns = patterns if patterns else self.PATTERNS
        self.telephone_code = json.load(open(config.TELEPHONE_CODE_FILE,
                                             'r', encoding='utf-8'))
        self.area_codes = list(itertools.chain(*self.telephone_code.values()))

        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns
        )

    def validate_result(self, pattern_text: str):
        if pattern_text[0] == '(':
            area_code = pattern_text[1:5]
        else:
            area_code = pattern_text[:4]

        if area_code in self.area_codes or area_code[:-1] in self.area_codes:
            return True
        else:
            return False
