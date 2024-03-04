import click
import json
from json.decoder import JSONDecodeError
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from .schemas import auth_template_schema, idor_template_schema
from requests import request


def validate_template(type, template):
    try:
        json_template = json.loads(template.read())
        if type == "auth":
            validate(json_template, auth_template_schema)
        elif type == "idor":
            validate(json_template, idor_template_schema)
    except ValidationError as error:
        click.echo(
            click.style("ERROR: Invalid template", bg="red", fg="white", bold=True)
        )
        click.echo(error.message)
        exit()
    except JSONDecodeError as error:
        click.echo(click.style("ERROR: Invalid JSON", bg="red", fg="white", bold=True))
        click.echo(f"{error.msg}: line {error.lineno}")
        exit()
    else:
        return json_template


def print_response(response, value_name,  show_response):
        if str(response.status_code)[0] == "2":
            color = "green"
        elif str(response.status_code)[0] == "4":
            color = "yellow"
        elif str(response.status_code)[0] == "5":
            color = "red"
        else:
            color = "orange"
        if show_response:
            click.echo(
                f"- {value_name} "
                + click.style(
                    f"{response.status_code}", bold=True, fg="white", bg=color
                )
                + f": \n{response.text}"
            )
        else:
            click.echo(
                f"- {value_name} "
                + click.style(
                    f"{response.status_code}", bold=True, fg="white", bg=color
                )
            )


def run_auth_tests(template_data, show_response):
    for endpoint in template_data["endpoints"]:
        click.echo(
            click.style(
                f"\n# Testing endpoint [{endpoint['method']}] {endpoint['url']}",
                bold=True,
            )
        )
        headers = {}
        headers.update(template_data.get("global_headers", {}))
        headers.update(endpoint.get("headers", {}))
        for value in template_data["values"]:
            headers.update(value["headers"])
            # click.echo(f"Headers: {headers}")
            data = endpoint.get("data", None)
            if data:
                response = request(
                    endpoint["method"],
                    endpoint["url"],
                    data=json.dumps(data),
                    headers=headers,
                )
            else:
                response = request(endpoint["method"], endpoint["url"], headers=headers)
            print_response(response, value["name"], show_response)


def run_idor_tests(template_data, show_response):
    click.echo(
        click.style(
            f"\n# Testing endpoint [{template_data['method']}] {template_data['url']}",
            bold=True,
        )
    )
    replace_string = "{"+template_data["key"]+"}"
    for value in template_data["values"]:
        url = template_data["url"].replace(replace_string, value["value"])
        data = template_data.get("data", None)
        if data:
            response = request(
                template_data["method"],
                url,
                data=json.dumps(data),
                headers=template_data["headers"],
            )
        else:
            response = request(template_data["method"], url, headers=template_data["headers"])
        print_response(response, value["name"], show_response)



@click.command()
@click.argument("template", type=click.File())
@click.option(
    "-t",
    "--type",
    required=True,
    type=click.Choice(["idor", "auth"], case_sensitive=False),
    help="Test type",
)
@click.option("-r", "--show-response", is_flag=True, help="Print response text")
def main(template, type, show_response):
    """Run autoridor (type) tests for TEMPLATE file"""
    template_data = validate_template(type, template)
    if type == "auth":
        run_auth_tests(template_data, show_response)
    elif type == "idor":
        run_idor_tests(template_data, show_response)

