"""
Settlement-related MCP tools
"""

from typing import Dict, Any

from ..models import KodYeshuvArgs, KOD_YESHUV_SETTLEMENTS


def register_settlement_tools(mcp, api_client):
    """Register settlement-related tools"""

    @mcp.tool()
    def get_kod_yeshuv(args: KodYeshuvArgs) -> Dict[str, Any]:
        """
        Get Kod Yeshuv (settlement code) from Hebrew settlement name

        Returns the official settlement code used by Israeli authorities for the given
        settlement name. Useful for integration with other Israeli government systems.
        """
        try:
            # Search for exact match first
            settlement_name = args.settlement_name.strip()

            for settlement in KOD_YESHUV_SETTLEMENTS:
                if settlement.name_hebrew == settlement_name:
                    return {
                        "success": True,
                        "settlement_name": settlement_name,
                        "kod_yeshuv": settlement.kod_yeshuv,
                        "match_type": "exact",
                    }

            # Search for partial matches if no exact match found
            partial_matches = []
            settlement_lower = settlement_name.lower()

            for settlement in KOD_YESHUV_SETTLEMENTS:
                name_lower = settlement.name_hebrew.lower()
                if settlement_lower in name_lower or name_lower in settlement_lower:
                    partial_matches.append(
                        {
                            "settlement_name": settlement.name_hebrew,
                            "kod_yeshuv": settlement.kod_yeshuv,
                            "similarity": "partial",
                        }
                    )

            if partial_matches:
                return {
                    "success": True,
                    "searched_name": settlement_name,
                    "exact_match": False,
                    "partial_matches": partial_matches[:10],  # Limit to top 10 matches
                    "match_type": "partial",
                }

            # No matches found
            return {
                "success": False,
                "error": f"No settlement found matching '{settlement_name}'",
                "searched_name": settlement_name,
                "suggestion": "Try using the exact Hebrew name or check the settlement name spelling",
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "searched_name": args.settlement_name,
            }
