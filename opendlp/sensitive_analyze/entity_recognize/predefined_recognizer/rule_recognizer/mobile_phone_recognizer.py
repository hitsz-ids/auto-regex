from typing import List, Optional
import json
import itertools

from opendlp.sensitive_analyze.entity_recognize import Pattern, PatternRecognizer
from opendlp.sensitive_analyze.entity_recognize.conf import config


class MobilePhoneRecognizer(PatternRecognizer):
    """
    Recognize mobile phone number using regex.

    :param patterns: List of patterns to be used by this recognizer
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "MOBILE_PHONE",
            r"\s(((\+86))|(\(\+86\)))?1[3456789]\d{9}\b"
        ),
        Pattern(
            "MOBILE_PHONE",
            r"\s(((\+86))|(\(\+86\)))?1[3456789][0-9]-[0-9]{4}-[0-9]{4}\b"
        )
    ]

    def __init__(
            self,
            patterns: Optional[List[Pattern]] = None,
            supported_entity: str = "MOBILE_PHONE",
    ):
        patterns = patterns if patterns else self.PATTERNS
        self.mobile_phone_codes = json.load(open(config.MOBILE_PHONE_FILE, 'r',
                                                 encoding='utf-8'))
        self.mobile_phone_codes = list(itertools.chain(*self.mobile_phone_codes.values()))

        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns
        )

    def validate_result(self, pattern_text: str):
        # 前两个顺序不能变，后两个的顺序也不能变
        prefixes = ("(+86) ", "(+86)", "+86 ", "+86")
        start_index = 0
        for prefix in prefixes:
            if pattern_text.startswith(prefix):
                start_index = len(prefix)
                break

        # 去掉分隔符，空格在做正则之前已去除
        pattern_text = pattern_text.replace('-', '')
        # 号段，有3位的和4位的，先取4位
        number_code = pattern_text[start_index:start_index+4]
        if number_code[:-1] in self.mobile_phone_codes or \
            number_code in self.mobile_phone_codes:
            return True
        else:
            return False