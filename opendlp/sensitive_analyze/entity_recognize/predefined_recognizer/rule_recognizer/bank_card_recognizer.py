from typing import List, Optional
from opendlp.sensitive_analyze.entity_recognize import Pattern, PatternRecognizer


class BankCardRecognizer(PatternRecognizer):
    """
    Recognize postcode using regex.

    :param patterns: List of patterns to be used by this recognizer
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "BANK_CARD",
            r"\b([1-9]{1})(\d{12,18})\b"  # 国内银行卡长度13-19位（ISO标准）
        ),
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        supported_entity: str = "BANK_CARD",
    ):
        patterns = patterns if patterns else self.PATTERNS

        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns
        )

    def validate_result(self, pattern_text: str):
        sum_odd = sum_even = 0
        count = 0
        for bank_card_value in pattern_text[:-1][::-1]:
            if (count % 2) == 0:
                if int(bank_card_value) * 2 > 9:
                    sum_even += (int(bank_card_value) * 2 - 9)
                else:
                    sum_even += int(bank_card_value) * 2
            else:
                sum_odd += int(bank_card_value)
            count = count + 1
        if (sum_even + sum_odd) % 10 != 0:
            check_code = 10 - (sum_even + sum_odd) % 10
        else:
            check_code = 0

        if str(check_code) == pattern_text[-1]:
            return True
        else:
            return False

