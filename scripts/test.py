python3 -c "
from google.auth import default, impersonated_credentials
from google.auth.transport.requests import Request
import requests

SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
TARGET_SA = 'inference-cf-invoker@PROJECT.iam.gserviceaccount.com'
FUNCTION_URL = 'https://REGION-PROJECT.cloudfunctions.net/inference-cf'

source_credentials, _ = default(scopes=SCOPES)
credentials = impersonated_credentials.Credentials(
    source_credentials=source_credentials,
    target_principal=TARGET_SA,
    target_scopes=SCOPES,
    lifetime=3600,
)
auth_req = Request()
credentials.refresh(auth_req)
url = f'https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/{TARGET_SA}:generateIdToken'
headers = {'Authorization': f'Bearer {credentials.token}', 'Content-Type': 'application/json'}
resp = requests.post(url, json={'audience': FUNCTION_URL, 'includeEmail': True}, headers=headers)
id_token = resp.json()['token']

headers = {'Authorization': f'Bearer {id_token}', 'Content-Type': 'application/json'}

body_a = {'webtris_site_id': 39, 'datetime_hour': '2025-08-05 03:00:00', 'solar': 0.0, 'generation': 27128.0, 'fossil': 4137.0}
body_b = {'webtris_site_id': 39, 'datetime_hour': '2025-08-05 13:00:00', 'solar': 9842.5, 'generation': 37559.5, 'fossil': 3320.5}

r1 = requests.post(FUNCTION_URL, json=body_a, headers=headers)
r2 = requests.post(FUNCTION_URL, json=body_b, headers=headers)

print('A:', r1.json())
print('B:', r2.json())
"