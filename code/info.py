import logging
import os
import json
from jinja2 import Template
from lib import (
    create_response,
    render_template,
    get_report
)

logger = logging.getLogger()
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))

DOMAIN = os.environ.get("DOMAIN")


def lambda_handler(event, context):
    project_id = event["pathParameters"]["projectId"]
    logger.info(f"Got request for project {project_id}")

    report = get_report(project_id)

    if not "metadata" in report:
        return create_response(
            "No report is available (yet). Please check out in a view seconds.",
            code=404,
        )

    # Get existing state or create new
    if event["httpMethod"] == "GET":
        output = render_template(
            template_file="project_info.html",
            report=report,
            project_id=project_id,
            domain=DOMAIN,
        )
        return create_response(output, contenttype="text/html")
