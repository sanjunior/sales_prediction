import pandas as pd
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "UdE73S3XjgJcsYIqPg7C82Y1TI6EBPTx34TPc0lXJonv"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


#Get Data from Excel
df = pd.read_excel("Store Sales.xlsx")
df['Date']=df['Date'].astype(str)
df.fillna(0, inplace=True)


# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"input_data": [{"fields": ["Store","Date","Open","Promo","StateHoliday","SchoolHoliday","StoreType","Assortment","CompetitionDistance","CompetitionOpenSinceMonth","CompetitionOpenSinceYear","Promo2","Promo2SinceWeek","Promo2SinceYear","PromoInterval"
], "values": df.values.tolist()}]}

#Execution
response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/e144ee53-4ef3-43b5-83a4-09a86b847ad7/predictions?version=2022-07-16', json=payload_scoring,
 headers={'Authorization': 'Bearer ' + mltoken})

predictions = response_scoring.json()
df['Sales'] = [x[0] for x in predictions['predictions'][0]['values']]

#Export to excel
df.to_excel('Predicted Sales.xlsx')
