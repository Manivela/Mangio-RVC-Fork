import json
import requests
from infer_api import use_rvc_infer

# Define your backend API endpoint
api_url = "https://voiceai-api.rossai.app/graphql"
text = "I'd love to say what you just typed, but you need to subscribe to the full version 2, unlock unlimited messages, with my voice and all the other ones. Once you're subscribed, you can use all the voices as much as you want."
male_voice = "en-US-ChristopherNeural"
female_voice = "en-US-AnaNeural"

# Define your GraphQL query to retrieve all models

graphql_query = """
query GetOnlyPublicVoiceModels {
  getOnlyPublicVoiceModels(page: 1, pageSize: 1000) {
    id
    modelPath
    gender
  }
}
"""

AUTH_TOKEN = None
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + AUTH_TOKEN,
}


graphql_mutation = """
mutation InferTTS($ttsParams: TTsParamsInput!, $modelId: String!, $isAsync: Boolean) {
  inferTTS(ttsParams: $ttsParams, modelId: $modelId, isAsync: $isAsync) {
    success
  }
}
"""


import nest_asyncio
import asyncio

nest_asyncio.apply()


# Define a function to process a single model
def process_model(model_data):
    # Replace this with your processing logic
    print(f"Processing model ID: {model_data['id']}")
    print(f"Model Path: {model_data['modelPath']}")
    print("\n")
    # Pass the arguments as a dictionary
    arguments = {
        "model_data": model_data,
        "isYoutubeLink": False,
        "voice_and_text": [male_voice, text]
        if model_data["gender"] == "MALE"
        else [female_voice, text],
    }
    # Pass the arguments as json string like {'arguments': {'model': 'adele.pth', 'userId': '123', 'ttsParams': {'text': 'Naber lo, ben adele', 'voiceType': 'en-US-JennyNeural'}}, 'type': 'INFER_TTS'}
    voiceType = male_voice
    if model_data["gender"] == "FEMALE":
        voiceType = female_voice
    arguments = {
        "arguments": {
            "model": model_data["modelPath"],
            "userId": "test-auto-infer",
            "ttsParams": {
                "text": text,
                "voiceType": voiceType,
            },
        },
        "type": "INFER_TTS",
    }

    print(arguments)

    response = asyncio.run(use_rvc_infer(arguments, False, True))
    output_url = response["output_url"]
    model_mutation = f"""
      mutation UpdateOneVoiceModel {{
        updateOneVoiceModel(data: {{
          voiceUrl: {{
            set: "{output_url}"
          }}
        }},
        where: {{
          id: "{model_data['id']}"
        }}) {{
          voiceUrl
          id
        }}
      }} 
      """

    mutation_response = requests.post(
        api_url,
        json={"query": model_mutation},
        headers=headers,
    )
    print(mutation_response.text)


# Send the GraphQL query to your backend
response = requests.post(api_url, json={"query": graphql_query}, headers=headers)

# response = requests.post(
#     api_url,
#     mutation=graphql_mutation,
#     headers=headers,
# )
from time import sleep

if response.status_code == 200:
    data = response.json().get("data", {}).get("getOnlyPublicVoiceModels", [])
    # print(f"Retrieved {len(data)} models")
    # print("\n")
    # print(data)
    # Process each model one by one

    for model in data:
        try:
            process_model(model)
        except Exception as e:
            print(e)


else:
    print(f"Failed to retrieve models. Status code: {response.status_code}")
    print(response.text)
