import requests

# Read the raw Python script from a file
with open("complex_test_script.py", "r") as f:
    script_content = f.read()
# Make a POST request to your local Flask server
response = requests.post(
    "http://localhost:8080/execute",
    headers={"Content-Type": "application/json"},
    json={"script": script_content}
)

# Print the result
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
