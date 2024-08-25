import websockets
import asyncio

# Server Data
PORT = 7890
print(f"Server listening on port {PORT}")

# A set of connected WS clients
connections = set()

# The main behaviour function for this client
async def echo(websocket, path):
    print("A client just connected")
    
    # Store a copy of the client
    connections.add(websocket)
    
    # Handle incoming messages
    try:
        async for message in websocket:
            print(f"Received a msg from client, {message}")
            # Send a response to all the clients except Sender
            for conn in connections:
                if conn!=websocket:
                    await conn.send(f"{websocket} said: {message}")
    # Handle disconnecting clients
    except websockets.exceptions.ConnectionClosed as e:
        print("A Client just disconnected")
    finally:
        connections.remove(websocket)

# Start the Server
start_server = websockets.serve(echo, "localhost", PORT)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
