"""
Phase 0 Test: square.remote(5) should return 25
"""

from nano_modal import App

app = App("test")


@app.function()
def square(x):
    return x**2


if __name__ == "__main__":
    # Test local execution first
    print(f"Local: square(5) = {square.local(5)}")
    result = square.remote(5)
    print(f"Remote: square.remote(5) = {result}")
