from typing import List, Optional
import tldextract
from opendlp.sensitive_analyze.entity_recognize import Pattern, PatternRecognizer


class EmailRecognizer(PatternRecognizer):
    """
    Recognize email addresses using regex.

    :param patterns: List of patterns to be used by this recognizer
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "EMAIL_ADDRESS",
            # presidio
            #r"\b((([!#$%&'*+\-/=?^_`{|}~\w])|([!#$%&'*+\-/=?^_`{|}~\w][!#$%&'*+\-/=?^_`{|}~\.\w]{0,}[!#$%&'*+\-/=?^_`{|}~\w]))[@]\w+([-.]\w+)*\.\w+([-.]\w+)*)\b",  # noqa: E501
            # from https://c.runoob.com/front-end/854/
            r"\b\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*\b",
        ),
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        supported_entity: str = "EMAIL_ADDRESS",
    ):
        patterns = patterns if patterns else self.PATTERNS
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns
        )
        self.no_fetch_extract = tldextract.TLDExtract(suffix_list_urls=None)

    def validate_result(self, pattern_text: str):  # noqa D102
        result = self.no_fetch_extract(pattern_text)
        return result.fqdn != ""
