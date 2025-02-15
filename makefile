.PHONY: install protos server client run-all clean

# Stamp file for installation.
.VENV_STAMP := .venv/pyproject.stamp

# Stamp file for proto compilation.
.PROTO_STAMP := proto/.protos.stamp

# The install target: run only when pyproject.toml or poetry.toml changes.
install: $(.VENV_STAMP)

$(.VENV_STAMP): pyproject.toml poetry.toml
	@echo "Installing dependencies with Poetry..."
	poetry install --no-root
	@mkdir -p .venv
	@touch $(.VENV_STAMP)
	@echo "Dependencies installed."

# The protos target: re-run when proto file changes (or after install).
protos: install $(.PROTO_STAMP)

$(.PROTO_STAMP): proto/pingpong.proto
	@echo "Compiling Protocol Buffers..."
	poetry run python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. ./proto/pingpong.proto
	@touch $(.PROTO_STAMP)
	@echo "Protos compiled."

# run-all: starts the client (to show wait-for-ready behavior) then the server via an external script.
run-all: install protos
	./start-client-then-server.sh

clean:
	@echo "Cleaning stamp files..."
	@rm -f $(.VENV_STAMP) $(.PROTO_STAMP)
