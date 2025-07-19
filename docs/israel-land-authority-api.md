# Israel Land Authority API Documentation

## Base URL

```
https://apps.land.gov.il/MichrazimSite/api
```

## Authentication

The API requires a specific User-Agent header:

```
User-Agent: datagov-external-client
```

## Endpoints

### Search Tenders

Retrieves all land tenders data.

**Endpoint:** `/SearchApi/Search`  
**Method:** `POST`  
**Headers:**

```
Content-Type: application/json
User-Agent: datagov-external-client
Origin: https://apps.land.gov.il
Referer: https://apps.land.gov.il/MichrazimSite/
```

**Request Body Parameters:**

Based on the website's search form, the following parameters are supported:

```json
{
  "ActiveQuickSearch": false,  // Boolean - Quick search mode
  "ActiveMichraz": null,       // Boolean - Active tenders only
  "MisMichraz": "",           // String - Tender number (מספר מכרז)
  "SugMichraz": [],           // Array[int] - Tender types (סוג המכרז)
  "KodYeshuv": null,          // Int - Settlement code (preferred - API expects this)
  "Yishuv": "",               // String - Settlement name (frontend autocomplete only)
  "Shchuna": "",              // String - Neighborhood (שכונה)
  "YeudMichraz": [],          // Array[int] - Tender purpose/designation (ייעוד מכרז)
  "Merchav": [],              // Array[int] - Rami regions (מרחב ברמ"י)
  "StatusMichraz": [],        // Array[int] - Tender status (סטטוס המכרז)
  "CloseDate": {              // Submission deadline range (מועד אחרון להגשת הצעות)
    "from": "",               // String - Date format: dd/mm/yy
    "to": ""                  // String - Date format: dd/mm/yy
  },
  "VaadaDate": {              // Committee date range (ועדת מכרזים)
    "from": "",               // String - Date format: dd/mm/yy
    "to": ""                  // String - Date format: dd/mm/yy
  },
  "PirsumDate": {             // Publication date range (פרסום מכרז)
    "from": "",               // String - Date format: dd/mm/yy
    "to": ""                  // String - Date format: dd/mm/yy
  },
  "PriorityPopulations": []   // Array[int] - Priority populations (אוכלוסיות עדיפות)
}
```

**Priority Population Codes:**
- `1`: אנשים עם מוגבלות (People with disabilities)
- `2`: בני מקום - לא לשימוש (Locals - not for use)
- `3`: חסרי דיור (Housing-deprived)
- `4`: בני מיעוטים מומלצי כוחות הביטחון (Minorities recommended by security forces)
- `6`: חיילי מילואים (Reserve soldiers)
- `7`: חיילי מילואים לוחמים (Combat reserve soldiers)
- `8`: חיילי מילואים לוחמים בני מקום תושבי היישוב (Combat reserves - local settlement residents)
- `9`: חיילי מילואים פעילים בני מקום תושבי היישוב (Active reserves - local settlement residents)
- `10`: חיילי מילואים לוחמים בני מקום תושבי המועצה (Combat reserves - local council residents)
- `11`: חיילי מילואים לוחמים בני מקום (Combat reserves - locals)
- `12`: חיילי מילואים פעילים בני מקום תושבי המועצה (Active reserves - local council residents)
- `13`: חיילי מילואים פעילים בני מקום (Active reserves - locals)
- `14`: בני מקום תושבי היישוב (Local settlement residents)
- `15`: בני מקום תושבי המועצה (Local council residents)
- `16`: בני מקום (Locals)

**Important Notes:**
- The API expects `KodYeshuv` (settlement code) rather than settlement name strings
- The website's settlement field uses autocomplete that converts names to codes on the frontend
- When using settlement names, convert them to `KodYeshuv` codes first using the settlements reference data
- The MCP server automatically attempts this conversion when possible

**Response:**
Array of tender objects, each containing:

```json
{
  "MichrazID": 20000001, // Tender ID
  "MichrazName": "1/2000", // Tender Name/Number
  "KodMerchav": 5, // Area Code
  "StatusMichraz": 5, // Tender Status
  "KodYeudMichraz": 3, // Tender Purpose Code
  "KodYeshuv": 5000, // Settlement Code
  "KodSugMichraz": 1, // Tender Type Code
  "PublishedChoveret": false, // Published Booklet
  "Mekuvan": false, // Reserved
  "YechidotDiur": 0, // Housing Units
  "Shchuna": " משתלה", // Neighborhood
  "PirsumDate": null, // Publication Date
  "PtichaDate": "2000-06-01T00:00:00+03:00", // Opening Date
  "SgiraDate": "2000-07-02T12:00:00+03:00", // Closing Date
  "VaadaDate": "2000-07-04T00:00:00+03:00", // Committee Date
  "ChoveretUpdateDate": null, // Booklet Update Date
  "KhalYaadRashi": null // Minimum Bid Amount
}
```

## Status Codes

- `200 OK`: Request successful
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Missing or invalid User-Agent
- `403 Forbidden`: Access denied
- `500 Internal Server Error`: Server error

## Rate Limiting

The API may have rate limiting in place. It's recommended to:

- Add appropriate delays between requests
- Handle rate limit responses gracefully
- Cache responses when possible

## Notes

- All dates are in ISO 8601 format with timezone (UTC+3)
- Hebrew text is returned in UTF-8 encoding
- The API returns a maximum of 10,000 results per request
- Some fields may be null depending on the tender status

## Example Usage

```python
import requests

headers = {
    'User-Agent': 'datagov-external-client',
    'Content-Type': 'application/json',
    'Origin': 'https://apps.land.gov.il',
    'Referer': 'https://apps.land.gov.il/MichrazimSite/'
}

payload = {
    "ActiveQuickSearch": False,
    "ActiveMichraz": None
}

response = requests.post(
    'https://apps.land.gov.il/MichrazimSite/api/SearchApi/Search',
    headers=headers,
    json=payload
)

tenders = response.json()
```

## API Endpoints

### 1. Search API

- **Endpoint**: `https://apps.land.gov.il/MichrazimSite/api/SearchApi/Search`
- **Method**: POST
- **Description**: Search for land tenders, results, and proposals
- **Headers**:
    - User-Agent: datagov-external-client
    - Content-Type: application/json
- **Payload**:
  ```json
  {
    "ActiveQuickSearch": false,
    "ActiveMichraz": null
  }
  ```

### 2. Tender Details API

- **Endpoint**: `https://apps.land.gov.il/MichrazimSite/api/MichrazDetailsApi/Get`
- **Method**: GET
- **Description**: Get detailed information about a specific land tender
- **Headers**:
    - User-Agent: datagov-external-client
    - Content-Type: application/json
- **Parameters**:
    - `michrazID` (query parameter): The ID of the tender to get details for
- **Example Request**:
  ```
  GET https://apps.land.gov.il/MichrazimSite/api/MichrazDetailsApi/Get?michrazID=20250001
  ```
- **Response Fields**:
    - `MichrazID`: Tender ID
    - `MichrazName`: Tender name/number
    - `KodMerchav`: Regional code
    - `StatusMichraz`: Tender status
    - `KodYeudMichraz`: Purpose code
    - `KodYeshuv`: Settlement code
    - `YechidotDiur`: Housing units
    - `Shchuna`: Neighborhood
    - `PirsumDate`: Publication date
    - `PtichaDate`: Opening date
    - `SgiraDate`: Submission deadline
    - `VaadaDate`: Committee date
    - `TokefArvut`: Guarantee validity
    - `TokefArvutSarvan`: Root guarantee validity
    - `SumArvutSarvan`: Root guarantee amount
    - `SchumArvut`: Guarantee amount
    - `Divur`: Remarks
    - `Comments`: Additional comments
    - `MichrazDocList`: List of tender documents
    - `MichrazFullDocument`: Full tender document
    - `Tik`: Tender file details

## Usage Examples

### Python Code Examples

1. Get All Land Tenders:

```python
from src.scrapers.api_scraper import ApiScraper

scraper = ApiScraper()
tenders = scraper.get_all_land_tenders()
```

2. Get Land Tender Results:

```python
from src.scrapers.api_scraper import ApiScraper

scraper = ApiScraper()
results = scraper.get_land_tender_results()
```

3. Get Tender Details:

```python
from src.scrapers.api_scraper import ApiScraper

scraper = ApiScraper()
details = scraper.get_land_tender_details_by_tender_id(20250001)
```

## Response Data

The API returns data in JSON format. Both full and filtered versions of the data are saved to JSON files:

1. For tenders:

    - `get_all_land_tenders.json` (full data)
    - `get_all_land_tenders_FILTERED.json` (filtered fields)

2. For results:

    - `get_land_tender_results.json` (full data)
    - `get_land_tender_results_FILTERED.json` (filtered fields)

3. For tender details:
    - `get_land_tender_details_{tender_id}.json` (full data)
    - `get_land_tender_details_{tender_id}_FILTERED.json` (filtered fields)

## Field Mappings

The filtered responses include only the following fields:

### Tender Fields

- מס' מכרז (MichrazID)
- סוג מכרז (MichrazName)
- מרחב ברמ"י (KodMerchav)
- יישוב (KodYeshuv)
- שכונה/איזור (Shchuna)
- ייעוד (KodYeudMichraz)
- סטטוס (StatusMichraz)
- ת.פרסום (PirsumDate)
- ת.פתיחה (PtichaDate)
- ת.וועדת מכרזים (VaadaDate)
- מועד אחרון להגשת הצעות (SgiraDate)

### Results Fields

- מס' מכרז (MichrazID)
- מספר מתחם (MatachNumber)
- תוכנית (Tochnit)
- מגרש (Goral)
- גוש (Gush)
- חלקה (Chelka)
- מחיר סופי בש"ח (FinalPrice)
- הוצאות פיתוח בש"ח (DevelopmentCosts)
- יח"ד (YechidotDiur)
- שם זוכה (WinnerName)
- שטח במ"ר (Area)
- מחיר מינימום בש"ח (MinPrice)
- מחיר שומה בש"ח (ShumaPrice)

### Tender Details Fields

- מס' מכרז (MichrazID)
- סוג מכרז (MichrazName)
- מרחב ברמ"י (KodMerchav)
- סטטוס (StatusMichraz)
- ייעוד (KodYeudMichraz)
- יישוב (KodYeshuv)
- יחידות דיור (YechidotDiur)
- שכונה/איזור (Shchuna)
- ת.פרסום (PirsumDate)
- ת.פתיחה (PtichaDate)
- מועד אחרון להגשת הצעות (SgiraDate)
- ת.וועדת מכרזים (VaadaDate)
- תוקף ערבות (TokefArvut)
- תוקף ערבות שורש (TokefArvutSarvan)
- סכום ערבות שורש (SumArvutSarvan)
- סכום ערבות (SchumArvut)
- דיבור (Divur)
- הערות (Comments)
- רשימת מסמכים (MichrazDocList)
- מסמך מלא (MichrazFullDocument)
- תיק (Tik)