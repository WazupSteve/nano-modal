"""
Phase 0 Test: square.remote(5) should return 25
"""
from nano_modal import App

app = App("test")

@app.function()
def square(x):
    return x * x

if __name__ == "__main__":
    # Test local execution first
    print(f"Local: square(5) = {square.local(5)}")
    
    # Test remote execution (requires server running)
    try:
        result = square.remote(5)
        print(f"Remote: square.remote(5) = {result}")
    except Exception as e:
        print(f"Remote failed: {e}")
        print("Make sure the server is running: python -m server.main")
