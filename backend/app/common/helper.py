from typing import List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class HelperFunctions:
    @staticmethod
    def is_number(value):
        return isinstance(value, (int, float)) and not isinstance(value, bool)
