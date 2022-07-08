"""Presidio analyzer package."""

import logging

from opendlp.entity_analyzer.pattern import Pattern
from opendlp.entity_analyzer.recognizer_result import RecognizerResult
from opendlp.entity_analyzer.entity_recognizer import EntityRecognizer
from opendlp.entity_analyzer.pattern_recognizer import PatternRecognizer
from opendlp.entity_analyzer.recognizer_registry import RecognizerRegistry
from opendlp.entity_analyzer.recognizer_engine import RecognizerEngine



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