import requests
import zipfile
import os
import pandas as pd


class zipcode_get:
    def __init__(self):
        # Create the directory at the specified path, suppressing the error if the directory already exists
        tmp_path = 'app/tmp'
        os.makedirs(tmp_path, exist_ok=True)

        # URL of the zip file you want to download
        zip_file_url = "https://simplemaps.com/static/data/us-zips/1.81/basic/simplemaps_uszips_basicv1.81.zip"
        filename = zip_file_url.split('/')[-1]
        file_path = f'{tmp_path}/'
        # Send a request to the URL and store the response
        response = requests.get(zip_file_url, timeout=60)

        # Open a new file in binary write mode
        with open(file_path+filename, "wb") as zip_file:
            # Write the contents of the response to the file
            zip_file.write(response.content)

        # Unzip file

        uszips = 'uszips.csv'

        # Open the zip file
        with zipfile.ZipFile(file_path+filename) as zip_file:
            # Extract the specified file from the zip file
            zip_file.extract(uszips, tmp_path)

    def retrieve(self):
        # Read the CSV file into a DataFrame
        df = pd.read_csv('uszips.csv')
        selected_columns = df.loc[:, ['zip', 'state_id']]

        # Group the rows of the DataFrame by the 'state_id' column
        groups = selected_columns.groupby('state_id')

        # Convert each group to a dictionary where the keys are the 'state_id' values and the values are the rows from the DataFrame
        dicts = {name: group.to_dict(orient='state_id')
                 for name, group in groups}
        return dicts
