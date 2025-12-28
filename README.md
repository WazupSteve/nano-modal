# 🚀 Nano Modal

A minimal serverless platform for running Python functions in containers.

## Quick Start

```python
import nano_modal

app = nano_modal.App("demo")

@app.function()
def square(x):
    return x * x

# Run locally
print(square.local(5))  # 25

# Run in container (needs server running)
print(square.remote(5))  # 25

# Run in parallel
results = list(square.map(range(10)))
print(results)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

## Installation

```bash
pip install -e ".[dev]"
```

## Development

```bash
# Start Redis
docker run -d -p 6379:6379 redis:7-alpine

# Start server
python -m server.main

# Start worker (in another terminal)
python -m worker.main

# Run an example
python examples/hello.py
```

## Documentation

- [TODO.md](TODO.md) - Step-by-step implementation guide
- [examples/](examples/) - Example applications

## License

MIT
