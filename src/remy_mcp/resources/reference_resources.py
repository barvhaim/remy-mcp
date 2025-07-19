"""
Reference data resources
"""

import json
from ..models import (
    TENDER_TYPES,
    REGIONS,
    LAND_USES,
    TENDER_STATUSES,
    KOD_YESHUV_SETTLEMENTS,
)


def register_reference_resources(mcp):
    """Register reference data resources"""

    @mcp.resource("remy://tender-types")
    def get_tender_types_resource() -> str:
        """
        Get list of all available tender types as a resource

        Returns reference data for tender types with Hebrew and English names.
        Use the IDs for filtering in search functions.
        """
        tender_types = [t.model_dump() for t in TENDER_TYPES]
        return json.dumps({"tender_types": tender_types}, ensure_ascii=False, indent=2)

    @mcp.resource("remy://regions")
    def get_regions_resource() -> str:
        """
        Get list of all Israeli regions as a resource

        Returns reference data for regions with Hebrew and English names.
        Use for geographic filtering in search functions.
        """
        regions = [r.model_dump() for r in REGIONS]
        return json.dumps({"regions": regions}, ensure_ascii=False, indent=2)

    @mcp.resource("remy://land-uses")
    def get_land_uses_resource() -> str:
        """
        Get list of all land use categories as a resource

        Returns reference data for land use purposes with Hebrew and English names.
        Use for purpose-based filtering in search functions.
        """
        land_uses = [l.model_dump() for l in LAND_USES]
        return json.dumps({"land_uses": land_uses}, ensure_ascii=False, indent=2)

    @mcp.resource("remy://tender-statuses")
    def get_tender_statuses_resource() -> str:
        """
        Get list of all tender status types as a resource

        Returns reference data for tender statuses with Hebrew and English names.
        """
        tender_statuses = [s.model_dump() for s in TENDER_STATUSES]
        return json.dumps(
            {"tender_statuses": tender_statuses}, ensure_ascii=False, indent=2
        )

    @mcp.resource("remy://priority-populations")
    def get_priority_populations_resource() -> str:
        """
        Get list of all priority population codes as a resource

        Returns reference data for priority populations with Hebrew and English descriptions.
        Use these codes for filtering in search functions.
        """
        priority_populations = [
            {
                "id": 1,
                "name_hebrew": "אנשים עם מוגבלות",
                "name_english": "People with disabilities",
            },
            {
                "id": 2,
                "name_hebrew": "בני מקום - לא לשימוש",
                "name_english": "Locals - not for use",
            },
            {"id": 3, "name_hebrew": "חסרי דיור", "name_english": "Housing-deprived"},
            {
                "id": 4,
                "name_hebrew": "בני מיעוטים מומלצי כוחות הביטחון",
                "name_english": "Minorities recommended by security forces",
            },
            {
                "id": 6,
                "name_hebrew": "חיילי מילואים",
                "name_english": "Reserve soldiers",
            },
            {
                "id": 7,
                "name_hebrew": "חיילי מילואים לוחמים",
                "name_english": "Combat reserve soldiers",
            },
            {
                "id": 8,
                "name_hebrew": "חיילי מילואים לוחמים בני מקום תושבי היישוב",
                "name_english": "Combat reserves - local settlement residents",
            },
            {
                "id": 9,
                "name_hebrew": "חיילי מילואים פעילים בני מקום תושבי היישוב",
                "name_english": "Active reserves - local settlement residents",
            },
            {
                "id": 10,
                "name_hebrew": "חיילי מילואים לוחמים בני מקום תושבי המועצה",
                "name_english": "Combat reserves - local council residents",
            },
            {
                "id": 11,
                "name_hebrew": "חיילי מילואים לוחמים בני מקום",
                "name_english": "Combat reserves - locals",
            },
            {
                "id": 12,
                "name_hebrew": "חיילי מילואים פעילים בני מקום תושבי המועצה",
                "name_english": "Active reserves - local council residents",
            },
            {
                "id": 13,
                "name_hebrew": "חיילי מילואים פעילים בני מקום",
                "name_english": "Active reserves - locals",
            },
            {
                "id": 14,
                "name_hebrew": "בני מקום תושבי היישוב",
                "name_english": "Local settlement residents",
            },
            {
                "id": 15,
                "name_hebrew": "בני מקום תושבי המועצה",
                "name_english": "Local council residents",
            },
            {"id": 16, "name_hebrew": "בני מקום", "name_english": "Locals"},
        ]
        return json.dumps(
            {"priority_populations": priority_populations}, ensure_ascii=False, indent=2
        )

    @mcp.resource("remy://settlements")
    def get_settlements_resource() -> str:
        """
        Get complete list of all settlements with their Kod Yeshuv codes as a resource

        Returns a comprehensive list of all Israeli settlements with their official
        codes and Hebrew names for reference and local caching.
        """
        settlements = [
            {"kod_yeshuv": settlement.kod_yeshuv, "name_hebrew": settlement.name_hebrew}
            for settlement in KOD_YESHUV_SETTLEMENTS
        ]
        return json.dumps({"settlements": settlements}, ensure_ascii=False, indent=2)
