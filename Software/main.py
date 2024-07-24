import asyncio
import websockets
import json
from requestlib import gcode, home, status, get_max_xy
from workflow import steps as reaction_steps
from workflow import ProcedureStep

MOONRAKER_WS_URL = "ws://10.255.255.6:7125/websocket"

async def keepalive(websocket):
    while True:
        await websocket.send(json.dumps({"jsonrpc": "2.0", "method": "machine.info", "id": "keepalive"}))
        await asyncio.sleep(10)

def convert_procedure_step(procedure_step: ProcedureStep) -> str:
    if procedure_step.action == "add":
        amount = procedure_step.parameters.get('amount', 0)  # Default to 0 if 'amount' is missing
        return f"G1 F2000 E{amount}"  # Activate extruder to add solvent
    elif procedure_step.action == "add_dropwise":
        amount = procedure_step.parameters.get('amount', 0)  # Default to 0 if 'amount' is missing
        return f"G1 F2000 E{amount}"  # Activate extruder to add solvent dropwise
    elif procedure_step.action == "heat":
        temperature = procedure_step.parameters.get('temperature', 0)  # Default to 0 if 'temperature' is missing
        return f"M104 S{temperature}"  # Set hotend temperature
    elif procedure_step.action == "cool":
        return f"M104 S0"  # Turn off hotend heating
    elif procedure_step.action == "seal":
        return f"G28"  # Home the printer (assuming sealing involves homing)
    elif procedure_step.action == "transfer":
        compound = procedure_step.parameters.get('compound', 'unknown')
        mols = procedure_step.parameters.get('mols', 0)
        transfer_rate = procedure_step.parameters.get('transfer_rate', 'unknown')
        return f"Simulating transfer of {mols} mols of {compound} at {transfer_rate} rate."
    else:
        raise ValueError(f"Unknown action: {procedure_step.action}")

async def request(command, websocket):
    await websocket.send(json.dumps(command))
    print(f"> Sent: {json.dumps(command, indent=2)}")
    response = await websocket.recv()
    print(f"< Received: {json.dumps(json.loads(response), indent=2)}")
    return json.loads(response)

async def main():
    try:
        async with websockets.connect(MOONRAKER_WS_URL, ping_interval=20) as websocket:
            asyncio.create_task(keepalive(websocket))
            # Home the printer before starting the movement commands
            print("Homing the printer...")
            await request(home(), websocket)

            # Get max X and Y
            max_x, max_y = await get_max_xy(websocket, request)
            print(f"Working area: X={max_x} mm, Y={max_y} mm")

            # Execute the reaction steps
            for reaction_step in reaction_steps:
                print(f"Executing reaction: {reaction_step.reaction}")
                for procedure_step in reaction_step.procedure:
                    gcode_command = convert_procedure_step(procedure_step)
                    print(f"Sending G-code command: {gcode_command}")
                    await request(gcode(gcode_command), websocket)

                    # Wait for the G-code command to complete
                    while True:
                        response = await websocket.recv()
                        response_dict = json.loads(response)
                        if 'error' in response_dict and response_dict['error']['code'] == -32601 and response_dict['error']['message'] == 'Method not found' and response_dict['id'] == 'keepalive':
                            continue
                        elif 'result' in response_dict and response_dict['result'] == 'ok':
                            print(f"G-code command completed: {gcode_command}")
                            break
                        elif 'method' in response_dict:
                            if response_dict['method'] != 'notify_proc_stat_update':
                                print(f'< Received: {response}')
                        else:
                            print(f'< Received: {response} (no method)')
                    

    except Exception as e:
        print(f"Connection failed: {e}")

asyncio.get_event_loop().run_until_complete(main())