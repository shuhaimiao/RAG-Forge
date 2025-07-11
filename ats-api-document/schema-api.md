Schema API
☰ Close Sidebar
Description
This endpoint returns the schema details (i.e., what JSON schema should you expect when you ask for the particular data) for a specified profile type, search results, search filters, list of iForms, or specific iForm. Note: iCIMS utilizes the industry standard JSON schema as defined on http://json-schema.org.

API Examples
Get the JSON schema for the specified profile type
This endpoint provides the JSON schema to expect when calling the Search API.

URL:   https://api.icims.com/customers/{customerId}/profiledefinitions/v1/{profileType}/schema

{profileType}

The type of profile. Acceptable values include person, job, company, submittal, source, sourceworkflow, onboard, onboardworkflow, room and connectevent.

Action	Definition
Get:	
Example Request:

GET /customers/1771/profiledefinitions/v1/job/schema HTTP/1.1
Host: api.icims.com
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=
Content-Type: application/json
Cache-Control: no-cache

Example Response Payload (truncated):

{
    "type": "object",
    "properties": {
        "jobtemplate": {
            "type": "object",
            "properties": {
                "profile": {
                    "type": "string"
                },
                "id": {
                    "type": "integer"
                },
                "value": {
                    "type": "string"
                }
            }
        },
        "secondaryrecruiter": {
            "type": "object",
            "properties": {
                "profile": {
                    "type": "string"
                },
                "id": {
                    "type": "integer"
                },
                "value": {
                    "type": "string"
                }
            }
        },
        "talentpools": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "talentpool": {
                        "type": "object",
                        "properties": {
                            "profile": {
                                "type": "string"
                            },
                            "id": {
                                "type": "integer"
                            },
                            "value": {
                                "type": "string"
                            }
                        }
                    }
                }
            }
        },
        "hiringmanager": {
            "type": "object",
            "properties": {
                "profile": {
                    "type": "string"
                },
                "id": {
                    "type": "integer"
                },
                "value": {
                    "type": "string"
                }
            }
        },
        "positioncategory": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string"
                },
                "formattedvalue": {
                    "type": "string"
                },
                "value": {
                    "type": "string"
                }
            }
        },
        "bonus": {
            "type": "string"
        },
        "fee": {
            "type": "object",
            "properties": {
                "amountstring": {
                    "type": "string"
                },
                "amount": {
                    "type": "number"
                },
                "currency": {
                    "type": "string"
                }
            }
        },
        "joblength": {
            "type": "number"
        },
        "startdate": {
            "format": "date",
            "type": "string"
        },
        [...]
    }
}

 
Get the JSON schema for the specified field
This endpoint provides the JSON schema to expect when calling a specific field from the Profiles API.

URL:   https://api.icims.com/customers/{customerId}/profiledefinitions/v1/{profileType}/{field}/schema

{field}

The WebService Field ID for the field.

Action	Definition
Get:	
Example Request:

GET /customers/1771/profiledefinitions/v1/job/department/schema HTTP/1.1
Host: api.icims.com
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=
Content-Type: application/json
Cache-Control: no-cache

Example Response Payload:

{
    "type": "object",
    "properties": {
        "department": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string"
                },
                "formattedvalue": {
                    "type": "string"
                },
                "value": {
                    "type": "string"
                }
            }
        }
    }
}

 
Get the JSON schema for search results
This endpoint provides the JSON schema to expect when calling the Search API.

URL:   https://api.icims.com/customers/{customerId}/search/resultsSchema

Action	Definition
Get:	
Example Request:

GET /customers/1771/search/resultsSchema HTTP/1.1
Host: api.icims.com
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=
Content-Type: application/json
Cache-Control: no-cache

Example Response Payload:

{
    "type": "object",
    "properties": {
        "searchResults": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "self": {
                        "type": "string"
                    },
                    "id": {
                        "type": "integer"
                    }
                }
            }
        }
    }
}

 
Get the JSON schema for search filters
This endpoint provides the JSON schema to expect when calling the Search API.

Action	Definition
Get:	
Example Request:

GET /customers/1771/search/filtersSchema HTTP/1.1
Host: api.icims.com
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=
Content-Type: application/json
Cache-Control: no-cache
 

Example Response Payload:

{
    "type": "object",
    "properties": {
        "children": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "filters": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string"
                                },
                                "secondaryValue": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    }
                                },
                                "value": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    }
                                },
                                "operator": {
                                    "options": [
                                        "=",
                                        "!=",
                                        "<",
                                        ">",
                                        "<=",
                                        ">="
                                    ],
                                    "type": "string"
                                }
                            }
                        }
                    },
                    "operator": {
                        "options": [
                            "&",
                            "|"
                        ],
                        "type": "string"
                    }
                },
                "required": [
                    "filters"
                ]
            }
        },
        "filters": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string"
                    },
                    "secondaryValue": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "value": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "operator": {
                        "options": [
                            "=",
                            "!=",
                            "<",
                            ">",
                            "<=",
                            ">="
                        ],
                        "type": "string"
                    }
                }
            }
        },
        "operator": {
            "options": [
                "&",
                "|"
            ],
            "type": "string"
        }
    },
    "required": [
        "filters"
    ]
}

 

 
Get the JSON schema for iForms
This endpoint provides the JSON schema to expect when calling the "List all iForms accessible via web services" method described on iForms API.

URL:   https://api.icims.com/customers/{customerId}/forms/list/schema

Action	Definition
Get:	
Example Request:

GET /customers/1771/forms/list/schema HTTP/1.1
Host: api.icims.com
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=
Content-Type: application/json
Cache-Control: no-cache
 

Example Response Payload:

{
    "type": "object",
    "properties": {
        "forms": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "standardizedLevel": {
                        "type": "string",
                        "enum": [
                            "STANDARD",
                            "STANDARD_EDITED",
                            "CUSTOM",
                            "ACKNOWLEDGEMENT"
                        ]
                    },
                    "isPublicAnswers": {
                        "type": "boolean"
                    },
                    "displayName": {
                        "type": "string"
                    },
                    "formName": {
                        "type": "string"
                    },
                    "id": {
                        "type": "integer"
                    },
                    "type": {
                        "type": "string"
                    }
                }
            }
        }
    }
}

 

Get the JSON-schema for a specific iForm
This endpoint provides the JSON schema to expect when calling the "List out all questions for a specified Form" method described on iForms API.

URL:   https://api.icims.com/customers/{customerId}/forms/{formName}/meta/data_schema

Action	Definition
Get:	
Example Request:

GET /customers/1771/forms/Background_Check_template/meta/data_schema HTTP/1.1
Host: api.icims.com
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=
Content-Type: application/json
Cache-Control: no-cache
 

Example Response Payload:

{
    "type": "object",
    "properties": {
        "updatedby": {
            "type": "object",
            "properties": {
                "profile": {
                    "type": "string"
                },
                "id": {
                    "type": "integer"
                },
                "value": {
                    "type": "string"
                }
            }
        },
        "signature": {
            "type": "boolean"
        },
        "BG_Phone": {
            "type": "string"
        },
        "formname": {
            "type": "string"
        },
        "LastName2": {
            "type": "string"
        },
        "updatedfor": {
            "type": "object",
            "properties": {
                "profile": {
                    "type": "string"
                },
                "id": {
                    "type": "integer"
                },
                "value": {
                    "type": "string"
                }
            }
        },
        "Current_Addresses": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "entry": {
                        "type": "integer"
                    }
                }
            }
        },
        "Prim_Phone": {
            "type": "string"
        },
        "requestedby": {
            "type": "object",
            "properties": {
                "profile": {
                    "type": "string"
                },
                "id": {
                    "type": "integer"
                },
                "value": {
                    "type": "string"
                }
            }
        },
        "BG_Address": {
            "type": "string"
        },
        "FirstName2": {
            "type": "string"
        },
        "Phones": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "entry": {
                        "type": "integer"
                    }
                }
            }
        },
        "Education": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "entry": {
                        "type": "integer"
                    }
                }
            }
        },
        "Employment": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "entry": {
                        "type": "integer"
                    }
                }
            }
        },
        "Subscriber_Name": {
            "type": "string"
        },
        "completedby": {
            "type": "object",
            "properties": {
                "profile": {
                    "type": "string"
                },
                "id": {
                    "type": "integer"
                },
                "value": {
                    "type": "string"
                }
            }
        },
        "MiddleName2": {
            "type": "string"
        },
        "ME_MA_MN_NJ_OK_copy": {
            "type": "boolean"
        },
        "FrDate": {
            "format": "date",
            "type": "string"
        },
        "owner": {
            "type": "object",
            "properties": {
                "profile": {
                    "type": "string"
                },
                "id": {
                    "type": "integer"
                },
                "value": {
                    "type": "string"
                }
            }
        },
        "BG_URL": {
            "type": "string"
        },
        "otherfirst": {
            "type": "string"
        },
        "TDate": {
            "format": "date",
            "type": "string"
        },
        "CA_copy": {
            "type": "boolean"
        },
        "BG_Company_Name2": {
            "type": "string"
        },
        "BG_Phone2": {
            "type": "string"
        },
        "Previous_Addresses": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "Prev1Addr2": {
                        "type": "string"
                    },
                    "entry": {
                        "type": "integer"
                    }
                }
            }
        },
        "otherlast": {
            "type": "string"
        },
        "requesteddate": {
            "type": "string"
        },
        "Aliases": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "entry": {
                        "type": "integer"
                    }
                }
            }
        },
        "BG_Company_Name": {
            "type": "string"
        },
        "References": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "entry": {
                        "type": "integer"
                    }
                }
            }
        },
        "BG_Address2": {
            "type": "string"
        },
        "updateddate": {
            "type": "string"
        },
        "Package": {
            "type": "string"
        },
        "completeddate": {
            "type": "string"
        },
        "status": {
            "type": "string"
        }
    }
}

<!-- End of document -->