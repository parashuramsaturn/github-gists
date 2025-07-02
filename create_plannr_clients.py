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

class PlannrCRMClient:
    def __init__(self, api_key: str, base_url: str = "https://apidocs.plannrcrm.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.fake = Faker()
        
    def generate_client_data(self, status: str) -> Dict:
        """Generate realistic client data"""
        first_name = self.fake.first_name()
        last_name = self.fake.last_name()
        
        client_data = {
            "firstName": first_name,
            "lastName": last_name,
            "email": f"{first_name.lower()}.{last_name.lower()}@{self.fake.domain_name()}",
            "phone": self.fake.phone_number(),
            "address": {
                "street": self.fake.street_address(),
                "city": self.fake.city(),
                "state": self.fake.state(),
                "zipCode": self.fake.zipcode(),
                "country": self.fake.country()
            },
            "advisor": "parashuram joshi",
            "status": status,
            "dateOfBirth": self.fake.date_of_birth(minimum_age=18, maximum_age=85).isoformat(),
            "occupation": self.fake.job(),
            "company": self.fake.company(),
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
                "lastContact": self.fake.date_between(start_date='-1y', end_date='today').isoformat()
            }
        }
        
        return client_data
    
    def create_client(self, client_data: Dict) -> Dict:
        """Create a single client via API"""
        url = f"{self.base_url}/api/v1/client"
        
        try:
            response = self.session.post(url, json=client_data)
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
    
    def create_clients_batch(self, count: int = 100) -> List[Dict]:
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
            client_data = self.generate_client_data(status)
            
            # Create client
            result = self.create_client(client_data)
            
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
    
    def export_results_to_file(self, results: List[Dict], filename: str = "client_creation_results.json"):
        """Export results to JSON file"""
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\nResults exported to: {filename}")

def main():
    """Main function to run the client creation process"""
    
    # Configuration - Update these values
    API_KEY = "YOUR_PLANNR_CRM_API_KEY"  # Replace with your actual API key
    BASE_URL = "https://apidocs.plannrcrm.com"  # Update if different
    CLIENT_COUNT = 100
    
    # Initialize the client
    crm_client = PlannrCRMClient(api_key=API_KEY, base_url=BASE_URL)
    
    # Create clients
    results = crm_client.create_clients_batch(count=CLIENT_COUNT)
    
    # Export results
    crm_client.export_results_to_file(results)
    
    print("\nClient creation process completed!")

if __name__ == "__main__":
    main()