...existing code...

person

person.id (number)
person.idCSV (text) - to Select Multiple IDs
person.firstname (text)
person.middlename (text)
person.lastname (text)
person.email (text)
person.emailaddress (text)
person.folder (multiselect)
# Search API

## Description
The iCIMS API supports querying (searching) for System IDs matching a given set of criteria. Up to 1,000 matching results will be returned at a time, and more can be fetched using paging filters. The Search API works for the endpoints listed below.
person.addresscity (text)

## Important Notes

- To use the Search API, a user must be part of the Integration User group.
- The results of the search will return System IDs. iCIMS cannot customize the result set (i.e. custom response payloads).
- Search API supports searching for the text value of a list item (not just Node ID).
- Search API also supports searching for a list item's SystemID.
- All requests and responses use JSON.
- The Search API is optimized for background data sync, not real-time usage.

## Caching and the Staleness Parameter
person.collectionfield####person (multiselect)

The URL takes an optional GET parameter called `staleness` (positive integer, minutes). This indicates how old the search results may be when returning results. If no staleness is specified, it defaults to 15 minutes. Cached results may be shared across users.
person.firstnamelastupdated (datetime)

**Examples:**

- Default staleness (15 min):
  `https://api.icims.com/customers/1060/search/jobs?searchJson=<your filters...>`
- Live (no staleness/caching):
  `https://api.icims.com/customers/1060/search/jobs?staleness=0&searchJson=<your filters...>`
- Up to 5 min staleness:
  `https://api.icims.com/customers/1060/search/jobs?staleness=5&searchJson=<your filters...>`
person.hiredate (dateonly)

## Available Filters
In addition to standard fields, custom fields and custom collections can be used as search filters. Four hash signs (`####`) designate the custom field ID (e.g., RCF, JCF). The filter type is listed in parentheses beside each filter.

### person

- person.id (number)
- person.idCSV (text) - to Select Multiple IDs
- person.firstname (text)
- person.middlename (text)
- person.lastname (text)
- person.email (text)
- person.emailaddress (text)
- person.folder (multiselect)
- person.externalid (text)
- person.logingroupid (multiselect)
- person.addresszip (text)
- person.addresscountry (text)
- person.addresscity (text)
- person.addressstate (listnode)
- person.createddate (datetime)
- person.updateddate (datetime)
- person.employeeinfo (relation)
- person.customfield#### (relation)
- person.collectionfield####text (text or multiselect)
- person.collectionfield####number
- person.collectionfield####date
- person.collectionfield####listnode
- person.collectionfield####person (multiselect)
- person.collectionfield####job (multiselect)
- person.firstnamelastupdated (datetime)
- person.lastnamelastupdated (datetime)
- person.emaillastupdated (datetime)
- person.jobtitlelastupdated (datetime)
- person.folderlastupdated (datetime)
- person.addresslastupdated (datetime)
- person.isfullaccessuser
- person.login.lastaccess (datetime)

#### employeeinfo
- person.startdate (dateonly)
- person.hiredate (dateonly)
- person.enddate (dateonly)

### job

- job.id (number)
- job.idCSV (text)
- job.folder (multiselect)
- job.jobnumber (text)
- job.externalid (text)
- job.jobtitle (text)
- job.jobtype (multiselect)
- job.numberofpositions (number)
- job.numberofpositionsremaining (number)
- job.hiretype (multiselect)
- job.startdate (dateonly)
- job.duedate (dateonly)
- job.positionlevel (multiselect)
- job.positiontype (multiselect)
- job.positioncategory (multiselect)
- job.createddate (datetime)
- job.updateddate (datetime)
- job.customfield#### (relation)
- job.collectionfield####text (text or multiselect)
- job.collectionfield####number
- job.collectionfield####date
- job.collectionfield####listnode
- job.collectionfield####person (multiselect)
- job.collectionfield####job (multiselect)
- job.jobpost.enddate (datetime)
- job.jobpost.isposted (select)
- job.jobpost.postdate (datetime)
- job.jobpost.postedtohub (select)
- job.jobpost.status (multiselect)
- job.jobpost.type (multiselect)
- job.joblocation.addresscity (text)
- job.joblocation.addressstate (listnode)
- job.joblocation.addressstatetext (text)
- job.joblocation.addresscountry (multiselect)
- job.joblocation.addresscountrytext (text)
- job.joblocation.addresszip (text)
- job.joblocation.zipradius (zipradius)
- job.joblocation.companyid (number)
- job.postedto (multiselect)
- job.priority (multiselect)

### company

- company.id (number)
- company.idCSV (text)
- company.name (text)
- company.addresscity (text)
- company.addresszip (text)
- company.addresscountry (multiselect)
- company.addressstate (listnode)
- company.zipradius (zipradius)
- company.createddate (datetime)
- company.updateddate (datetime)
- company.customfield#### (relation)
- company.collectionfield####text
- company.collectionfield####number
- company.collectionfield####date
- company.collectionfield####listnode
- company.collectionfield####person (multiselect)
- company.collectionfield####job (multiselect)

### applicantworkflow

- applicantworkflow.bin (multiselect)
- applicantworkflow.status (multiselect)
- applicantworkflow.updateddate (datetime)
- applicantworkflow.person (relation)
  - Example: `{ "name": "applicantworkflow.person.id", "value": ["system ID"] }`
- applicantworkflow.job (relation)
  - Example: `{ "name": "applicantworkflow.job.id", "value": ["system ID"] }`
- applicantworkflow.customfield#### (relation)
- applicantworkflow.collectionfield####text
- applicantworkflow.collectionfield####number
- applicantworkflow.collectionfield####date
- applicantworkflow.collectionfield####listnode
- applicantworkflow.collectionfield####person (multiselect)
- applicantworkflow.collectionfield####job (multiselect)

### talentpools

- talentpool.createddate (datetime)
- talentpool.updateddate (datetime)
- talentpool.postedto (multiselect)
- talentpool.title.text
- talentpool.externalid.text
- talentpool.folder.number
- talentpool.owner.number
- talentpool.customfield#### (rcf 4 digit)

### sourceworkflows

- sourceworkflow.associatedprofile.person (multiselect)
- sourceworkflow.createddate (datetime)
- sourceworkflow.updateddate (datetime)
- sourceworkflow.postedto (multiselect)
- sourceworkflow.baseprofile.number
- sourceworkflow.source.number
- sourceworkflow.sourceorigin.number
- sourceworkflow.sourcename.number
- sourceworkflow.sourceperson.person (multiselect)
- sourceworkflow.status.number
- sourceworkflow.vendorname.text
- sourceworkflow.customfield####(rcf 4 digit).(fieldtype)

### formdata

- formdata.id (Backend Note: Schema - FormDataIDNumeric, alias FormDataID - label="Form Data ID")
- formdata.formid (Schema - FormID - label="Form Name") (multiselect)
- formdata.formstatus (multiselect)
- formdata.updateddate (datetime)
- formdata.completeddate (datetime)
- formdata.form (relation)
  - Example: `{ "name": "formdata.form.formname", "value": ["[form name]"] }`
- formdata.personformpersonid (text)
- formdata.submittalformsubmittalid (text)
- formdata.submittalformpersonid (text)
- formdata.submittalformjobid (text)
- formdata.onboardworkflowformonboardworkflowid (text)

### form

- form.formname (text)

> **Note:** All ID filters must be added manually to the query JSON. Password and custom password fields are not supported through the Search API and cannot be used as filter criteria.
job.idCSV (text)

## Available Filter Operators

| Operator | Description | Available Field Types |
|----------|-------------|----------------------|
| `==`     | Exact match for text type fields. | text |
| `!==`    | Is not an exact match for text type fields. (Some fields do not support this operator.) | text |
| `=`      | Listnode, multiselect, select, zipradius, dateonly, datetime, and number fields filter by exact match. Text fields filter by contains. | listnode, multiselect, select, zipradius, dateonly, datetime, number, text |
| `!=`     | Multiselect, select, dateonly, datetime, and number fields filter by not matching. Text fields filter by does not contain. (Some fields do not support this operator.) | multiselect, select, dateonly, datetime, number, text |
| `<`      | Less than | dateonly, datetime, number |
| `>`      | Greater than | dateonly, datetime, number |
| `<=`     | Less than or equal to | dateonly, datetime, number |
| `>=`     | Greater than or equal to | dateonly, datetime, number |
job.createddate (datetime)
## API Examples

### Basic Example
In the following example, the "operator" for the filter group is omitted. It is assumed to be "&", but in this case it makes no difference, since there is only one filter.

```json
{
  "filters": [
    {
      "name": "person.firstname",
      "value": ["Mike"],
      "operator": "="
    }
  ]
}
```

### Multiple Filters
In the following example, the "operator" for the filters are omitted. They are assumed to be "=".
The operator for the filter group is explicitly included and set to "&". It could also be "|".

```json
{
  "filters": [
    {
      "name": "person.firstname",
      "value": ["Mike"]
    },
    {
      "name": "person.lastname",
      "value": ["Smith"]
    }
  ],
  "operator": "&"
}
```

### Custom Field Filters
Assume that person profiles have a custom field, "rcf2145," that stores text data; the following example will demonstrate how to query on this custom field data. Other custom field types can be queried using "number", "date", "listnode", "person", or "job" filters, if the field supports those filter types.

```json
{
  "filters": [
    {
      "name": "person.customfield2145.text",
      "value": ["test"]
    }
  ]
}
```

Collections are similar, however, they do not get a dot. The same arguments are valid: "text", "number", "date", "listnode", "person", or "job". Assume now that there is a numerical custom field "rcf2231" that exists within a collection on the person profile; the following example will demonstrate how to query on this data, as well as how to specify a ">" operator. Note that this operator only works with numerical field types.

```json
{
  "filters": [
    {
      "name": "person.collectionfield2231number",
      "value": ["1234"],
      "operator": ">"
    }
  ]
}
```

### Date Filters
Dates in the Search API may be in either a "yyyy-MM-dd hh:mm a" or a  "yyyy-MM-dd" format (with no time added). All dates in the Search API will be assumed to be in the UTC time zone, regardless of user settings; if no time is specified, Midnight UTC will be assumed. If a date is not formatted properly, it will be ignored. This is in line with the core Search Engine. This brings Search API dates in line with dates elsewhere in the API.

If a date is used via the Search API that is in a format that is not recognized, then the search will assume the most lenient date range, allowing all results through. Date filters also do not support blank searches; i.e. a data must be specified when using the value or secondary value search filter.

For custom date ranges, the JSON will take a VALUE parameter as the initial start date and SECONDARYVALUE as the end date. An example of a Date search request is below:

```json
{
  "filters": [
    {
      "secondaryValue": [
        "2013-06-10 11:59 PM"
      ],
      "name": "person.updateddate",
      "value": [
        "2013-05-01 12:00 AM"
      ],
      "operator": "="
    }
  ],
  "operator": "&"
}
```

The following example search will find all entries between midnight June 10th and June 17th of 2013:

```json
{
  "filters": [
    {
      "name": "person.updateddate",
      "value": ["2013-06-10"],
      "secondaryValue": ["2013-06-17"]
    }
  ]
}
```

If the end date is omitted, the search will find all entries starting at 5:00 PM on September 5th, with no end boundary:

```json
{
  "filters": [
    {
      "name": "person.updateddate",
      "value": ["2013-09-05 05:00 PM"]
    }
  ]
}
```

To get all entries before the specified date, omit the value and specify a secondaryValue.

### And/Or Nesting
To combine filters in a more complicated way, use the "children" attribute on the filter group. For example, the following query could be used to find a person with a first name of "John" or "Jane", but always with a last name of "Doe".

```json
{
  "filters": [
    {
      "name": "person.lastname",
      "value": ["Doe"]
    }
  ],
  "operator": "&",
  "children": [
    {
      "filters": [
        {
          "name": "person.firstname",
          "value": ["John"]
        },
        {
          "name": "person.firstname",
          "value": ["Jane"]
        }
      ],
      "operator": "|"
    }
  ]
}
```

### Paging
Results are always sorted in ascending order by System ID. If there are more than 1000 results, only the first 1000 will be displayed. To fetch the next 1000 results, append a filter on the ID. For example, assume the following query returns more than 1000 results:

```json
{
  "filters": [
    {
      "name": "person.lastname",
      "value": ["Smith"]
    }
  ]
}
```

When reading through the results, keep track of the last system ID that is returned, which is guaranteed to be the greatest one.

Assume for the following example that the highest system ID returned by the above query is 1234. By modifying the query in the following way, the next 1000 results will be fetched:

```json
{
  "filters": [
    {
      "name": "person.lastname",
      "value": ["Smith"]
    },
    {
      "name": "person.id",
      "value": ["1234"],
      "operator": ">"
    }
  ]
}
```

To fetch subsequent pages, replace the "1234" value with the new highest system ID from the previous page's results.

## Responses
Links to the search endpoint should be added to the generic API information request results.

All profile and form references returned by the API will now include a `self` attribute that contains a link to the current profile via the API. All links that appear in the headers for all API integrations will now also appear in the JSON response body. The headers are not removed from API requests that already have them; the new `self` attributes exist in addition to the headers for previously existing requests.

The results will be in a standardized format, also formatted as JSON.

```json
{
  "searchResults": [
    {
      "id": "1",
      "self": "LINK"
    },
    {
      "id": "2",
      "self": "LINK"
    }
  ]
}
```

The `id` is the System ID, which is useful for paging and making API requests to get more information about a specific profile. The `self` attribute provides a direct link to make a request for more information from that profile as a convenience, so you won't have to generate it yourself. The results will always be ordered by `id` in ascending order, so for paging, you only have to look at the last result in the JSON array.

If the search has no results, it will return an empty searchResults array:

```json
{
  "errors": [
    {
      "errorMessage": "MESSAGE",
      "errorCode": "CODE"
    }
  ]
}
```

## Error Handling
The following error messages can be sent as a response when searching the API:

| Scenario | Error Message |
|----------|--------------|
| Must specify at least one filter. | At least one filter must be specified |
| Invalid filter or hidden filter | The following filter is either not valid or hidden: [filter] |
| Invalid filter operator | The following filter operator is not valid in the given context: [operator] |
| Invalid group operator | The following group operator is not valid in the given context: [operator] |
| Unrecognized filter attribute | The following filter attribute is unrecognized: [attribute] |
| Unrecognized group attribute: xxxx | The following group attribute is unrecognized: [attribute] |
| Unknown parsing error. | An unknown parsing error occurred |

Any invalid filters added into the API search query will be rejected and an error will be shown indicating which one is invalid. Blank filter names will be rejected and filter names that include criteria for the wrong search type. For example, the following are now invalid:

- A filter where name is not defined at all.
- A filter where name is defined as ''.
- A filter on a person search that has a name of 'job.*' or vice versa.

When specifying an altogether invalid operator, the request will be denied. If you choose the wrong operator for a specific filter, the request will fail. If the query specifies an attribute with an unrecognized name (e.g., 'name1' instead of 'name'), the entire query will be rejected (even if the rest of the query is fine).

Valid operators for filters are different than for groups, and it validates based on context.

When specifying an invalid list node id, all results will be filtered out. Searches that do not specify at least one filter are rejected.
job.customfield#### (relation)
job.joblocation.addressstatetext (text)
job.joblocation.addresscountry (multiselect)
job.joblocation.addresscountrytext (text)
job.joblocation.addresszip (text)
job.joblocation.zipradius (zipradius)
job.joblocation.companyid (number)
job.postedto (multiselect)
job.priority (multiselect)
company

company.id (number)
company.idCSV (text)
company.name (text)
company.addresscity (text)
company.addresszip (text)
company.addresscountry (multiselect)
company.addressstate (listnode)
company.zipradius (zipradius)
company.createddate (datetime)
company.updateddate (datetime)
company.customfield#### (relation)
company.collectionfield####text
company.collectionfield####number
company.collectionfield####date
company.collectionfield####listnode
company.collectionfield####person (multiselect)
company.collectionfield####job (multiselect)
applicantworkflow

applicantworkflow.bin (multiselect)
applicantworkflow.status (multiselect)
applicantworkflow.updateddate (datetime)
applicantworkflow.person (relation)
Example: { "name": "applicantworkflow.person.id", "value": ["system ID"], }
applicantworkflow.job (relation)
Example: { "name": "applicantworkflow.job.id", "value": ["system ID"], }
applicantworkflow.customfield#### (relation)
applicantworkflow.collectionfield####text
applicantworkflow.collectionfield####number
applicantworkflow.collectionfield####date
applicantworkflow.collectionfield####listnode
applicantworkflow.collectionfield####person (multiselect)
applicantworkflow.collectionfield####job (multiselect)
talentpools

talentpool.createddate (datetime)
talentpool.updateddate (datetime)
talentpool.postedto (multiselect)
talentpool.title.text
talentpool.externalid.text
talentpool.folder.number
talentpool.owner.number
talentpool.customfield#### (rcf 4 digit)
sourceworkflows

sourceworkflow.associatedprofile.person (multiselect)
sourceworkflow.createddate (datetime)
sourceworkflow.updateddate (datetime)
sourceworkflow.postedto (multiselect)
sourceworkflow.baseprofile.number
sourceworkflow.source.number
sourceworkflow.sourceorigin.number
sourceworkflow.sourcename.number
sourceworkflow.sourceperson.person (multiselect)
sourceworkflow.status.number
sourceworkflow.vendorname.text
sourceworkflow.customfield####(rcf 4 digit).(fieldtype)
formdata

formdata.id (Backend Note: Schema - FormDataIDNumeric, alias FormDataID - label="Form Data ID")
formdata.formid (Schema - FormID - label="Form Name") (multiselect)
formdata.formstatus (multiselect)
formdata.updateddate (datetime)
formdata.completeddate (datetime)
formdata.form (relation)
Example: {"name":"formdata.form.formname","value":['[form name]']
​​formdata.personformpersonid (text)
formdata.submittalformsubmittalid (text)
formdata.submittalformpersonid (text)
formdata.submittalformjobid (text)
formdata.onboardworkflowformonboardworkflowid (text)
form

form.formname (text) 
 

Note: All ID filters must be added manually to the query JSON. In addition, password and custom password fields are not supported through the Search API and cannot be used as filter criteria.

API Examples
Available Filter Operators
The following list of filter operators that can be used within a given Search Query is below. (Note: If none is specified, '=' is assumed. These are not all valid for all filter types.)

Operator	Description	Available Field Types
'=='	Exact match for text type fields.	text
'!=='	Is not an exact match for text type fields. (Note: Some fields do not support this operator.)	text
'='	Listnode, multiselect, select, zipradius, dateonly, datetime, and number fields filter by exact match. Text based fields filter by contains.	listnode, multiselect, select, zipradius, dateonly, datetime, number, text
'!='	Multiselect, select, dateonly, datetime, and number fields filter by not matching. Text based fields filter by does not contain. (Note: Some fields do not support this operator.)	multiselect, select, dateonly, datetime, number, text
'<'	Less than	dateonly, datetime, number
'>'	Greater than	dateonly, datetime, number
'<='	Less than or equal to	dateonly, datetime, number
'>='	Greater than or equal to	dateonly, datetime, number
 

Basic Example
In following example, the "operator" for the filter group is omitted. It is assumed to be "&", but in this case it makes no difference, since there is only one filter.

{
     "filters": [
           {
                "name": "person.firstname",
                "value": ["Mike"],
                "operator": "="
           }
     ]
}
Multiple Filters
In the following example, the "operator" for the filters are omitted. They are assumed to be "=".

The operator for the filter group is explicitly included and set to "&". It could also be "|".

{
     "filters": [
           {
                "name": "person.firstname",
                "value": ["Mike"]
           },
           {
                "name": "person.lastname",
                "value": ["Smith"]
           }
     ],
     "operator": "&"
}
Custom Field Filters
Assume that person profiles have a custom field, "rcf2145," that stores text data; the following example will demonstrate how to query on this custom field data. Other custom field types can be queried using "number", "date", "listnode", "person", or "job" filters, if the field supports those filter types.

{
     "filters": [
           {
                "name": "person.customfield2145.text",
                "value": ["test"]
           }
     ]   
}
Collections are similar, however, they do not get a dot. The same arguments are valid: "text", "number", "date", "listnode", "person", or "job". Assume now that there is a numerical custom field "rcf2231" that exists within a collection on the person profile; the following example will demonstrate how to query on this data, as well as how to specify a ">" operator. Note that this operator only works with numerical field types.

{
     "filters": [
           {
                "name": "person.collectionfield2231number",
                "value": ["1234"],
                "operator": ">"
           }
     ]
}
Date Filters
Dates in the Search API may be in either a "yyyy-MM-dd hh:mm a" or a  "yyyy-MM-dd" format (with no time added). All dates in the Search API will be assumed to be in the UTC time zone, regardless of user settings; if no time is specified, Midnight UTC will be assumed. If a date is not formatted properly, it will be ignored. This is in line with the core Search Engine. This brings Search API dates in line with dates elsewhere in the API.

If a date is used via the Search API that is in a format that is not recognized, then the search will assume the most lenient date range, allowing all results through. Date filters also do not support blank searches; i.e. a data must be specified when using the value or secondary value search filter.

For custom date ranges, the JSON will take a VALUE parameter as the initial start date and SECONDARYVALUE as the end date. An example of a Date search request is below:

{
    "filters": [
        {
            "secondaryValue": [
                "2013-06-10 11:59 PM"
            ],
            "name": "person.updateddate",
            "value": [
                "2013-05-01 12:00 AM"
            ],
            "operator": "="
        }
    ],
    "operator": "&"
}
iCIMS system admin users can access the Get SQL button on the search engine to show dates in the correct format and time zone to match what is selected in the filter. This function is restricted to iCIMS support.

Date filters use the "secondaryValue" of the filter. A date filter may omit either the value or the secondaryValue. Searches that include valid values for both will be constrained only to entries between those times. If a date is invalid or omitted, then that boundary is removed and the search will extend indefinitely.

The following example search will find all entries between midnight June 10th and June 17th of 2013:

{
     "filters": [
           {
                "name": "person.updateddate",
                "value": ["2013-06-10"],
                "secondaryValue": ["2013-06-17"]
           }
     ]
}
If the end date is omitted, the search will find all entries starting at 5:00 PM on September 5th, with no end boundary:

{
     "filters": [
           {
                "name": "person.updateddate",
                "value": ["2013-09-05 05:00 PM"]
           }
     ]
}
To get all entries before the specified date, omit the value and specify a secondaryValue.

And/Or Nesting
To combine filters in a more complicated way, use the "children" attribute on the filter group. For example, the following query could be used to find a person with a first name of "John" or "Jane", but always with a last name of "Doe".

{
     "filters": [
           {
                "name": "person.lastname",
                "value": ["Doe"]
           }
     ],
     "operator": "&",
     "children": [
          {
                "filters": [
                     {
                           "name": "person.firstname",
                           "value": ["John"]
                     },
                     {
                           "name": "person.firstname",
                           "value": ["Jane"]
                     }
                ],
                "operator": "|"
           }
     ]
}
This query uses a child grouping that contains the filters for checking the first name of John or Jane, using the "|" operator on the filter group. The top level filter group uses the "&" operator to compare the results of the child groups to the native filter it has in the top group.

Paging
Results are always sorted in ascending order by System ID. If there are more than 1000 results, only the first 1000 will be displayed. To fetch the next 1000 results, appending a filter on the ID. For example, assume the following query returns more than 1000 results:

{
     "filters": [
           {
                "name": "person.lastname",
                "value": ["Smith"]
           }
     ]
}
When reading through the results, keep track of the last system ID that is returned, which is guaranteed to be the greatest one.

Assume for the following example that the highest system ID returned by the above query is 1234. By modifying the query in the following way, the next 1000 results will be fetched:

{
     "filters": [
           {
                "name": "person.lastname",
                "value": ["Smith"]
           },
           {
                "name": "person.id",
                "value": ["1234"],
                "operator": ">"
           }
     ]
}
To fetch subsequent pages, replace the "1234" value with the new highest system ID from the previous page's results.

Responses
Links to the search endpoint should be added to the generic API information request results.

All profile and form references returned by the API will now include a "self" attribute that contains a link to the current profile via the API. All links that appear in the headers for all API integrations will now also appear in the JSON response body. The headers are not removed from API requests that already have them; the new "self" attributes exist in addition to the headers for previously existing requests.

The results will be in a standardized format, also formatted as JSON.

{
     "searchResults": [
           {
                "id": "1",
                "self": "LINK"
           },
           {
                "id": "2",
                "self": "LINK"
           }
     ]
}
The "id" is the System ID, which is useful for paging and making API requests to get more information about a specific profile. The "self" attribute provides a direct link to make a request for more information from that profile as a convenience, so you won't have to generate it yourself. The results will always be ordered by "id" in ascending order, so for paging, you only have to look at the last result in the JSON array.

If the search has no results, it will return an empty searchResults array:

{
     "errors": [
           {
                "errorMessage": "MESSAGE",
                "errorCode": "CODE"
           }
     ]
}
 
Error Handling
The following error messages can be sent as a response when searching the API:

Scenario: Must specify at least one filter.
Error Message: At least one filter must be specified
Scenario: Invalid filter or hidden filter
Error Message: The following filter is either not valid or hidden: [filter]
Scenario: Invalid filter operator
Error Message: The following filter operator is not valid in the given context: [operator]
Scenario: Invalid group operator
Error Message: The following group operator is not valid in the given context: [operator]
Scenario: Unrecognized filter attribute
Error Message: The following filter attribute is unrecognized: [attribute]
Scenario: Unrecognized group attribute: xxxx
Error Message: The following group attribute is unrecognized: [attribute]
Scenario: Unknown parsing error.
Error Message: An unknown parsing error occurred
Any invalid filters added into the API search query will be rejected and an error will be shown indicating which one is invalid. Blank filter names will be rejected and filter names that include criteria for the wrong search type. For example, the following are now invalid:

A filter where name is not defined at all.
A filter where name is defined as ''.
A filter on a person search that has a name of 'job.*' or vice versa.
When specifying an altogether invalid operator, the request will be denied. If you choose the wrong operator for a specific filter, the request will fail. If the query specifies an attribute with an unrecognized name (e.g., 'name1' instead of 'name'), the entire query will be rejected (even if the rest of the query is fine).

Valid operators for filters are different than for groups, and it validates based on context.

When specifying an invalid list node id, all results will be filtered out. Searches that do not specify at least one filter are rejected.

<!-- End of document -->
