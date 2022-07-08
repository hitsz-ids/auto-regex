from typing import List
import json

from opendlp.sensitive_analyze.entity_recognize.conf import config
from opendlp.sensitive_analyze.entity_recognize.pattern import Pattern
from opendlp.sensitive_analyze.entity_recognize.userdefined_recognizer import UDFRecognizer
from opendlp.sensitive_analyze.entity_recognize.predefined_recognizer import (
    BankCardRecognizer,
    DateRecognizer,
    DomainRecognizer,
    EmailRecognizer,
    IDCardRecognizer,
    Ipv4Recognizer,
    Ipv6Recognizer,
    LicensePlateRecognizer,
    MacRecognizer,
    MobilePhoneRecognizer,
    PassportRecognizer,
    PostcodeRecognizer,
    SocialCreditCodeRecognizer,
    TelephoneRecognizer,
    NLPRecognizer
)


class RecognizerRegistry:
    def __init__(self, pattern_file):
        self.recognizers = {}
        self.predefined_recognizers_map = {
            config.PERSON: NLPRecognizer,
            config.COMPANY_NAME: NLPRecognizer,
            config.LOCATION: NLPRecognizer,

            config.ID_CARD: IDCardRecognizer,
            config.TELEPHONE: TelephoneRecognizer,
            config.MOBILE_PHONE: MobilePhoneRecognizer,
            config.EMAIL: EmailRecognizer,
            config.LICENSE_PLATE: LicensePlateRecognizer,
            config.BANK_CARD: BankCardRecognizer,
            config.PASSPORT: PassportRecognizer,
            config.SOCIAL_CREDIT_CODE: SocialCreditCodeRecognizer,
            config.POSTCODE: PostcodeRecognizer,
            config.DATE: DateRecognizer,
            config.IPV4: Ipv4Recognizer,
            config.IPV6: Ipv6Recognizer,
            config.MAC: MacRecognizer,
            config.DOMAIN_NAME: DomainRecognizer
        }

        self.pattern_file = pattern_file
        self.user_defined_recognizer = []

    def load_predefined_recognizers(self, entities: List[str]):
        recognizers = []
        for entity in entities:
            if entity in (config.PERSON, config.LOCATION, config.COMPANY_NAME):
                entity = config.PERSON
            recognizer = self.recognizers.get(entity, None)
            if recognizer is None:
                recognizer = self.predefined_recognizers_map.get(entity)()
                self.recognizers[entity] = recognizer
            recognizers.append(recognizer)

        return recognizers

    def load_user_defined_recognizers(self):
        if not self.user_defined_recognizer:
            pattern_dict = json.load(open(self.pattern_file, 'r', encoding='utf-8'))
            for entity, regexes in pattern_dict.items():
                patterns = []
                for regex in regexes:
                    # json中的字符是转义过的，不然json会报错
                    patterns.append(Pattern(name=entity, regex=regex))
                recognizer = UDFRecognizer(supported_entity=entity,
                                           patterns=patterns)
                self.user_defined_recognizer.append(recognizer)

        return self.user_defined_recognizer
