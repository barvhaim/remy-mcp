"""
Reference data models for Israeli Land Authority
"""

from pydantic import BaseModel, Field
from typing import Optional
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../../.."))
from data.kod_yeshuv import KOD_YESHUV_MAPPING


class TenderType(BaseModel):
    """Model for tender type reference data"""

    id: int
    name_hebrew: str
    name_english: str
    description: Optional[str] = None


class Region(BaseModel):
    """Model for region reference data"""

    id: int
    name_hebrew: str
    name_english: str
    code: Optional[str] = None


class LandUse(BaseModel):
    """Model for land use type reference data"""

    id: int
    name_hebrew: str
    name_english: str
    description: Optional[str] = None


class TenderStatus(BaseModel):
    """Model for tender status reference data"""

    id: int
    name_hebrew: str
    name_english: str
    description: Optional[str] = None


class Settlement(BaseModel):
    """Model for settlement (yeshuv) reference data"""

    kod_yeshuv: int = Field(..., description="Settlement code")
    name_hebrew: str = Field(..., description="Settlement name in Hebrew")


# Predefined reference data based on documentation
TENDER_TYPES = [
    TenderType(
        id=1, name_hebrew="מכרז פומבי רגיל", name_english="Regular Public Tender"
    ),
    TenderType(id=2, name_hebrew="מחיר מטרה", name_english="Target Price"),
    TenderType(
        id=3, name_hebrew="דיור במחיר מופחת", name_english="Reduced Price Housing"
    ),
    TenderType(id=4, name_hebrew="מכרז ייזום", name_english="Initiative Tender"),
    TenderType(
        id=5,
        name_hebrew="מכרז למגרש בלתי מסוים",
        name_english="Unspecified Plot Tender",
    ),
    TenderType(
        id=6, name_hebrew="הרשמה והגרלה", name_english="Registration and Lottery"
    ),
    TenderType(id=7, name_hebrew="דיור להשכרה", name_english="Rental Housing"),
    TenderType(id=8, name_hebrew="מכרזי עמידר", name_english="Amidar Tenders"),
    TenderType(
        id=9,
        name_hebrew="מכרזי החברה לפיתוח עכו",
        name_english="Acre Development Company Tenders",
    ),
]

REGIONS = [
    Region(id=1, name_hebrew='יו"ש', name_english="Judea and Samaria"),
    Region(id=2, name_hebrew="דרום", name_english="South"),
    Region(id=3, name_hebrew="חיפה", name_english="Haifa"),
    Region(id=4, name_hebrew="תל אביב", name_english="Tel Aviv"),
    Region(id=5, name_hebrew="ירושלים", name_english="Jerusalem"),
    Region(id=6, name_hebrew="מרכז", name_english="Center"),
]

LAND_USES = [
    LandUse(
        id=1,
        name_hebrew="בנייה נמוכה/צמודת קרקע",
        name_english="Low-rise/Ground-attached Construction",
    ),
    LandUse(id=2, name_hebrew="בנייה רוויה", name_english="High-density Construction"),
    LandUse(
        id=3, name_hebrew="מסחר ו/או משרדים", name_english="Commerce and/or Offices"
    ),
    LandUse(id=4, name_hebrew="מלונאות", name_english="Hotels"),
    LandUse(
        id=5,
        name_hebrew="מוסדות ו/או בניינים ציבוריים",
        name_english="Institutions and/or Public Buildings",
    ),
    LandUse(
        id=6,
        name_hebrew="ספורט ו/או נופש ו/או תיירות ו/או מלונאות",
        name_english="Sports/Recreation/Tourism/Hotels",
    ),
    LandUse(
        id=7,
        name_hebrew="מגורים ו/או מסחר ו/או מלונאות ו/או נופש",
        name_english="Residential/Commercial/Hotels/Recreation",
    ),
    LandUse(id=8, name_hebrew="כרייה וחציבה", name_english="Mining and Quarrying"),
    LandUse(id=9, name_hebrew="אחר", name_english="Other"),
]

TENDER_STATUSES = [
    TenderStatus(id=1, name_hebrew="מפורסם", name_english="Published"),
    TenderStatus(id=2, name_hebrew="בוטל", name_english="Cancelled"),
    TenderStatus(
        id=3, name_hebrew="טרם הוכרזו זוכים", name_english="Winners Not Yet Announced"
    ),
]

# Kod Yeshuv settlement mapping data
KOD_YESHUV_SETTLEMENTS = [
    Settlement(kod_yeshuv=kod, name_hebrew=name)
    for kod, name in KOD_YESHUV_MAPPING.items()
]
