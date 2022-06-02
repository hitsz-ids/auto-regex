"""Predefined recognizers package. Holds all the default recognizers."""

from opendlp.sensitive_analyze.entity_recognize.predefined_recognizer.rule_recognizer.bank_card_recognizer import BankCardRecognizer
from opendlp.sensitive_analyze.entity_recognize.predefined_recognizer.rule_recognizer.date_recognizer import DateRecognizer
from opendlp.sensitive_analyze.entity_recognize.predefined_recognizer.rule_recognizer.domain_recognizer import DomainRecognizer
from opendlp.sensitive_analyze.entity_recognize.predefined_recognizer.rule_recognizer.email_recognizer import EmailRecognizer
from opendlp.sensitive_analyze.entity_recognize.predefined_recognizer.rule_recognizer.idcard_recognizer import IDCardRecognizer
from opendlp.sensitive_analyze.entity_recognize.predefined_recognizer.rule_recognizer.ipv4_recognizer import Ipv4Recognizer
from opendlp.sensitive_analyze.entity_recognize.predefined_recognizer.rule_recognizer.ipv6_recognizer import Ipv6Recognizer
from opendlp.sensitive_analyze.entity_recognize.predefined_recognizer.rule_recognizer.license_plate_recognizer import LicensePlateRecognizer
from opendlp.sensitive_analyze.entity_recognize.predefined_recognizer.rule_recognizer.mac_recognizer import MacRecognizer
from opendlp.sensitive_analyze.entity_recognize.predefined_recognizer.rule_recognizer.mobile_phone_recognizer import MobilePhoneRecognizer
from opendlp.sensitive_analyze.entity_recognize.predefined_recognizer.rule_recognizer.passport_recognizer import PassportRecognizer
from opendlp.sensitive_analyze.entity_recognize.predefined_recognizer.rule_recognizer.postcode_recognizer import PostcodeRecognizer
from opendlp.sensitive_analyze.entity_recognize.predefined_recognizer.rule_recognizer.social_credit_code_recognizer import SocialCreditCodeRecognizer
from opendlp.sensitive_analyze.entity_recognize.predefined_recognizer.rule_recognizer.telephone_recognizer import TelephoneRecognizer
from opendlp.sensitive_analyze.entity_recognize.predefined_recognizer.nlp_recognizer.nlp_recognizer import NLPRecognizer


__all__ = [
    "BankCardRecognizer",
    "DateRecognizer",
    "DomainRecognizer",
    "EmailRecognizer",
    "IDCardRecognizer",
    "Ipv4Recognizer",
    "Ipv6Recognizer",
    "LicensePlateRecognizer",
    "MacRecognizer",
    "MobilePhoneRecognizer",
    "PassportRecognizer",
    "PostcodeRecognizer",
    "SocialCreditCodeRecognizer",
    "TelephoneRecognizer",
    "NLPRecognizer"
]