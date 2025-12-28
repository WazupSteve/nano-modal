# Nano Modal - TODO Workflow

> Step-by-step tasks to build nano-modal. Check off as you complete each one.

---

## Project Structure

```
nano-modal/
├── nano_modal/              # SDK Package
│   ├── __init__.py         
│   ├── app.py              
│   ├── function.py         
│   ├── image.py            
│   ├── volume.py           
│   ├── secret.py           
│   ├── client.py           
│   ├── serialize.py        
│   ├── config.py           
│   ├── container/
│   │   ├── __init__.py     
│   │   └── entrypoint.py   
│   └── proto/
│       ├── __init__.py     
│       └── (generated)     
│
├── server/
│   ├── __init__.py         
│   ├── main.py             
│   ├── service.py          
│   └── queue.py            
│
├── worker/
│   ├── __init__.py         
│   ├── main.py             
│   ├── executor.py         
│   ├── docker_runner.py    
│   └── autoscaler.py       
│
├── proto/
│   └── nano_modal.proto    
│
├── cli/
│   ├── __init__.py         
│   └── main.py             
│
├── tests/
│   ├── __init__.py         
│   ├── test_sdk.py         
│   ├── test_server.py      
│   └── test_integration.py 
│
├── examples/
│   ├── hello.py            
│   ├── parallel.py         
│   └── deps.py             
│
├── docker-compose.yml      
├── Dockerfile.server       
├── Dockerfile.worker       
├── pyproject.toml          
└── README.md              
```

---

## Phase 0: "Ping Pong" 

**Goal:** `square.remote(5)` returns `25`

### Step 0.1: Environment Setup
- [ ] Install dependencies: `pip install -e ".[dev]"`
- [ ] Start Redis: `docker run -d -p 6379:6379 redis:7-alpine`
- [ ] Verify Docker: `docker run --rm python:3.11-slim python -c "print('works')"`

---

### Step 0.2: `serialize.py`
- [ ] Import cloudpickle
- [ ] `serialize_function(fn)` -> bytes
- [ ] `serialize_args(args, kwargs)` -> bytes
- [ ] `deserialize(data)` -> object
- [ ] Add tests

---

### Step 0.3: `app.py`
- [ ] `App` class with `name` parameter
- [ ] `functions` dict to store registered functions
- [ ] `function()` decorator method
- [ ] Wrap function in `Function` object
- [ ] Return wrapped function

---

### Step 0.4: `function.py`
- [ ] `Function` class
- [ ] Store original function and options
- [ ] `local(*args, **kwargs)` - direct execution
- [ ] `__call__` - defaults to local
- [ ] `remote(*args, **kwargs)` - calls server
- [ ] Stub `map(inputs)` for Phase 2

---

### Step 0.5: `proto/nano_modal.proto`
- [ ] Define `NanoModal` service
- [ ] `Invoke` RPC
- [ ] `GetResult` RPC
- [ ] `InvokeRequest` message
- [ ] `InvokeResponse` message
- [ ] `GetResultRequest` message
- [ ] `GetResultResponse` message
- [ ] Generate stubs with protoc

---

### Step 0.6: `client.py`
- [ ] Import grpc and generated stubs
- [ ] `get_channel()` - returns gRPC channel
- [ ] `invoke(fn_bytes, args_bytes)` -> result_bytes
- [ ] Handle connection errors
- [ ] Add timeout handling

---

### Step 0.7: `config.py`
- [ ] Read server address from env var
- [ ] `get_server_address()` -> str
- [ ] `get_redis_url()` -> str

---

### Step 0.8: `server/service.py`
- [ ] Import grpc and stubs
- [ ] `NanoModalServicer` class
- [ ] `Invoke()` - execute directly (no queue yet)
- [ ] `GetResult()` - return result from storage
- [ ] In-memory dict for results (Redis later)

---

### Step 0.9: `server/main.py`
- [ ] Create gRPC server
- [ ] Add servicer
- [ ] Bind to port 50051
- [ ] Start and wait

---

### Step 0.10: `worker/docker_runner.py`
- [ ] Import docker SDK
- [ ] `execute_in_docker(fn_bytes, args_bytes)` -> result_bytes
- [ ] Encode bytes as base64
- [ ] Generate Python code for container
- [ ] Add sandbox flags (--network none, --memory, etc)
- [ ] Parse output and return result

---

### Step 0.11: Test Ping Pong
- [ ] Start server: `python -m server.main`
- [ ] Run test: `square.remote(5)` should return `25`

---

## Phase 1: Redis Queue

### Step 1.1: `server/queue.py`
- [ ] Connect to Redis
- [ ] `enqueue_task(task_id, fn_bytes, args_bytes)`
- [ ] `dequeue_task()` -> task
- [ ] `store_result(task_id, result)`
- [ ] `get_result(task_id)` -> result

---

### Step 1.2: Update `server/service.py`
- [ ] Replace direct execution with queue push
- [ ] Return immediately after queuing
- [ ] `GetResult` reads from Redis

---

### Step 1.3: `worker/executor.py`
- [ ] Main loop: poll queue
- [ ] Dequeue task
- [ ] Call `docker_runner.execute_in_docker()`
- [ ] Store result in Redis
- [ ] Handle errors gracefully

---

### Step 1.4: `worker/main.py`
- [ ] Start executor loop
- [ ] Add graceful shutdown

---

## Phase 2: Parallel `.map()`

### Step 2.1: Update `function.py`
- [ ] `map(inputs)` generator
- [ ] Submit multiple tasks
- [ ] Collect results in order
- [ ] Yield results as they complete

---

### Step 2.2: Update Proto
- [ ] Add `InvokeMany` RPC
- [ ] Add `StreamResults` RPC
- [ ] Regenerate stubs

---

### Step 2.3: Update Server
- [ ] Handle batch invocations
- [ ] Stream results back

---

## Phase 3: Dependencies & Images

### Step 3.1: `image.py`
- [ ] `Image` class
- [ ] `python(version)` class method
- [ ] `pip_install(*packages)` method
- [ ] `run_commands(*cmds)` method
- [ ] Store config as proto message

---

### Step 3.2: Update `docker_runner.py`
- [ ] Accept image config
- [ ] Install pip packages at container start
- [ ] Run commands before function

---

## Phase 4: CLI & Polish

### Step 4.1: `cli/main.py`
- [ ] Use Click framework
- [ ] `nano-modal run <file>` - run locally
- [ ] `nano-modal serve` - start server
- [ ] `nano-modal worker` - start worker

---

### Step 4.2: `volume.py`
- [ ] `Volume` class
- [ ] Mount Docker volumes

---

### Step 4.3: `secret.py`
- [ ] `Secret` class
- [ ] Inject as environment variables

---

## Phase 5: Autoscaling

### Step 5.1: `worker/autoscaler.py`
- [ ] Monitor Redis queue depth
- [ ] `scale_up()` - start new worker container
- [ ] `scale_down()` - stop idle worker
- [ ] Main loop with configurable interval
- [ ] Min/max worker limits

---

## Daily Goals

| Day | Goal |
|-----|------|
| 1 | `serialize.py` + `app.py` + `function.py` (local works) |
| 2 | Proto + `client.py` + `config.py` |
| 3 | `server/service.py` + `server/main.py` |
| 4 | `worker/docker_runner.py` + test ping-pong |
| 5 | `server/queue.py` + `worker/executor.py` (Redis) |
| 6 | `.map()` implementation |
| 7 | `image.py` + dependencies |
| 8 | CLI + volumes + secrets |
| 9 | Autoscaler |
| 10 | Testing + polish |

---

## Success Criteria

When done, this should work:

```python
import nano_modal

app = nano_modal.App("test")
image = nano_modal.Image.python("3.11").pip_install("requests")

@app.function(image=image)
def fetch(url):
    import requests
    return len(requests.get(url).text)

# Single call
print(fetch.remote("https://example.com"))

# Parallel calls
sizes = list(fetch.map(["https://example.com"] * 10))
print(sizes)
```

---

Start with Step 0.1!
