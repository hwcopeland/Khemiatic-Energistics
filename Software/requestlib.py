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

# async def get_max_xy(websocket, request_func):
#     config_response = await request_func(get_config(), websocket)
#     config = config_response.get("result", {}).get("status", {}).get("configfile", {}).get("config", {})
    
#     # Try to get dimensions from stepper configuration
#     max_x = float(config.get("stepper_x", {}).get("position_max", 0))
#     max_y = float(config.get("stepper_y", {}).get("position_max", 0))
    
#     # If not found, try to get from bed_mesh configuration
#     if max_x == 0 or max_y == 0:
#         max_x = float(config.get("bed_mesh", {}).get("mesh_max", "0,0").split(",")[0])
#         max_y = float(config.get("bed_mesh", {}).get("mesh_max", "0,0").split(",")[1])
    
#     return max_x, max_y