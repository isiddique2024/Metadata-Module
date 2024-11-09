import requests

url = "http://127.0.0.1:5002/generate"

input_text = input("Enter Prompt: ")

payload = {"input_text": input_text}

response = requests.post(url, json=payload)

if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    generated_text = data.get("generated_text", "No text generated.")
    
    result = generated_text
    nodesArray = result.split(",")
    print(nodesArray)
    print(result)  # Optional: Print it to verify
else:
    print(f"Failed to connect to API: {response.status_code}")

    #The M551 Sheridan light tank, known for its mobility and versatility, is equipped with a DF670 diesel engine that relies heavily on a well-maintained  GE87 air intake system for optimal performance. Proper upkeep of the air intake filter is critical to ensure the engine receives clean, debris-free air, which helps maintain efficient combustion and prevents engine wear. WHAT is the relationship between M551 and DF670. Sample output should be in this format (object,relationship,object) dont generate any other text beside the output.Relation is defined in this scenario as one object that is part of an another object