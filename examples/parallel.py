import nano_modal

app = nano_modal.App("test")


@app.function()
def compute(x):
    return x * x


# Test the new map!
results = list(compute.map([1, 2, 3, 4, 5]))
print(results)  # Should be [1, 4, 9, 16, 25]
