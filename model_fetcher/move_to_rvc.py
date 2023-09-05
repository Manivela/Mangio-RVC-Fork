import os
import shutil

folder_path = "../../models/"
# Loop through each file in ./out
for file in os.listdir(folder_path):
    # Check if the file is a .pth file
    if file.endswith(".pth"):
        # Save the name of the .pth file
        pth_filename = file

        # Move the .pth file to ../weights
        shutil.move(os.path.join(folder_path, file), "../weights")

        # Find the related .index file
        for index_file in os.listdir(folder_path):
            if pth_filename.split(".")[0] in index_file and index_file.endswith(
                ".index"
            ):
                # Create a folder in ../logs/ with the name of the model
                model_name = pth_filename.split(".")[0]
                os.makedirs(os.path.join("../logs", model_name), exist_ok=True)

                # Save the .index file in the model folder
                shutil.move(
                    os.path.join(folder_path, index_file),
                    os.path.join("../logs", model_name, index_file),
                )
