import json
import uuid

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

def probe_bedmesh():
    return {
        "jsonrpc": "2.0",
        "method": "printer.objects.query",
        "params": {
            "objects": {
                "bed_mesh": ["profiles"]
            }
        },
        "id": generate_unique_id()
    }