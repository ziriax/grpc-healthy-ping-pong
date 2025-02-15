import asyncio
import json
import grpc
import pingpong_pb2
import pingpong_pb2_grpc

# ANSI color codes:
GREEN = "\033[32m"
MAGENTA = "\033[35m"
RESET = "\033[0m"

def load_config(config_file="config.json"):
    with open(config_file, "r") as f:
        return json.load(f)

async def run():
    # Load configuration from JSON
    config = load_config()
    target = config.get("channel", "localhost:50051")
    
    # Convert channel options (list of lists) into tuples
    options = [tuple(option) for option in config.get("options", [])]
    
    # Add the complete service config as a channel option if provided.
    service_config = config.get("service_config")
    if service_config:
        options.append(("grpc.service_config", json.dumps(service_config)))
    
    # Create an asynchronous gRPC channel using the target and options.
    # Notice the tracer is now "health_check_client,client_channel" per documentation.
    async with grpc.aio.insecure_channel(target, options=options) as channel:
        stub = pingpong_pb2_grpc.PingPongStub(channel)
        
        while True:
            request = pingpong_pb2.PingRequest(message="Ping")
            try:
                response = await stub.Ping(request, wait_for_ready=True)
                print(f"{GREEN}client: Received response: {response.message}{RESET}")
            except grpc.RpcError as e:
                print(f"{MAGENTA}client: Request failed: {e}{RESET}")
            
            # Wait 1 second before sending the next Ping.
            await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(run())
