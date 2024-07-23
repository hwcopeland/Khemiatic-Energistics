import asyncio
import websockets
import json
import random
from requestlib import gcode, home, status, probe_bedmesh

MOONRAKER_WS_URL = "ws://10.255.255.6:7125/websocket"

async def request(command, websocket):
    await websocket.send(json.dumps(command))
    print(f"> Sent: {json.dumps(command, indent=2)}")
    response = await websocket.recv()
    print(f"< Received: {json.dumps(json.loads(response), indent=2)}")
    return json.loads(response)

async def main():
    try:
        async with websockets.connect(MOONRAKER_WS_URL, ping_interval=20) as websocket:
            # Request initial information
            print("Requesting printer status...")
            await request(status(), websocket)
            
            # Home the printer before starting the movement commands
            print("Homing the printer...")
            await request(home(), websocket)
            
            # Check if bed mesh calibration exists
            print("Checking for existing bed mesh calibration...")
            response = await request(probe_bedmesh(), websocket)
            bed_mesh_data = response.get("result", {}).get("status", {}).get("bed_mesh", {})
            
            if not bed_mesh_data.get("mesh_min") or not bed_mesh_data.get("mesh_max"):
                # Start bed mesh calibration if not already available
                print("Starting bed mesh calibration...")
                await request(gcode("BED_MESH_CALIBRATE"), websocket)
                
                # Wait for the bed mesh calibration to finish
                print("Waiting for bed mesh calibration to complete...")
                while True:
                    response = await request(probe_bedmesh(), websocket)
                    bed_mesh_data = response.get("result", {}).get("status", {}).get("bed_mesh", {})
                    if bed_mesh_data.get("mesh_min") and bed_mesh_data.get("mesh_max"):
                        break
                    await asyncio.sleep(1)
            
            max_x = bed_mesh_data["mesh_max"][0]
            max_y = bed_mesh_data["mesh_max"][1]
            
            print(f"Working area: X={max_x} mm, Y={max_y} mm")
            
            # Move to random positions within the working area
            while True:
                x = random.uniform(0, max_x)
                y = random.uniform(0, max_y)
                print(f"Moving to position: X={x:.2f}, Y={y:.2f}")
                
                gcode_command = f"G0 X{x:.2f} Y{y:.2f}"
                await request(gcode(gcode_command), websocket)
                await asyncio.sleep(5)

    except Exception as e:
        print(f"Connection failed: {e}")

asyncio.get_event_loop().run_until_complete(main())