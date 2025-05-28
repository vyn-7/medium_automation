import logging
import json

def get_logger(name):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

    logging.getLogger("selenium").setLevel(logging.WARNING)
    return logging.getLogger(name)

def parse_response(content):
    try:
        if '```json' in content:
            json_part = content.split('```json')[1].split('```')[0].strip()
        else:
            json_part = content.strip()
        return json.loads(json_part)
    except json.JSONDecodeError:
        return { "title": "", "subtitle": "", "tags": "", "image": "", "body": "" }
    
