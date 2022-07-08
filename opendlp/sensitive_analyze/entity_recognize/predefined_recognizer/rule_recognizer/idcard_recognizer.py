from typing import List, Optional
from opendlp.sensitive_analyze.entity_recognize import Pattern, PatternRecognizer

class IDCardRecognizer(PatternRecognizer):
    """
    Recognize ID card number(length 18) using regex.

    :param patterns: List of patterns to be used by this recognizer
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "ID_CARD",
            r'\b([1-9]\d{5}[12]\d{3}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])\d{3}[0-9xX])\b'
        )
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        supported_entity: str = "ID_CARD",
    ):
        patterns = patterns if patterns else self.PATTERNS
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns
        )

def check_code_check(id_card: str): # noqa D102
    weightFactor = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]  # 校验和系数
    check_code_dic = {'0': '1', '1': '0', '2': 'X', '3': '9', '4': '8', '5': '7', '6': '6', '7': '5', '8': '4',
                      '9': '3', '10': '2'}  # 余数对应的最后一位号码

    # 校验和
    sum = 0
    for i in range(0, 17):
        sum += int(id_card[i]) * weightFactor[i]

    # 校验和除以11取余数，再转换为1位校验数
    check_code = sum % 11
    check_code = check_code_dic[str(check_code)]

    if check_code == id_card[-1]:
        return True
    else:
        return False

    # 检查中间的出生日期码是否合法：第11位-14位
def birthday_check(id_card: str):  # noqa D102
    year = int(id_card[6:10])
    month = int(id_card[10:12])
    day = int(id_card[12:14])

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

    def validate_result(self, pattern_text: str):  # noqa D102
        if self.check_code_check(pattern_text) and \
                self.birthday_check(pattern_text):
            return True
        return False

