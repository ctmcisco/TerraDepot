import json
import logging
import os
from lib import create_response, randomString, write_key, read_key_or_default

logger = logging.getLogger()
logger.setLevel(os.environ.get('LOG_LEVEL','INFO'))


def lambda_handler(event, context):
    project_id = event["pathParameters"]["projectId"]    
    logger.info(f"Got request for project {project_id}")

    configfile = f"{project_id}/config.json"
    statefile = f"{project_id}/terraform.tfstate"

    
    config = json.loads(read_key_or_default(configfile))
    project_name = config["name"]
    logger.info(f"Got request for {project_name} with id {project_id}")


    self_url = "https://" + event["requestContext"]["domainName"]

    # Get existing state or create new
    if event['httpMethod'] == "GET":
        logger.info("Type is GET, send state")
        data = read_key_or_default(statefile)
        if data == None:
            return create_response(f"No project exists, please visit {self_url}/project/new")
        else:
            return create_response(data.decode('utf-8'))
        
    # update
    if event['httpMethod'] == "POST":
        logger.info("Type is POST, save and send state")
        data = read_key_or_default(configfile)
        if data == None:
            return create_response(f"No project exists, please visit {self_url}/project/new")
        else:
            data = event["body"]
            write_key(statefile,data)
            return create_response(data)