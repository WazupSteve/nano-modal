# Nano Modal - TODO Workflow

> Detailed step-by-step tasks. Checking off as I complete each one.

---

## Project Structure

```
nano-modal/
├── nano_modal/              
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

## Phase 0: Weekend 1 - "Ping Pong" (Goal: `square.remote(5)` returns `25`)

### Step 0.1: Environment Setup
- [ ] **0.1.1** Install dependencies
- [ ] **0.1.2** Start Redis
- [ ] **0.1.3** Verify Docker works

---

### Step 0.2: Implement `serialize.py` 
**File:** `nano_modal/serialize.py`

- [ ] **0.2.1** Import cloudpickle
- [ ] **0.2.2** Implement `serialize_function(fn)` -> bytes
- [ ] **0.2.3** Implement `serialize_args(args, kwargs)` -> bytes
- [ ] **0.2.4** Implement `deserialize(data)` -> object
- [ ] **0.2.5** Add tests in `tests/test_sdk.py`

---

### Step 0.3: Implement `app.py` 
**File:** `nano_modal/app.py`

- [ ] **0.3.1** Create `App` class with `name` parameter
- [ ] **0.3.2** Add `functions` dict to store registered functions
- [ ] **0.3.3** Implement `function()` decorator method
- [ ] **0.3.4** Decorator should wrap function in `Function` object
- [ ] **0.3.5** Return wrapped function (not original)

---

### Step 0.4: Implement `function.py` 
**File:** `nano_modal/function.py`

- [ ] **0.4.1** Create `Function` class
- [ ] **0.4.2** Store original function and options
- [ ] **0.4.3** Implement `local(*args, **kwargs)` - direct execution
- [ ] **0.4.4** Implement `__call__` - defaults to local
- [ ] **0.4.5** Implement `remote(*args, **kwargs)` - calls server
- [ ] **0.4.6** Stub `map(inputs)` - we'll finish in Phase 2

---

### Step 0.5: Generate Proto Stubs
- [ ] **0.5.1** Run protoc to generate Python stubs
- [ ] **0.5.2** Verify files created:
  - `nano_modal/proto/nano_modal_pb2.py`
  - `nano_modal/proto/nano_modal_pb2_grpc.py`
- [ ] **0.5.3** Fix import in generated grpc file (common issue)

---

### Step 0.6: Implement `client.py` 
**File:** `nano_modal/client.py`

- [ ] **0.6.1** Import grpc and generated stubs
- [ ] **0.6.2** Create `get_channel()` - returns gRPC channel
- [ ] **0.6.3** Implement `invoke(fn_bytes, args_bytes)` -> result_bytes
- [ ] **0.6.4** Handle connection errors gracefully
- [ ] **0.6.5** Add timeout handling


---

### Step 0.7: Implement `config.py` 
**File:** `nano_modal/config.py`

- [ ] **0.7.1** Read server address from env var or default
- [ ] **0.7.2** Implement `get_server_address()` -> str
- [ ] **0.7.3** Add `get_redis_url()` for later

---

### Step 0.8: Implement Server `service.py` 
**File:** `server/service.py`

- [ ] **0.8.1** Import grpc and generated stubs
- [ ] **0.8.2** Create `NanoModalServicer` class
- [ ] **0.8.3** Implement `Invoke()` - for now, execute directly (no queue)
- [ ] **0.8.4** Implement `GetResult()` - return result from storage
- [ ] **0.8.5** Use dict for in-memory result storage (replace with Redis later)

---

### Step 0.9: Implement Server `main.py` (~50 LOC)
**File:** `server/main.py`

- [ ] **0.9.1** Create gRPC server
- [ ] **0.9.2** Add servicer
- [ ] **0.9.3** Bind to port 50051
- [ ] **0.9.4** Start and wait

---

### Step 0.10: Implement `docker_runner.py` (~250 LOC)
**File:** `worker/docker_runner.py`

- [ ] **0.10.1** Import docker SDK
- [ ] **0.10.2** Implement `execute_in_docker(fn_bytes, args_bytes)` -> result_bytes
- [ ] **0.10.3** Encode bytes as base64 for passing to container
- [ ] **0.10.4** Generate Python code to run inside container
- [ ] **0.10.5** Add sandbox flags (--network none, --memory, etc)
- [ ] **0.10.6** Parse output and return result bytes
