"""
Israeli Land Authority API Client
Provides access to רמ״י (Israeli Land Authority) public tender data
"""

import time
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class IsraeliLandAPI:
    """Client for accessing Israeli Land Authority public tender data"""

    BASE_URL = "https://apps.land.gov.il/MichrazimSite/api"

    REQUIRED_HEADERS = {
        "User-Agent": "datagov-external-client",
        "Content-Type": "application/json",
        "Origin": "https://apps.land.gov.il",
        "Referer": "https://apps.land.gov.il/MichrazimSite/",
    }

    def __init__(self, rate_limit_delay: float = 1.0):
        """
        Initialize the API client

        Args:
            rate_limit_delay: Delay between requests in seconds
        """
        self.rate_limit_delay = rate_limit_delay
        self._last_request_time = 0.0

        # Configure session with retries
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        self.session.headers.update(self.REQUIRED_HEADERS)

    def _rate_limit(self):
        """Implement rate limiting between requests"""
        current_time = time.time()
        time_since_last = current_time - self._last_request_time
        if time_since_last < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last)
        self._last_request_time = time.time()

    def search_tenders(
        self,
        tender_number: Optional[str] = None,
        tender_types: Optional[List[int]] = None,
        settlement: Optional[str] = None,
        kod_yeshuv: Optional[int] = None,
        neighborhood: Optional[str] = None,
        purpose: Optional[str] = None,
        region: Optional[str] = None,
        submission_date_from: Optional[datetime] = None,
        submission_date_to: Optional[datetime] = None,
        publication_date_from: Optional[datetime] = None,
        publication_date_to: Optional[datetime] = None,
        committee_date_from: Optional[datetime] = None,
        committee_date_to: Optional[datetime] = None,
        tender_purposes: Optional[List[int]] = None,
        regions: Optional[List[int]] = None,
        tender_statuses: Optional[List[int]] = None,
        priority_populations: Optional[List[int]] = None,
        active_only: bool = False,
        quick_search: bool = False,
        has_results: Optional[bool] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = None,
        page_size: int = 100,
        page_number: int = 1,
    ) -> Dict[str, Any]:
        """
        Search for land tenders with enhanced filtering capabilities

        Args:
            tender_number: Specific tender number to search for (מספר מכרז)
            tender_types: List of tender type IDs to filter by (סוג המכרז)
            settlement: Settlement name to filter by (יישוב)
            kod_yeshuv: Settlement code (Kod Yeshuv) to filter by
            neighborhood: Neighborhood name to filter by (שכונה)
            purpose: Land use purpose to filter by (legacy)
            region: Region to filter by (legacy)
            submission_date_from: Start date for submission deadline filter
            submission_date_to: End date for submission deadline filter
            publication_date_from: Start date for publication filter
            publication_date_to: End date for publication filter
            committee_date_from: Start date for committee date filter (ועדת מכרזים)
            committee_date_to: End date for committee date filter (ועדת מכרזים)
            tender_purposes: List of tender purpose/designation IDs (ייעוד מכרז)
            regions: List of Rami region IDs (מרחב ברמ"י)
            tender_statuses: List of tender status IDs (סטטוס המכרז)
            priority_populations: List of priority population codes (אוכלוסיות עדיפות)
            active_only: Only return active tenders
            quick_search: Use quick search mode
            has_results: Filter by whether tender has results
            sort_by: Field to sort by
            sort_order: Sort order (asc/desc)
            page_size: Number of results per page (client-side pagination)
            page_number: Page number to retrieve (client-side pagination)

        Returns:
            Dictionary containing search results

        Note:
            The Israeli Land Authority API does not support server-side pagination.
            Pagination is implemented client-side by retrieving all results and
            then slicing them according to page_size and page_number parameters.
        """
        self._rate_limit()

        # Build request payload based on website form structure
        payload = {"ActiveQuickSearch": quick_search, "ActiveMichraz": active_only}

        # Basic search filters
        if tender_number:
            payload["MisMichraz"] = tender_number
        if tender_types:
            payload["SugMichraz"] = tender_types
        # Note: Settlement name is handled by frontend autocomplete, API expects KodYeshuv
        if kod_yeshuv:
            payload["KodYeshuv"] = kod_yeshuv
        elif settlement:
            # If settlement name provided but no kod_yeshuv, this may not work with API
            # Users should use kod_yeshuv or convert settlement name to code first
            payload["Yishuv"] = settlement
        if neighborhood:
            payload["Shchuna"] = neighborhood

        # Enhanced filtering options
        if tender_purposes:
            payload["YeudMichraz"] = tender_purposes
        if regions:
            payload["Merchav"] = regions
        if tender_statuses:
            payload["StatusMichraz"] = tender_statuses
        if priority_populations:
            payload["PriorityPopulations"] = priority_populations

        # Date range filters
        if submission_date_from or submission_date_to:
            payload["CloseDate"] = {}
            if submission_date_from:
                payload["CloseDate"]["from"] = submission_date_from.strftime("%d/%m/%y")
            if submission_date_to:
                payload["CloseDate"]["to"] = submission_date_to.strftime("%d/%m/%y")

        if committee_date_from or committee_date_to:
            payload["VaadaDate"] = {}
            if committee_date_from:
                payload["VaadaDate"]["from"] = committee_date_from.strftime("%d/%m/%y")
            if committee_date_to:
                payload["VaadaDate"]["to"] = committee_date_to.strftime("%d/%m/%y")

        if publication_date_from or publication_date_to:
            payload["PirsumDate"] = {}
            if publication_date_from:
                payload["PirsumDate"]["from"] = publication_date_from.strftime(
                    "%d/%m/%y"
                )
            if publication_date_to:
                payload["PirsumDate"]["to"] = publication_date_to.strftime("%d/%m/%y")

        # Legacy compatibility fallbacks
        if purpose and not tender_purposes:
            payload["purpose"] = purpose
        if region and not regions:
            payload["region"] = region

        # Additional search parameters
        if has_results is not None:
            payload["hasResults"] = has_results
        if sort_by:
            payload["sortBy"] = sort_by
        if sort_order:
            payload["sortOrder"] = sort_order

        # Note: The Israeli Land Authority API doesn't support server-side pagination
        # pageSize and pageNumber parameters are ignored by the API
        # We implement client-side pagination instead

        try:
            response = self.session.post(
                f"{self.BASE_URL}/SearchApi/Search", json=payload, timeout=30
            )
            response.raise_for_status()
            data = response.json()

            # Implement client-side pagination since API doesn't support it
            if isinstance(data, list):
                # Apply client-side pagination to the results
                start_idx = (page_number - 1) * page_size
                end_idx = start_idx + page_size
                return data[start_idx:end_idx]
            else:
                # If it's a dict with results key, paginate those
                if "results" in data:
                    start_idx = (page_number - 1) * page_size
                    end_idx = start_idx + page_size
                    data["results"] = data["results"][start_idx:end_idx]
                return data

        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to search tenders: {str(e)}")

    def get_tender_details(self, michraz_id: int) -> Dict[str, Any]:
        """
        Get detailed information for a specific tender

        Args:
            michraz_id: The tender ID to get details for

        Returns:
            Dictionary containing tender details
        """
        self._rate_limit()

        try:
            response = self.session.get(
                f"{self.BASE_URL}/MichrazDetailsApi/Get",
                params={"michrazID": michraz_id},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(
                f"Failed to get tender details for ID {michraz_id}: {str(e)}"
            )

    def get_tender_map_details(self, michraz_id: int) -> Dict[str, Any]:
        """
        Get geographic/mapping data for a tender

        Args:
            michraz_id: The tender ID to get map details for

        Returns:
            Dictionary containing map details
        """
        self._rate_limit()

        try:
            response = self.session.get(
                f"{self.BASE_URL}/MichrazDetailsApi/GetMichrazMapaDetails",
                params={"michrazID": michraz_id},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(
                f"Failed to get map details for tender ID {michraz_id}: {str(e)}"
            )

    def get_all_tenders(self) -> List[Dict[str, Any]]:
        """
        Get all available tenders (simplified search)

        Returns:
            List of all tenders
        """
        return self.search_tenders(active_only=False, page_size=10000)

    def get_active_tenders(self) -> List[Dict[str, Any]]:
        """
        Get only active tenders

        Returns:
            List of active tenders
        """
        return self.search_tenders(active_only=True, page_size=10000)

    def get_recent_results(self, days: int = 30) -> List[Dict[str, Any]]:
        """
        Get tenders with results from the last N days

        Args:
            days: Number of days to look back

        Returns:
            List of tenders with recent results
        """
        date_from = datetime.now() - timedelta(days=days)
        return self.search_tenders(
            has_results=True, submission_date_from=date_from, page_size=10000
        )

    def search_by_location(
        self,
        settlement_code: Optional[str] = None,
        region: Optional[str] = None,
        neighborhood: Optional[str] = None,
        purpose: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search tenders by location

        Args:
            settlement_code: Settlement code (Kod Yeshuv)
            region: Region name
            neighborhood: Neighborhood name
            purpose: Purpose of the tender (e.g., "מגרש לבניית בית קרקע")

        Returns:
            List of location-specific tenders
        """
        return self.search_tenders(
            kod_yeshuv=settlement_code,
            region=region,
            neighborhood=neighborhood,
            purpose=purpose,
            page_size=10000,
        )

    def search_by_type(
        self, tender_types: Optional[List[int]] = None, purpose: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search tenders by type or purpose

        Args:
            tender_types: List of tender type IDs
            purpose: Land use purpose

        Returns:
            List of type-specific tenders
        """
        return self.search_tenders(
            tender_types=tender_types, purpose=purpose, page_size=10000
        )
