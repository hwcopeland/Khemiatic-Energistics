import json
import uuid

## Library for generating JSON-RPC requests to Moonraker

def generate_unique_id():
    return str(uuid.uuid4())

def gcode(script):
    return {
        "jsonrpc": "2.0",
        "method": "printer.gcode.script",
        "params": {
            "script": script
        },
        "id": generate_unique_id()
    }

def home():
    return gcode("G28")

def status():
    return {
        "jsonrpc": "2.0",
        "method": "printer.info",
        "id": generate_unique_id()
    }

def get_config():
    return {
        "jsonrpc": "2.0",
        "method": "printer.objects.query",
        "params": {
            "objects": {
                "configfile": ["config"]
            }
        },
        "id": generate_unique_id()
    }