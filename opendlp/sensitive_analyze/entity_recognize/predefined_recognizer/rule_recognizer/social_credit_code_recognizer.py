from typing import Optional, List
import json

from opendlp.sensitive_analyze.entity_recognize import Pattern, PatternRecognizer
from opendlp.sensitive_analyze.entity_recognize.conf import config


class SocialCreditCodeRecognizer(PatternRecognizer):
    """
    Recognize social credit code using regex.

    :param patterns: List of patterns to be used by this recognizer
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "SOCIAL_CREDIT_CODE",
            r"\b(((?=[^IOSVZ])[A-Z0-9]){2})([0-9]{6})(((?=[^IOSVZ])[A-Z0-9]){10})\b"
        )
    ]

    def __init__(
            self,
            patterns: Optional[List[Pattern]] = None,
            supported_entity: str = "SOCIAL_CREDIT_CODE",
    ):
        patterns = patterns if patterns else self.PATTERNS
        self.credit_code_elements = json.load(open(config.SOCIAL_CREDIT_CODE_FILE, 'r', encoding='utf-8'))

        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns
        )

    # 第一位登记管理部门代码校验
    def first_code_check(self, pattern_text):   # noqa D102
        first_code_list = list(self.credit_code_elements['登记管理部门代码'].values())
        if pattern_text[0] in first_code_list:
            return True
        return False

    # 第二位机构类别代码校验, 匹配第一位的登记管理部门
    def second_code_check(self, pattern_text):  # noqa D102
        second_code_dic = self.credit_code_elements['机构类别代码']
        reverse_first_code_dic = {v: k for k, v in self.credit_code_elements['登记管理部门代码'].items()}
        second_code_list = second_code_dic[reverse_first_code_dic[pattern_text[0]]]
        if pattern_text[1] in second_code_list:
            return True
        return False

    # 第17位校验码校验，参照https://www.cods.org.cn/c/2020-10-29/12582.html
    def first_checkcode_check(self, pattern_text: str):   # noqa D102
        # 每个位置上的字符对应的权重
        weights = [3, 7, 9, 10, 5, 8, 4, 2]
        sum_value = 0
        for i in range(8, 16):
            # '0'的ASCII是48， 'A'的ASCII是65
            sum_value += ((ord(pattern_text[i]) - 48) if ord(pattern_text[i]) < 65 else (
                    ord(pattern_text[i]) - 55)) * weights[i - 8]
        first_check_num = 11 - sum_value % 11
        if first_check_num == 10:
            first_check_num = 'X'
        elif first_check_num == 11:
            first_check_num = 0

        if str(first_check_num) == pattern_text[16]:
            return True
        return False

    # 第18位校验码校验，参照https://www.cods.org.cn/c/2020-10-29/12575.html
    def last_checkcode_check(self, pattern_text: str):  # noqa D102
        # 前17位每个字符对应的权重
        weights = [1, 3, 9, 27, 19, 26, 16, 17, 20, 29, 25, 13, 8, 24, 10, 30, 28]

        # 用list的index表示每个字符代表的数字大小
        charset = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B',
                   'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P',
                   'Q', 'R', 'T', 'U', 'W', 'X', 'Y']
        sum_value = 0
        for i in range(0, 17):
            sum_value += charset.index(pattern_text[i]) * weights[i]
        second_check_num = 31 - sum_value % 31
        if second_check_num == 31:
            second_check_num = 0
        second_check_num = charset[second_check_num]

        if str(second_check_num) == pattern_text[17]:
            return True
        return False

    def validate_result(self, pattern_text: str):  # noqa D102
        if self.first_code_check(pattern_text) and \
                self.second_code_check(pattern_text) and \
                self.first_checkcode_check(pattern_text) and \
                self.last_checkcode_check(pattern_text):
            return True
        return False
