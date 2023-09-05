import os
import requests

folder_path = "../weights/"
AUTH_TOKEN = ""

idx = 0
data = []
for file in os.listdir(folder_path):
    # Check if the file is a .pth file
    if file.endswith(".pth"):
        # Save the name of the .pth file
        pth_filename = file

        # split by _ capitialize the first letter of each word and join with spaces
        model_name = " ".join([word.capitalize() for word in pth_filename.split("_")])
        # remove ".pth" from model name
        model_name = model_name.split(".")[0]

        # create prod data
        runpodId = f"dump_1_{idx}"
        idx += 1
        gender = "MALE"

        # push json to data
        data.append(
            {
                "runpodId": runpodId,
                "gender": gender,
                "name": model_name,
                "modelPath": pth_filename,
                "status": "succeeded",
            }
        )

print(data)

# call createManyVoiceModel graphql mutation at https://voiceai-api.rossai.app/graphql with auth header
mutation = """
mutation createManyVoiceModel($data: [VoiceModelCreateManyInput!]!) {
    createManyVoiceModel(data: $data) {
        count}
        }
"""

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + AUTH_TOKEN,
}

response = requests.post(
    "https://voiceai-api.rossai.app/graphql",
    json={"query": mutation, "variables": {"data": data}},
    headers=headers,
)
