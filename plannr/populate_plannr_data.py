#!/usr/bin/env python3
"""
Script to create 100 clients in Plannr CRM
Requirements:
- 100 clients total
- advisor: parashuram joshi
- status split across: active, deceased, archived, inactive
"""

import requests
import json
import random
import time
from faker import Faker
from typing import List, Dict

# Sample client data for testing API calls
SAMPLE_CLIENT_DATA = {
    "firstName": "John",
    "lastName": "Smith",
    "email": "john.smith@example.com",
    "phone": "+1-555-123-4567",
    "address": {
        "street": "123 Main Street",
        "city": "New York",
        "state": "NY",
        "zipCode": "10001",
        "country": "United States"
    },
    "advisor": "parashuram joshi",
    "status": "active",
    "dateOfBirth": "1985-06-15",
    "occupation": "Software Engineer",
    "company": "Tech Solutions Inc",
    "notes": "Client created via API - Status: active",
    "preferredContactMethod": "email",
    "riskTolerance": "moderate",
    "investmentGoals": "retirement planning",
    "annualIncome": 125000,
    "netWorth": 350000,
    "tags": ["active", "api-created"],
    "customFields": {
        "source": "API Import",
        "priority": "high",
        "lastContact": "2024-01-15"
    }
}

def test_api_call(base_url: str, headers: Dict = None) -> Dict:
    """Test API call with sample client data"""
    url = f"{base_url}/api/v1/client"
    
    print("Testing API call with sample client data:")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(SAMPLE_CLIENT_DATA, indent=2)}")
    print("-" * 50)
    
    try:
        response = requests.post(url, json=SAMPLE_CLIENT_DATA, headers=headers)
        response.raise_for_status()
        
        result = {
            "success": True,
            "data": response.json(),
            "status_code": response.status_code
        }
        print(f"✅ API call successful!")
        print(f"Status Code: {result['status_code']}")
        print(f"Response: {json.dumps(result['data'], indent=2)}")
        
    except requests.exceptions.RequestException as e:
        result = {
            "success": False,
            "error": str(e),
            "status_code": getattr(e.response, 'status_code', None),
            "response_text": getattr(e.response, 'text', None)
        }
        print(f"❌ API call failed!")
        print(f"Error: {result['error']}")
        if result.get('status_code'):
            print(f"Status Code: {result['status_code']}")
        if result.get('response_text'):
            print(f"Response: {result['response_text']}")
    
    return result

def generate_client_data(fake: Faker, status: str) -> Dict:
    """Generate realistic client data"""
    first_name = fake.first_name()
    last_name = fake.last_name()
    
    client_data = {
        "firstName": first_name,
        "lastName": last_name,
        "email": f"{first_name.lower()}.{last_name.lower()}@{fake.domain_name()}",
        "phone": fake.phone_number(),
        "address": {
            "street": fake.street_address(),
            "city": fake.city(),
            "state": fake.state(),
            "zipCode": fake.zipcode(),
            "country": fake.country()
        },
        "advisor": "parashuram joshi",
        "status": status,
        "dateOfBirth": fake.date_of_birth(minimum_age=18, maximum_age=85).isoformat(),
        "occupation": fake.job(),
        "company": fake.company(),
        "notes": f"Client created via API - Status: {status}",
        "preferredContactMethod": random.choice(["email", "phone", "mail"]),
        "riskTolerance": random.choice(["conservative", "moderate", "aggressive"]),
        "investmentGoals": random.choice([
            "retirement planning", 
            "wealth accumulation", 
            "education funding", 
            "estate planning",
            "tax planning"
        ]),
        "annualIncome": random.randint(30000, 500000),
        "netWorth": random.randint(50000, 2000000),
        "tags": [status, "api-created"],
        "customFields": {
            "source": "API Import",
            "priority": random.choice(["high", "medium", "low"]),
            "lastContact": fake.date_between(start_date='-1y', end_date='today').isoformat()
        }
    }
    
    return client_data

def create_client(base_url: str, session: requests.Session, client_data: Dict) -> Dict:
    """Create a single client via API"""
    url = f"{base_url}/api/v1/client"
    
    try:
        response = session.post(url, json=client_data)
        response.raise_for_status()
        return {
            "success": True,
            "data": response.json(),
            "status_code": response.status_code
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e),
            "status_code": getattr(e.response, 'status_code', None),
            "response_text": getattr(e.response, 'text', None)
        }

def create_clients_batch(base_url: str, session: requests.Session, fake: Faker, count: int = 100) -> List[Dict]:
    """Create multiple clients with distributed status"""
    
    # Define status distribution (roughly equal split)
    statuses = ["active", "deceased", "archived", "inactive"]
    clients_per_status = count // len(statuses)
    remainder = count % len(statuses)
    
    # Create status list with distribution
    status_list = []
    for i, status in enumerate(statuses):
        # Add one extra client to first 'remainder' statuses
        extra = 1 if i < remainder else 0
        status_list.extend([status] * (clients_per_status + extra))
    
    # Shuffle to randomize order
    random.shuffle(status_list)
    
    results = []
    successful_creates = 0
    failed_creates = 0
    
    print(f"Creating {count} clients with advisor 'parashuram joshi'")
    print(f"Status distribution: {dict(zip(statuses, [status_list.count(s) for s in statuses]))}")
    print("-" * 60)
    
    for i, status in enumerate(status_list, 1):
        print(f"Creating client {i}/{count} with status: {status}")
        
        # Generate client data
        client_data = generate_client_data(fake, status)
        
        # Create client
        result = create_client(base_url, session, client_data)
        
        if result["success"]:
            successful_creates += 1
            print(f"✅ Successfully created: {client_data['firstName']} {client_data['lastName']}")
        else:
            failed_creates += 1
            print(f"❌ Failed to create client: {result.get('error', 'Unknown error')}")
            if result.get('status_code'):
                print(f"   Status Code: {result['status_code']}")
            if result.get('response_text'):
                print(f"   Response: {result['response_text'][:200]}...")
        
        results.append({
            "client_number": i,
            "client_data": client_data,
            "result": result
        })
        
        # Add small delay to respect rate limits
        time.sleep(0.1)
        
        # Progress update every 10 clients
        if i % 10 == 0:
            print(f"Progress: {i}/{count} clients processed")
            print(f"Success: {successful_creates}, Failed: {failed_creates}")
            print("-" * 30)
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total clients processed: {count}")
    print(f"Successfully created: {successful_creates}")
    print(f"Failed: {failed_creates}")
    print(f"Success rate: {(successful_creates/count)*100:.1f}%")
    
    # Status breakdown
    print("\nStatus Distribution:")
    for status in statuses:
        count_for_status = status_list.count(status)
        print(f"  {status.capitalize()}: {count_for_status}")
    
    return results

if __name__ == "__main__":
    # Configuration - update these values for your API
    BASE_URL = "https://your-plannr-api-url.com"  # Update this URL
    API_HEADERS = {
        "Authorization": "Bearer YOUR_API_TOKEN",  # Update with your token
        "Content-Type": "application/json"
    }
    
    print("Plannr Client Data Population Script")
    print("=" * 50)
    
    # Test with sample data first
    print("\n1. Testing with sample client data...")
    test_result = test_api_call(BASE_URL, API_HEADERS)
    
    if test_result["success"]:
        print("\n✅ Sample test successful! You can now run the batch creation.")
        
        # Uncomment the lines below to run batch creation
        # fake = Faker()
        # session = requests.Session()
        # session.headers.update(API_HEADERS)
        # 
        # print("\n2. Creating 100 clients...")
        # batch_results = create_clients_batch(BASE_URL, session, fake, count=100)
    else:
        print("\n❌ Sample test failed. Please check your API configuration.")
        print("Update BASE_URL and API_HEADERS in the script before proceeding.")

