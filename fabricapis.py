from azure.identity import InteractiveBrowserCredential
import requests
import json

# Acquire a token
# DO NOT USE IN PRODUCTION.
# Below code to acquire token is for development purpose only to test the GraphQL endpoint
# For production, always register an application in a Microsoft Entra ID tenant and use the appropriate client_id and scopes
# https://learn.microsoft.com/en-us/fabric/data-engineering/connect-apps-api-graphql#create-a-microsoft-entra-app

app = InteractiveBrowserCredential()
scp = 'https://analysis.windows.net/powerbi/api/user_impersonation'
result = app.get_token(scp)

if not result.token:
    print('Error:', "Could not get access token")

# Prepare headers
headers = {
    'Authorization': f'Bearer {result.token}',
    'Content-Type': 'application/json'
}

endpoint = 'https://5a03756f3ac0409480eab7addfb12562.z5a.graphql.fabric.microsoft.com/v1/workspaces/5a03756f-3ac0-4094-80ea-b7addfb12562/graphqlapis/72c50ef7-1e91-40db-88a3-ba517717fb80/graphql'
query = """
    query {
  fruit_infos(first: 10) {
     items {
        FruitID
        FruitName
     }
  }
}
"""

variables = {

  }
  

# Issue GraphQL request
try:
    response = requests.post(endpoint, json={'query': query, 'variables': variables}, headers=headers)
    response.raise_for_status()
    data = response.json()
    print(json.dumps(data, indent=4))
except Exception as error:
    print(f"Query failed with error: {error}")
