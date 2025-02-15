import asyncio
import random
import grpc
import pingpong_pb2
import pingpong_pb2_grpc

from grpc_health.v1 import health, health_pb2_grpc, health_pb2

# ANSI color codes:
CYAN = "\033[36m"   # Normal server messages now in cyan.
RED = "\033[31m"
RESET = "\033[0m"

class PingPongServicer(pingpong_pb2_grpc.PingPongServicer):
    async def Ping(self, request, context):
        response_message = f"Pong: {request.message}"
        print(f"{CYAN}server: Received ping with message: {request.message} – responding with: {response_message}{RESET}")
        return pingpong_pb2.PongResponse(message=response_message)

async def run_server():
    # Create an asynchronous gRPC server.
    server = grpc.aio.server()
    
    # Register the PingPong service.
    pingpong_pb2_grpc.add_PingPongServicer_to_server(PingPongServicer(), server)
    
    # Register the health checking service.
    health_servicer = health.HealthServicer()
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)
    service_name = "pingpong.PingPong"
    health_servicer.set(service_name, health_pb2.HealthCheckResponse.SERVING)
    health_servicer.set("", health_pb2.HealthCheckResponse.SERVING)
    
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    await server.start()
    print(f"{CYAN}server: Server started on {listen_addr}{RESET}")

    # Determine a random uptime before failure (between 5 and 10 seconds).
    uptime = random.randint(5, 10)
    print(f"{CYAN}server: Server will simulate a failure in {uptime} seconds.{RESET}")
    await asyncio.sleep(uptime)

    # Simulate server failure by shutting it down.
    print(f"{RED}server: Simulating server failure now. Shutting down...{RESET}")
    await server.stop(0)
    print(f"{RED}server: Server has stopped.{RESET}")

async def main():
    while True:
        await run_server()
        # Wait a random delay before restarting (between 5 and 10 seconds).
        restart_delay = random.randint(5, 10)
        print(f"{CYAN}server: Server will restart in {restart_delay} seconds.{RESET}\n")
        await asyncio.sleep(restart_delay)

if __name__ == '__main__':
    asyncio.run(main())
