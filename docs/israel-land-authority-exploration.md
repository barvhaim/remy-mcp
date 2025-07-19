# Israeli Land Authority MCP - Website Analysis & API Documentation

## Overview
The Israeli Land Authority (רשות מקרקעי ישראל) operates a comprehensive land tenders website at `https://apps.land.gov.il/MichrazimSite/` that provides access to active land tenders, tender results, and detailed tender information.

## Website Structure

### Main Sections
1. **Active Land Tenders** (מכרזי מקרקעין פעילים) - `/search` with status filters
2. **Tender Results** (תוצאות מכרזי מקרקעין) - Completed tenders with outcomes  
3. **All Land Tenders** (כל מכרזי המקרקעין) - Combined view of all tenders
4. **Tenders on Map** (מכרזים על המפה) - Geographic visualization

### URL Patterns
- Home Page: `/#/homePage`
- Search Page: `/#/search`
- Tender Details: `/#/michraz/{tenderID}`

## API Endpoints Discovered

### 1. Search API
**Endpoint:** `POST https://apps.land.gov.il/MichrazimSite/api/SearchApi/Search`

**Purpose:** Primary search functionality for all tenders

**Request Body Parameters:**
```json
{
  "tenderNumber": "string",
  "tenderTypes": ["array of tender type IDs"],
  "settlement": "string",
  "neighborhood": "string", 
  "purpose": "string",
  "region": "string",
  "submissionDateFrom": "date",
  "submissionDateTo": "date",
  "publicationDateFrom": "date", 
  "publicationDateTo": "date",
  "targetPopulations": ["array of population filters"],
  "activeOnly": "boolean",
  "hasResults": "boolean",
  "sortBy": "string",
  "sortOrder": "string",
  "pageSize": "number",
  "pageNumber": "number"
}
```

### 2. Tender Details API
**Endpoint:** `GET https://apps.land.gov.il/MichrazimSite/api/MichrazDetailsApi/Get?michrazID={tenderID}`

**Purpose:** Get comprehensive details for a specific tender

**Response includes:**
- Tender basic information
- Timeline and dates
- Documents and announcements
- Status updates
- Location details

### 3. Tender Map Details API  
**Endpoint:** `GET https://apps.land.gov.il/MichrazimSite/api/MichrazDetailsApi/GetMichrazMapaDetails?michrazID={tenderID}`

**Purpose:** Get geographic/mapping data for tender location

## Data Schema

### Tender Types (סוג המכרז)
1. **מכרז פומבי רגיל** - Regular Public Tender
2. **מחיר מטרה** - Target Price
3. **דיור במחיר מופחת** - Reduced Price Housing
4. **מכרז ייזום** - Initiative Tender
5. **מכרז למגרש בלתי מסוים** - Unspecified Plot Tender
6. **הרשמה והגרלה** - Registration and Lottery
7. **דיור להשכרה** - Rental Housing
8. **מכרזי עמידר** - Amidar Tenders
9. **מכרזי החברה לפיתוח עכו** - Acre Development Company Tenders

### Regions (מרחב ברמ"י)
- **יו"ש** - Judea and Samaria
- **דרום** - South
- **חיפה** - Haifa
- **תל אביב** - Tel Aviv
- **ירושלים** - Jerusalem
- **מרכז** - Center

### Land Use Types (ייעוד)
- **בנייה נמוכה/צמודת קרקע** - Low-rise/Ground-attached Construction
- **בנייה רוויה** - High-density Construction
- **מסחר ו/או משרדים** - Commerce and/or Offices
- **מלונאות** - Hotels
- **מוסדות ו/או בניינים ציבוריים** - Institutions and/or Public Buildings
- **ספורט ו/או נופש ו/או תיירות ו/או מלונאות** - Sports/Recreation/Tourism/Hotels
- **מגורים ו/או מסחר ו/או מלונאות ו/או נופש** - Residential/Commercial/Hotels/Recreation
- **כרייה וחציבה** - Mining and Quarrying
- **אחר** - Other

### Tender Statuses (סטטוס)
- **מפורסם** - Published
- **בוטל** - Cancelled
- **טרם הוכרזו זוכים** - Winners Not Yet Announced

### Target Populations (אוכלוסיה מיועדת)
- **אנשים עם מוגבלות** - People with Disabilities
- **חיילי מילואים לוחמים** - Combat Reserve Soldiers
- **בני מקום** - Local Residents
- **חסרי דיור** - Homeless
- **בני מיעוטים מומלצי כוחות הביטחון** - Security Forces Recommended Minorities

### Tender Information Fields
```typescript
interface Tender {
  tenderNumber: string;          // e.g., "10/2020"
  tenderType: string;           // Type from enum above
  region: string;               // Region from enum above
  settlement: string;           // Settlement name
  neighborhood?: string;        // Neighborhood/area
  purpose: string;              // Land use type
  units?: number;               // Number of housing units (יח"ד)
  publicationDate: Date;        // Publication date
  openingDate: Date;           // Opening date for submissions
  submissionDeadline: Date;     // Last date for submissions
  status: string;              // Current status
  planNumber?: string;         // Building plan number
  mapData?: object;            // Geographic coordinates
  documents: Document[];       // Associated documents
  announcements: Announcement[]; // Updates and notices
}

interface Document {
  type: string;                // Document type
  title: string;              // Document title
  updateDate: Date;           // Last update
  downloadUrl?: string;       // Download URL if available
}

interface Announcement {
  type: string;               // Announcement type
  title: string;             // Announcement title
  date: Date;                // Publication date
  content?: string;          // Announcement content
}
```

## MCP Server Implementation Recommendations

### Core Functions to Implement

1. **search_tenders**
   - Parameters: All search criteria from SearchAPI
   - Returns: Paginated list of matching tenders
   - Use: Primary discovery function

2. **get_tender_details**
   - Parameters: tenderID
   - Returns: Complete tender information
   - Use: Deep dive into specific tender

3. **get_active_tenders**
   - Parameters: Optional filters
   - Returns: Currently active tenders only
   - Use: Quick access to bidding opportunities

4. **get_recent_results**
   - Parameters: Date range
   - Returns: Recent tender results
   - Use: Market analysis and trends

5. **search_by_location**
   - Parameters: Settlement/region/neighborhood
   - Returns: Location-specific tenders
   - Use: Geographic-based searches

6. **search_by_type**
   - Parameters: Tender type, land use
   - Returns: Type-specific tenders
   - Use: Specialized searches

7. **get_tender_documents**
   - Parameters: tenderID
   - Returns: Available documents and announcements
   - Use: Access to detailed tender materials

### Additional Utility Functions

8. **get_tender_types**
   - Returns: List of all tender types
   - Use: Reference data for filters

9. **get_regions**
   - Returns: List of all regions
   - Use: Reference data for geographic searches

10. **get_land_uses**
    - Returns: List of all land use categories
    - Use: Reference data for purpose-based searches

### Error Handling Considerations
- Handle Hebrew text encoding properly (UTF-8)
- Manage rate limiting on API calls
- Handle timeout scenarios for map data
- Validate tender IDs before API calls
- Cache reference data (types, regions, etc.)

### Data Freshness
- Tender data updates frequently
- Recommend polling interval of 15-30 minutes for active monitoring
- Status changes can happen multiple times per day
- New tenders typically published during business hours

### Authentication Notes
- No authentication required for public data access
- APIs are publicly accessible
- Rate limiting may apply (not documented)

### Special Considerations
- Website uses Hebrew language primarily
- Dates are in DD/MM/YYYY format
- Geographic data integrates with Israeli national mapping system
- Some tenders may have restricted document access
- Map functionality uses govmap.gov.il integration

## Sample MCP Implementation Structure

```python
class IsraeliLandAuthorityMCP:
    BASE_URL = "https://apps.land.gov.il/MichrazimSite/api"
    
    def search_tenders(self, **filters):
        """Search tenders with comprehensive filtering"""
        
    def get_tender_details(self, tender_id):
        """Get complete tender information"""
        
    def get_active_tenders(self, region=None, tender_type=None):
        """Get currently active tenders"""
        
    def get_recent_results(self, days=30):
        """Get recent tender results"""
        
    def search_by_location(self, settlement=None, region=None):
        """Location-based tender search"""
```

This MCP server would provide comprehensive access to Israeli land tender data, enabling applications to monitor opportunities, analyze market trends, and provide localized real estate development insights.