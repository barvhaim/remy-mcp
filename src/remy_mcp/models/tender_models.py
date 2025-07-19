"""
Core tender data models
"""

from datetime import datetime
from typing import Optional, List, Any, Dict
from pydantic import BaseModel, Field, ConfigDict


class TenderDocument(BaseModel):
    """Model for tender document information"""

    document_type: Optional[str] = Field(None, description="Type of document")
    title: Optional[str] = Field(None, description="Document title")
    update_date: Optional[datetime] = Field(None, description="Last update date")
    download_url: Optional[str] = Field(None, description="Download URL if available")


class TenderAnnouncement(BaseModel):
    """Model for tender announcements and updates"""

    announcement_type: Optional[str] = Field(None, description="Type of announcement")
    title: Optional[str] = Field(None, description="Announcement title")
    date: Optional[datetime] = Field(None, description="Publication date")
    content: Optional[str] = Field(None, description="Announcement content")


class TenderBasic(BaseModel):
    """Basic tender information from search results"""

    michraz_id: int = Field(..., description="Tender ID", alias="MichrazID")
    michraz_name: Optional[str] = Field(
        None, description="Tender name/number", alias="MichrazName"
    )
    kod_merchav: Optional[int] = Field(
        None, description="Area code", alias="KodMerchav"
    )
    status_michraz: Optional[int] = Field(
        None, description="Tender status code", alias="StatusMichraz"
    )
    kod_yeud_michraz: Optional[int] = Field(
        None, description="Purpose code", alias="KodYeudMichraz"
    )
    kod_yeshuv: Optional[int] = Field(
        None, description="Settlement code", alias="KodYeshuv"
    )
    kod_sug_michraz: Optional[int] = Field(
        None, description="Tender type code", alias="KodSugMichraz"
    )
    published_choveret: Optional[bool] = Field(
        None, description="Published booklet", alias="PublishedChoveret"
    )
    mekuvan: Optional[bool] = Field(None, description="Reserved", alias="Mekuvan")
    yechidot_diur: Optional[int] = Field(
        None, description="Housing units", alias="YechidotDiur"
    )
    shchuna: Optional[str] = Field(None, description="Neighborhood", alias="Shchuna")
    pirsum_date: Optional[datetime] = Field(
        None, description="Publication date", alias="PirsumDate"
    )
    pticha_date: Optional[datetime] = Field(
        None, description="Opening date", alias="PtichaDate"
    )
    sgira_date: Optional[datetime] = Field(
        None, description="Closing date", alias="SgiraDate"
    )
    vaada_date: Optional[datetime] = Field(
        None, description="Committee date", alias="VaadaDate"
    )
    choveret_update_date: Optional[datetime] = Field(
        None, description="Booklet update date", alias="ChoveretUpdateDate"
    )
    khal_yaad_rashi: Optional[float] = Field(
        None, description="Minimum bid amount", alias="KhalYaadRashi"
    )

    model_config = ConfigDict(populate_by_name=True)


class TenderDetails(TenderBasic):
    """Detailed tender information"""

    tokef_arvut: Optional[datetime] = Field(
        None, description="Guarantee validity", alias="TokefArvut"
    )
    tokef_arvut_sarvan: Optional[datetime] = Field(
        None, description="Root guarantee validity", alias="TokefArvutSarvan"
    )
    sum_arvut_sarvan: Optional[float] = Field(
        None, description="Root guarantee amount", alias="SumArvutSarvan"
    )
    schum_arvut: Optional[float] = Field(
        None, description="Guarantee amount", alias="SchumArvut"
    )
    divur: Optional[str] = Field(None, description="Remarks", alias="Divur")
    comments: Optional[str] = Field(
        None, description="Additional comments", alias="Comments"
    )
    michraz_doc_list: Optional[List[Dict[str, Any]]] = Field(
        None, description="Document list", alias="MichrazDocList"
    )
    michraz_full_document: Optional[Dict[str, Any]] = Field(
        None, description="Full document", alias="MichrazFullDocument"
    )
    tik: Optional[Dict[str, Any]] = Field(None, description="File details", alias="Tik")


class TenderResult(BaseModel):
    """Model for tender results"""

    michraz_id: int = Field(..., description="Tender ID", alias="MichrazID")
    matach_number: Optional[str] = Field(
        None, description="Matach number", alias="MatachNumber"
    )
    tochnit: Optional[str] = Field(None, description="Plan", alias="Tochnit")
    goral: Optional[str] = Field(None, description="Lot", alias="Goral")
    gush: Optional[str] = Field(None, description="Block", alias="Gush")
    chelka: Optional[str] = Field(None, description="Parcel", alias="Chelka")
    final_price: Optional[float] = Field(
        None, description="Final price in NIS", alias="FinalPrice"
    )
    development_costs: Optional[float] = Field(
        None, description="Development costs in NIS", alias="DevelopmentCosts"
    )
    yechidot_diur: Optional[int] = Field(
        None, description="Housing units", alias="YechidotDiur"
    )
    winner_name: Optional[str] = Field(
        None, description="Winner name", alias="WinnerName"
    )
    area: Optional[float] = Field(
        None, description="Area in square meters", alias="Area"
    )
    min_price: Optional[float] = Field(
        None, description="Minimum price in NIS", alias="MinPrice"
    )
    shuma_price: Optional[float] = Field(
        None, description="Appraisal price in NIS", alias="ShumaPrice"
    )

    model_config = ConfigDict(populate_by_name=True)


class SearchRequest(BaseModel):
    """Model for search request parameters"""

    tender_number: Optional[str] = None
    tender_types: Optional[List[int]] = None
    settlement: Optional[str] = None
    neighborhood: Optional[str] = None
    purpose: Optional[str] = None
    region: Optional[str] = None
    submission_date_from: Optional[datetime] = None
    submission_date_to: Optional[datetime] = None
    publication_date_from: Optional[datetime] = None
    publication_date_to: Optional[datetime] = None
    active_only: bool = False
    has_results: Optional[bool] = None
    sort_by: Optional[str] = None
    sort_order: Optional[str] = None
    page_size: int = 100
    page_number: int = 1


class SearchResponse(BaseModel):
    """Model for search response"""

    results: List[TenderBasic]
    total_count: Optional[int] = None
    page_number: int = 1
    page_size: int = 100
    has_more: bool = False


class TenderMapDetails(BaseModel):
    """Model for tender geographic/mapping data"""

    michraz_id: int = Field(..., description="Tender ID")
    coordinates: Optional[Dict[str, Any]] = Field(
        None, description="Geographic coordinates"
    )
    map_data: Optional[Dict[str, Any]] = Field(None, description="Additional map data")

    model_config = ConfigDict(populate_by_name=True)
