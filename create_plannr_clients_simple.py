#!/usr/bin/env python3
"""
Script to create 100 clients in Plannr CRM (Simple version - no external dependencies)
Requirements:
- 100 clients total
- advisor: parashuram joshi
- status split across: active, deceased, archived, inactive
"""

import json
import random
import time
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timedelta
from typing import List, Dict

class PlannrCRMClientSimple:
    def __init__(self, api_key: str, base_url: str = "https://apidocs.plannrcrm.com"):
        self.api_key = api_key
        self.base_url = base_url
        
        # Sample data for generating realistic clients
        self.first_names = [
            "John", "Jane", "Michael", "Sarah", "David", "Lisa", "Robert", "Mary",
            "William", "Jennifer", "James", "Patricia", "Christopher", "Linda", "Matthew",
            "Elizabeth", "Daniel", "Susan", "Mark", "Jessica", "Anthony", "Karen",
            "Steven", "Nancy", "Paul", "Betty", "Andrew", "Helen", "Kenneth", "Sandra",
            "Joshua", "Donna", "Kevin", "Carol", "Brian", "Ruth", "George", "Sharon",
            "Timothy", "Michelle", "Ronald", "Laura", "Jason", "Sarah", "Edward", "Kimberly",
            "Jeffrey", "Deborah", "Ryan", "Dorothy", "Jacob", "Amy", "Gary", "Angela"
        ]
        
        self.last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
            "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
            "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
            "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
            "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill",
            "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell",
            "Mitchell", "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner"
        ]
        
        self.companies = [
            "Tech Solutions Inc", "Global Consulting", "Innovative Systems", "Alpha Corp",
            "Beta Industries", "Creative Designs", "Future Technologies", "Prime Services",
            "Elite Enterprises", "Advanced Solutions", "Dynamic Systems", "Strategic Partners",
            "Modern Solutions", "Digital Innovations", "Professional Services", "Quality Assurance Corp",
            "Excellence Group", "Premier Solutions", "Optimal Systems", "Superior Services"
        ]
        
        self.cities = [
            "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia",
            "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville",
            "Fort Worth", "Columbus", "Charlotte", "San Francisco", "Indianapolis", "Seattle",
            "Denver", "Washington", "Boston", "Nashville", "Oklahoma City", "Las Vegas",
            "Detroit", "Portland", "Memphis", "Louisville", "Baltimore", "Milwaukee"
        ]
        
        self.states = [
            "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID",
            "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS",
            "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK",
            "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
        ]
        
        self.occupations = [
            "Software Engineer", "Project Manager", "Sales Representative", "Marketing Manager",
            "Financial Advisor", "Teacher", "Nurse", "Doctor", "Lawyer", "Accountant",
            "Consultant", "Designer", "Analyst", "Engineer", "Administrator", "Director",
            "Manager", "Specialist", "Coordinator", "Supervisor", "Executive", "Architect"
        ]
        
    def generate_client_data(self, status: str) -> Dict:
        """Generate realistic client data using built-in libraries only"""
        first_name = random.choice(self.first_names)
        last_name = random.choice(self.last_names)
        
        # Generate random birth date (18-85 years old)
        today = datetime.now()
        birth_year = today.year - random.randint(18, 85)
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 28)  # Safe day for any month
        birth_date = datetime(birth_year, birth_month, birth_day)
        
        # Generate random phone number
        phone = f"({random.randint(200, 999)}) {random.randint(200, 999)}-{random.randint(1000, 9999)}"
        
        # Generate email
        email_domain = random.choice(["gmail.com", "yahoo.com", "outlook.com", "company.com", "business.org"])
        email = f"{first_name.lower()}.{last_name.lower()}@{email_domain}"
        
        client_data = {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "phone": phone,
            "address": {
                "street": f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Pine', 'Elm', 'Cedar'])} {random.choice(['St', 'Ave', 'Blvd', 'Dr', 'Ln'])}",
                "city": random.choice(self.cities),
                "state": random.choice(self.states),
                "zipCode": f"{random.randint(10000, 99999)}",
                "country": "United States"
            },
            "advisor": "parashuram joshi",
            "status": status,
            "dateOfBirth": birth_date.strftime("%Y-%m-%d"),
            "occupation": random.choice(self.occupations),
            "company": random.choice(self.companies),
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
                "lastContact": (today - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d")
            }
        }
        
        return client_data
    
    def create_client(self, client_data: Dict) -> Dict:
        """Create a single client via API using urllib"""
        url = f"{self.base_url}/api/v1/client"
        
        try:
            # Prepare request
            data = json.dumps(client_data).encode('utf-8')
            
            req = urllib.request.Request(url, data=data)
            req.add_header('Authorization', f'Bearer {self.api_key}')
            req.add_header('Content-Type', 'application/json')
            req.add_header('Accept', 'application/json')
            
            # Make request
            with urllib.request.urlopen(req) as response:
                response_data = json.loads(response.read().decode('utf-8'))
                return {
                    "success": True,
                    "data": response_data,
                    "status_code": response.getcode()
                }
                
        except urllib.error.HTTPError as e:
            return {
                "success": False,
                "error": f"HTTP Error {e.code}: {e.reason}",
                "status_code": e.code,
                "response_text": e.read().decode('utf-8') if e.fp else None
            }
        except urllib.error.URLError as e:
            return {
                "success": False,
                "error": f"URL Error: {e.reason}",
                "status_code": None,
                "response_text": None
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "status_code": None,
                "response_text": None
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
    
    # Validate API key
    if API_KEY == "YOUR_PLANNR_CRM_API_KEY":
        print("❌ ERROR: Please update the API_KEY variable with your actual Plannr CRM API key")
        print("   You can find this in your Plannr CRM settings/API section")
        return
    
    # Initialize the client
    print("Initializing Plannr CRM client...")
    crm_client = PlannrCRMClientSimple(api_key=API_KEY, base_url=BASE_URL)
    
    # Create clients
    print("Starting client creation process...\n")
    results = crm_client.create_clients_batch(count=CLIENT_COUNT)
    
    # Export results
    crm_client.export_results_to_file(results)
    
    print("\nClient creation process completed!")
    print("Please check the results file for detailed information about each client creation attempt.")

if __name__ == "__main__":
    main()