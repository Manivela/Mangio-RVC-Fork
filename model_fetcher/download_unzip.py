import os
import zipfile
import urllib.request

# Create the output directory if it doesn't exist
if not os.path.exists("./out"):
    os.makedirs("./out")

# Open the models.txt file and read the URLs
with open("./models.txt", "r") as f:
    urls = f.readlines()

# Download and extract each URL
for url in urls:
    # Remove any whitespace from the URL
    url = url.strip()

    # Get the filename from the URL
    filename = url.split("/")[-1]

    # Download the file
    urllib.request.urlretrieve(url, filename)

    # Extract the file to the output directory
    with zipfile.ZipFile(filename, "r") as zip_ref:
        zip_ref.extractall("./out")

    # Delete the downloaded zip file
    os.remove(filename)
