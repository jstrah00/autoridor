auth_template_schema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "endpoints": {
      "type": "array",
      "items": [
        {
          "type": "object",
          "properties": {
            "url": {
              "type": "string"
            },
            "method": {
              "type": "string",
              "enum": ["POST", "GET", "DELETE", "OPTIONS", "PATCH", "PUT"]
            },
            "data": {
              "type": "object"
            },
            "headers": {
              "type": "object"
            }
          },
          "required": [
            "url",
            "method"
          ]
        }
      ]
    },
    "global_headers": {
      "type": "object"
    },
    "values": {
      "type": "array",
      "items": [
        {
          "type": "object",
          "properties": {
            "name": {
              "type": "string"
            },
            "headers": {
              "type": "object"
            }
          },
          "required": [
            "name",
            "headers"
          ]
        }
      ]
    }
  },
  "required": [
    "endpoints",
    "values"
  ]
}

idor_template_schema  = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "url": {
      "type": "string"
    },
    "method": {
      "type": "string"
    },
    "headers": {
      "type": "object"
    },
    "data": {
      "type": "object"
    },
    "key": {
      "type": "string"
    },
    "values": {
      "type": "array",
      "items": [
        {
          "type": "object",
          "properties": {
            "name": {
              "type": "string"
            },
            "value": {
              "type": "string"
            }
          },
          "required": [
            "name",
            "value"
          ]
        }
      ]
    }
  },
  "required": [
    "url",
    "method",
    "key",
    "values"
  ]
}
