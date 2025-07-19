"""
Argument models for MCP tools
"""

from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel, Field


class DateRange(BaseModel):
    """Date range model for search parameters"""

    from_date: Optional[str] = Field(None, description="Start date (dd/mm/yy format)")
    to_date: Optional[str] = Field(None, description="End date (dd/mm/yy format)")


class SearchTendersArgs(BaseModel):
    """Arguments for search_tenders tool"""

    # Basic search parameters
    tender_number: Optional[str] = Field(
        None, description="Specific tender number to search for (מספר מכרז)"
    )
    tender_types: Optional[List[int]] = Field(
        None, description="List of tender type IDs (סוג המכרז)"
    )
    settlement: Optional[str] = Field(
        None, description="Settlement name in Hebrew (יישוב)"
    )
    kod_yeshuv: Optional[int] = Field(None, description="Settlement code (Kod Yeshuv)")
    neighborhood: Optional[str] = Field(
        None, description="Neighborhood name in Hebrew (שכונה)"
    )
    tender_purposes: Optional[List[int]] = Field(
        None, description="List of tender purpose/designation IDs (ייעוד מכרז)"
    )
    regions: Optional[List[int]] = Field(
        None, description='List of Rami region IDs (מרחב ברמ"י)'
    )
    tender_statuses: Optional[List[int]] = Field(
        None, description="List of tender status IDs (סטטוס המכרז)"
    )

    # Date range filters
    submission_deadline: Optional[DateRange] = Field(
        None, description="Submission deadline date range (מועד אחרון להגשת הצעות)"
    )
    committee_date: Optional[DateRange] = Field(
        None, description="Committee date range (ועדת מכרזים)"
    )
    publication_date: Optional[DateRange] = Field(
        None, description="Publication date range (פרסום מכרז)"
    )

    # Priority populations
    priority_populations: Optional[List[int]] = Field(
        None, description="Priority population codes (אוכלוסיות עדיפות)"
    )

    # Search mode and result controls
    active_only: bool = Field(False, description="Only return active tenders")
    quick_search: bool = Field(False, description="Use quick search mode")
    max_results: int = Field(100, description="Maximum number of results to return")

    # Legacy compatibility (deprecated)
    purpose: Optional[str] = Field(
        None,
        description="Legacy: Land use purpose (use tender_purposes instead)",
        deprecated=True,
    )
    region: Optional[str] = Field(
        None, description="Legacy: Region name (use regions instead)", deprecated=True
    )
    days_back: Optional[int] = Field(
        None,
        description="Legacy: Search tenders from last N days (use date ranges instead)",
        deprecated=True,
    )


class TenderDetailsArgs(BaseModel):
    """Arguments for tender details tools"""

    michraz_id: int = Field(..., description="The tender ID to get details for")


class LocationSearchArgs(BaseModel):
    """Arguments for location-based search"""

    settlement: Optional[str] = Field(None, description="Settlement name in Hebrew")
    region: Optional[str] = Field(None, description="Region name")
    neighborhood: Optional[str] = Field(None, description="Neighborhood name in Hebrew")
    active_only: bool = Field(False, description="Only return active tenders")


class TypeSearchArgs(BaseModel):
    """Arguments for type-based search"""

    tender_types: Optional[List[int]] = Field(
        None, description="List of tender type IDs (1-9)"
    )
    purpose: Optional[str] = Field(None, description="Land use purpose")
    active_only: bool = Field(False, description="Only return active tenders")


class RecentResultsArgs(BaseModel):
    """Arguments for recent results query"""

    days: int = Field(30, description="Number of days to look back for results")


class KodYeshuvArgs(BaseModel):
    """Arguments for settlement code lookup"""

    settlement_name: str = Field(
        ..., description="Settlement name in Hebrew to get the Kod Yeshuv for"
    )
