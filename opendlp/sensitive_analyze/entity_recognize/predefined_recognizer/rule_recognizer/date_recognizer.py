from typing import List, Optional
from opendlp.sensitive_analyze.entity_recognize import Pattern, PatternRecognizer


class DateRecognizer(PatternRecognizer):
    """
    Recognize domain names using regex.

    :param patterns: List of patterns to be used by this recognizer
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "DATE",
            r"\b([0-9]{1,4}-[0-9]{1,2}-[0-9]{1,2})|([0-9]{1,4}\.[0-9]{1,2}\.[0-9]{1,2})|([0-9]{1,4}\/[0-9]{1,2}\/[0-9]{1,2})|([0-9]{1,4}年[0-9]{1,2}月[0-9]{1,2}日)\b"
        ),
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        supported_entity: str = "DATE",
    ):
        patterns = patterns if patterns else self.PATTERNS
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns
        )

    def get_year_moth_day(self, pattern_text): # noqa D102
        separators = ['-', '/', '.']
        for sep in separators:
            if sep in pattern_text:
                elements = pattern_text.split(sep)
                year, month, day = int(elements[0]), int(elements[1]), int(elements[2])
                return year, month, day

        try:
            year = int(pattern_text[:pattern_text.index("年")])
            month = int(pattern_text[(pattern_text.index("年") + 1):pattern_text.index("月")])
            day = int(pattern_text[(pattern_text.index("月") + 1):pattern_text.index("日")])
            return year, month, day
        except:
            raise ValueError('不支持的日期格式！')


    def valipattern_result(self, pattern_text: str):  # noqa D102
        year, month, day = self.get_year_moth_day(pattern_text)
        if month < 1 or month > 12:
            return False

        days = 31
        if month in [4, 6, 9, 11]:
            days = 30
        elif month == 2:
            if (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0):
                days = 29
            else:
                days = 28
        if day < 1 or day > days:
            return False

        return True
