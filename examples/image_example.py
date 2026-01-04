import nano_modal

app = nano_modal.App("image_test")

# image config
image = nano_modal.Image.python("3.11").pip_install("requests")


# use the image in the function decorator
@app.function(image=image)
def fetch_url(url):
    import requests

    return len(requests.get(url).text)


# call remotely
result = fetch_url.remote("https://google.com")
print(f"page size: {result} bytes")
