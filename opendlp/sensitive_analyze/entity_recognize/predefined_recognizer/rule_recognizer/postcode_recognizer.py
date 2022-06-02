from typing import List, Optional
import json
import itertools

from opendlp.sensitive_analyze.entity_recognize import Pattern, PatternRecognizer
from opendlp.sensitive_analyze.entity_recognize.conf import config


class PostcodeRecognizer(PatternRecognizer):
    """
    Recognize postcode using regex.

    :param patterns: List of patterns to be used by this recognizer
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "POSTCODE",
            r"\b[0-9]{6}\b",
        ),
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        supported_entity: str = "POSTCODE",
    ):
        patterns = patterns if patterns else self.PATTERNS
        self.postcode = json.load(open(config.POST_CODE_FILE, 'r', encoding='utf-8'))
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns
        )

    def validate_result(self, pattern_text: str):
        post_code_pre_two = list(itertools.chain(*self.postcode.values()))
        if pattern_text[:2] in post_code_pre_two:
            return True
        elif pattern_text in ('999077', '999078', '999079'):
            return True
        return False
