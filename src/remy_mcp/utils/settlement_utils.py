"""
Utility functions for settlement handling
"""

from typing import Optional
from ..models import KOD_YESHUV_SETTLEMENTS


def convert_settlement_name_to_code(settlement_name: str) -> Optional[int]:
    """
    Convert Hebrew settlement name to Kod Yeshuv code

    Args:
        settlement_name: Settlement name in Hebrew

    Returns:
        Kod Yeshuv code if found, None otherwise
    """
    settlement_name = settlement_name.strip()

    for settlement in KOD_YESHUV_SETTLEMENTS:
        if settlement.name_hebrew == settlement_name:
            return settlement.kod_yeshuv

    return None
