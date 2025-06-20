

import requests
from faker import Faker

fake = Faker()

# https://api.iressopen.com.au/swagger/index.html?urls.primaryName=3.0#/Client/PostClientV3
def create_client():
    url = "https://api.iressopen.co.uk/client/"

    headers = {'Authorization': 'Bearer sE1bjC5DzEu5ugQBgR6tpCoju26beVNAr25LxIEx', 'x-xplan-app-id': '9yWu0XqhYbA6y4iRFy2B', 'x-forwarded-host': 'thirdpartyintegrations.xplan.iress.co.uk', 'x-api-version': '3.0'}

    # {
#   "ClientType": 0,
#   "ClientStatuses": [
#     0
#   ],
#   "ClientCategory": 0,
#   "PartnerId": 0,
#   "ClientAdviser": 0,
#   "IndividualDetails": {
#     "Title": "string",
#     "FirstName": "string",
#     "MiddleName": "string",
#     "Surname": "string",
#     "Gender": "string",
#     "DateOfBirth": "2025-06-18",
#     "MiFIDNationality": "string",
#     "MaidenName": "string",
#     "MaritalStatus": "string",
#     "PreferredName": "string",
#     "TaxResidentStatus": "string",
#     "IsSmoker": true
#   },
#   "TrustDetails": {
#     "TrustType": "string",
#     "TrustName": "string",
#     "TrustNumber": "string"
#   },
#   "CompanyDetails": {
#     "CompanyType": "string",
#     "CompanyName": "string",
#     "CompanyNumber": "string"
#   },
#   "PartnershipDetails": {
#     "PartnershipName": "string"
#   },
#   "SuperfundDetails": {
#     "SuperfundName": "string",
#     "SuperfundType": "string",
#     "SuperfundNumber": "string",
#     "ABN": "string",
#     "EstablishmentDate": "2025-06-18"
#   },
#   "HealthDetails": {
#     "MedicalHistory": "string",
#     "HealthStatus": "string"
#   }
# }
    data = {
            "ClientType": 1,
            "ClientTypeDescription": "Individual",
            "ClientStatuses": [
                4,
                32
            ],
            "ClientStatusDescriptions": [
                "Group Plan Members",
                "Contact"
            ],
            "ClientCategory": 2,
            "ClientCategoryDescription": "Platinum",
            "PartnerId": None,
            "ClientAdviser": 69326,
            "ClientAdviserDescription": "HeySaturn, Admin",
            "IsPartner": False,
            "CommunicationPreferences": {
                "EmailCommunicationPreference": "0",
                "EmailCommunicationPreferenceDescription": "No",
                "PostCommunicationPreference": "0",
                "PostCommunicationPreferenceDescription": "No",
                "PhoneCommunicationPreference": "0",
                "PhoneCommunicationPreferenceDescription": "No",
                "SmsCommunicationPreference": "0",
                "SmsCommunicationPreferenceDescription": "No"
            },
            "IndividualDetails": {
                "Title": "1",
                "TitleDescription": "Mr",
                "FirstName": fake.first_name(),
                "MiddleName": None,
                "Surname": fake.last_name(),
                "Gender": "1",
                "GenderDescription": "Male",
                "DateOfBirth": None,
                "MiFIDNationality": None,
                "MiFIDNationalityDescription": None,
                "ProposedRetirementAge": None,
                "VulnerableClient": "0",
                "VulnerableClientDescription": "No",
                "NationalInsuranceNumber": None,
                "MaidenName": None,
                "MaritalStatus": None,
                "MaritalStatusDescription": None,
                "PreferredName": fake.first_name(),
                "TaxResidentStatus": None,
                "TaxResidentStatusDescription": None,
                "IsSmoker": False
            },
            "TrustDetails": None,
            "CompanyDetails": None,
            "PartnershipDetails": None,
            "HealthDetails": {
                "MedicalHistory": None,
                "HealthComment": None,
                "GoodHealth": None
            },
            "TaxDetails": {
                "IsUKDomiciled": None,
                "IsUKDomiciledDescription": None,
                "HighestTaxRate": None,
                "HighestTaxRateDescription": None
            }
        }
    print(data)
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        user_id = response.json()
        print(user_id)

        # create a note for the client
        contact_url = f"https://api.iressopen.co.uk/client/{user_id}/contact"
        contact_data = {
            "ContactType": "m2",
            "ContactValue": fake.email(),
            "Preferred": True
            }
        contact_response = requests.post(contact_url, headers=headers, json=contact_data)
        contact_response.raise_for_status()
        print(contact_response.json())
    except Exception as e:
        print(e)
        print(response.text)
        return None

for _ in range(30):
    x = create_client()
    print(x)


