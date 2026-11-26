# autoridor

Template-driven CLI to test API endpoints for **IDOR** and **broken authorization**. Describe the endpoints and the identities (or object IDs) once in a JSON template, run it, and compare status codes side by side.

## Install

```bash
pip install .
```

## Usage

```bash
autoridor -t auth auth_template.json      # same endpoints, different users
autoridor -t idor idor_template.json      # same user, different object IDs
autoridor -t auth auth_template.json -r   # also print response bodies
```

Status codes are colored (2xx green, 4xx yellow, 5xx red), so a `200` where you expected a `403` stands out.

## Templates

**`auth`**: every endpoint is called once per entry in `values`, merging its headers (typically `Authorization`) over `global_headers` and the endpoint's own headers. See [`auth_template.json`](auth_template.json).

**`idor`**: one URL with a `{key}` placeholder, replaced by each entry in `values`. See [`idor_template.json`](idor_template.json).

Templates are validated against a JSON schema before any request is sent.

> Only use against systems you are authorized to test.
