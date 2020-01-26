import json
import logging
import os
from lib import create_response, randomString, write_key, read_key_or_default, get_config

logger = logging.getLogger()
logger.setLevel(os.environ.get('LOG_LEVEL','INFO'))


def lambda_handler(event, context):
    project_id = event["pathParameters"]["projectId"]    
    logger.info(f"Got request for project {project_id}")

    statefile = f"{project_id}/terraform.tfstate"

    config = get_config(project_id)    
    if config["name"] == "invalid":
        self_url = "https://" + event["requestContext"]["domainName"]
        return create_response(f"No project exists, please visit {self_url}/project/new")

    project_name = config["name"]
    logger.info(f"Got request for {project_name} with id {project_id}")

    # Get existing state or create new
    if event['httpMethod'] == "GET":
        logger.info("Type is GET, send state")
        data = read_key_or_default(statefile)
        return create_response(data.decode('utf-8'))
        
    # update
    if event['httpMethod'] == "POST":
        logger.info("Type is POST, save and send state")
        data = event["body"]
        write_key(statefile,data)
        return create_response(data)