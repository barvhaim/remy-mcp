"""
Tender-related MCP tools
"""

from datetime import datetime, timedelta
from typing import Dict, Any

from ..models import (
    SearchTendersArgs,
    TenderDetailsArgs,
    TypeSearchArgs,
    RecentResultsArgs,
    KOD_YESHUV_SETTLEMENTS,
)


def register_tender_tools(mcp, api_client):
    """Register tender-related tools"""

    @mcp.tool()
    def search_tenders(args: SearchTendersArgs) -> Dict[str, Any]:
        """
        Search for land tenders from the Israeli Land Authority

        Enhanced search with comprehensive filtering options including tender types, locations,
        statuses, date ranges, and priority populations. Supports Hebrew text and backward compatibility.
        """
        try:
            # Handle date range conversion
            submission_date_from = None
            submission_date_to = None
            publication_date_from = None
            publication_date_to = None

            # New date range format
            if args.submission_deadline:
                if args.submission_deadline.from_date:
                    submission_date_from = datetime.strptime(
                        args.submission_deadline.from_date, "%d/%m/%y"
                    )
                if args.submission_deadline.to_date:
                    submission_date_to = datetime.strptime(
                        args.submission_deadline.to_date, "%d/%m/%y"
                    )

            if args.publication_date:
                if args.publication_date.from_date:
                    publication_date_from = datetime.strptime(
                        args.publication_date.from_date, "%d/%m/%y"
                    )
                if args.publication_date.to_date:
                    publication_date_to = datetime.strptime(
                        args.publication_date.to_date, "%d/%m/%y"
                    )

            # Legacy compatibility for days_back
            if args.days_back and not submission_date_from:
                submission_date_from = datetime.now() - timedelta(days=args.days_back)

            # Handle legacy parameters
            legacy_purpose = args.purpose
            legacy_region = args.region

            # Handle settlement name to kod_yeshuv conversion
            final_kod_yeshuv = args.kod_yeshuv
            if args.settlement and not args.kod_yeshuv:
                # Try to convert settlement name to kod_yeshuv
                for settlement in KOD_YESHUV_SETTLEMENTS:
                    if settlement.name_hebrew == args.settlement.strip():
                        final_kod_yeshuv = settlement.kod_yeshuv
                        break

            # Handle committee date ranges
            committee_date_from = None
            committee_date_to = None
            if args.committee_date:
                if args.committee_date.from_date:
                    committee_date_from = datetime.strptime(
                        args.committee_date.from_date, "%d/%m/%y"
                    )
                if args.committee_date.to_date:
                    committee_date_to = datetime.strptime(
                        args.committee_date.to_date, "%d/%m/%y"
                    )

            # Call API with enhanced parameters
            results = api_client.search_tenders(
                tender_number=args.tender_number,
                tender_types=args.tender_types,
                settlement=(
                    args.settlement if not final_kod_yeshuv else None
                ),  # Only pass if no kod_yeshuv
                kod_yeshuv=final_kod_yeshuv,
                neighborhood=args.neighborhood,
                purpose=legacy_purpose,  # Legacy support
                region=legacy_region,  # Legacy support
                submission_date_from=submission_date_from,
                submission_date_to=submission_date_to,
                publication_date_from=publication_date_from,
                publication_date_to=publication_date_to,
                committee_date_from=committee_date_from,
                committee_date_to=committee_date_to,
                tender_purposes=args.tender_purposes,
                regions=args.regions,
                tender_statuses=args.tender_statuses,
                priority_populations=args.priority_populations,
                active_only=args.active_only,
                quick_search=args.quick_search,
                page_size=min(args.max_results, 1000),
            )

            # Process results
            if isinstance(results, list):
                tender_list = results[: args.max_results]
            else:
                tender_list = results.get("results", results)[: args.max_results]

            # Prepare search summary
            search_summary = {
                "parameters_used": args.model_dump(exclude_unset=True),
                "new_features": {
                    "enhanced_date_ranges": bool(
                        args.submission_deadline or args.publication_date
                    ),
                    "priority_populations": bool(args.priority_populations),
                    "multiple_statuses": bool(args.tender_statuses),
                    "multiple_purposes": bool(args.tender_purposes),
                    "multiple_regions": bool(args.regions),
                },
                "settlement_conversion": {
                    "settlement_name_provided": bool(args.settlement),
                    "kod_yeshuv_resolved": (
                        final_kod_yeshuv
                        if args.settlement and not args.kod_yeshuv
                        else None
                    ),
                    "conversion_successful": bool(
                        args.settlement and not args.kod_yeshuv and final_kod_yeshuv
                    ),
                },
            }

            return {
                "success": True,
                "count": len(tender_list),
                "tenders": tender_list,
                "search_summary": search_summary,
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "search_parameters": args.model_dump(exclude_unset=True),
            }

    @mcp.tool()
    def get_tender_details(args: TenderDetailsArgs) -> Dict[str, Any]:
        """
        Get comprehensive details for a specific tender by ID

        Returns detailed information including dates, guarantees, documents,
        and administrative details for the specified tender.
        """
        try:
            details = api_client.get_tender_details(args.michraz_id)
            return {"success": True, "tender_id": args.michraz_id, "details": details}
        except Exception as e:
            return {"success": False, "error": str(e), "tender_id": args.michraz_id}

    @mcp.tool()
    def get_active_tenders(max_results: int = 100) -> Dict[str, Any]:
        """
        Get all currently active land tenders

        Returns a list of tenders that are currently open for submissions,
        useful for finding current bidding opportunities.
        """
        try:
            results = api_client.get_active_tenders()

            if isinstance(results, list):
                tender_list = results[:max_results]
            else:
                tender_list = results.get("results", results)[:max_results]

            return {
                "success": True,
                "count": len(tender_list),
                "active_tenders": tender_list,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @mcp.tool()
    def search_by_type(args: TypeSearchArgs) -> Dict[str, Any]:
        """
        Search tenders by type or land use purpose

        Find tenders of specific types (residential, commercial, etc.) or
        purposes (low-rise construction, offices, etc.).
        """
        try:
            results = api_client.search_by_type(
                tender_types=args.tender_types, purpose=args.purpose
            )

            if isinstance(results, list):
                tender_list = results
            else:
                tender_list = results.get("results", results)

            return {
                "success": True,
                "count": len(tender_list),
                "tenders": tender_list,
                "type_search": {
                    "tender_types": args.tender_types,
                    "purpose": args.purpose,
                },
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "type_search": {
                    "tender_types": args.tender_types,
                    "purpose": args.purpose,
                },
            }

    @mcp.tool()
    def get_recent_results(args: RecentResultsArgs) -> Dict[str, Any]:
        """
        Get tenders with results from recent days

        Find completed tenders with published results for market analysis
        and trend monitoring.
        """
        try:
            results = api_client.get_recent_results(days=args.days)

            if isinstance(results, list):
                tender_list = results
            else:
                tender_list = results.get("results", results)

            return {
                "success": True,
                "count": len(tender_list),
                "days_back": args.days,
                "recent_results": tender_list,
            }
        except Exception as e:
            return {"success": False, "error": str(e), "days_back": args.days}

    @mcp.tool()
    def get_tender_map_details(args: TenderDetailsArgs) -> Dict[str, Any]:
        """
        Get geographic and mapping data for a specific tender

        Returns location coordinates and map integration data for the specified tender.
        """
        try:
            map_details = api_client.get_tender_map_details(args.michraz_id)
            return {
                "success": True,
                "tender_id": args.michraz_id,
                "map_details": map_details,
            }
        except Exception as e:
            return {"success": False, "error": str(e), "tender_id": args.michraz_id}
