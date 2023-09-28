import requests
from infer_api import use_rvc_infer

# Define your backend API endpoint
api_url = "https://voiceai-api.rossai.app/graphql"
text = "I'd love to say what you just typed, but you need to subscribe to the full version 2, unlock unlimited messages, with my voice and all the other ones. Once you're subscribed, you can use all the voices as much as you want."
male_voice = "en-US-ChristopherNeural"
female_voice = "en-US-AnaNeural"

# Define your GraphQL query to retrieve all models
graphql_query = """
{
  getVoiceModels {
    id
    name
    description
    gender
  }
}
"""


# Define a function to process a single model
async def process_model(model_data):
    # Replace this with your processing logic
    print(f"Processing model ID: {model_data['id']}")
    print(f"Model Name: {model_data['name']}")
    print(f"Model Description: {model_data['description']}")
    print("\n")

    # Pass the arguments as a dictionary
    arguments = {
        "model_data": model_data,
        "isYoutubeLink": False,
        "voice_and_text": [male_voice, text]
        if model_data["gender"] == "MALE"
        else [female_voice, text],
    }

    # Use square brackets for arguments
    await use_rvc_infer(arguments)


# Send the GraphQL query to your backend
response = requests.post(api_url, json={"query": graphql_query})

if response.status_code == 200:
    data = response.json().get("data", {}).get("getVoiceModels", [])

    # Process each model one by one
    for model in data:
        process_model(model)
else:
    print(f"Failed to retrieve models. Status code: {response.status_code}")
    print(response.text)
