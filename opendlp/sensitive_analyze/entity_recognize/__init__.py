"""Presidio analyzer package."""

import logging

from opendlp.sensitive_analyze.entity_recognize.pattern import Pattern
from opendlp.sensitive_analyze.entity_recognize.recognizer_result import RecognizerResult
from opendlp.sensitive_analyze.entity_recognize.entity_recognizer import EntityRecognizer
from opendlp.sensitive_analyze.entity_recognize.pattern_recognizer import PatternRecognizer
from opendlp.sensitive_analyze.entity_recognize.recognizer_registry import RecognizerRegistry
from opendlp.sensitive_analyze.entity_recognize.recognizer_engine import RecognizerEngine



# Define default loggers behavior

# 1. entity_analyzer logger

logging.getLogger("entity-analyzer").addHandler(logging.NullHandler())

ch = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s][%(name)s][%(levelname)s]%(message)s")
ch.setFormatter(formatter)

__all__ = [
    "Pattern",
    "RecognizerResult",
    "EntityRecognizer",
    "PatternRecognizer",
    "RecognizerRegistry",
    "RecognizerEngine"
]