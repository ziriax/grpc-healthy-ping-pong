# grpc-healthy-ping-pong

A simple gRPC Python client and server that demonstrates how to add channel ready waiting and service health checking purely declaratively using the channel JSON configuration

## Prerequisites

- `Linux`
- `python`
- `poetry`
- `make`

## Running

```bash
./run.sh
```

> Press CTRL+C to quit

> The GRPC log files are in the `_logs` folder

## References

https://grpc.io/docs/guides/health-checking
https://grpc.io/docs/guides/service-config
https://github.com/grpc/grpc-proto/blob/master/grpc/service_config/service_config.proto
https://github.com/grpc/grpc/blob/master/doc/trace_flags.md

## Notes

All this code was written by OpenAI `o3-mini`! Of course I had to correct it a lot, as it was trained with the example gRPC code that *does not* use the JSON channel configuration! But when pointing it to read the documentation carefully and removing all the client Python code for waiting and health checking, it mostly all worked out of the box!
