#!/usr/bin/env python3
"""
Example usage of the Plannr CRM API Client

This script demonstrates how to use the PlannrClient to interact with the Plannr CRM API.
Make sure to set your API token as an environment variable or replace the placeholder.
"""

import os
from plannr_client import PlannrClient, PlannrAPIError, create_client_from_env

def main():
    """Main example function"""
    
    # Method 1: Create client with API token directly
    # api_token = "your-api-token-here"
    # client = PlannrClient(api_token=api_token)
    
    # Method 2: Create client from environment variables
    # Set PLANNR_API_TOKEN environment variable
    try:
        client = create_client_from_env()
    except ValueError as e:
        print(f"Error: {e}")
        print("Please set the PLANNR_API_TOKEN environment variable")
        return
    
    try:
        print("=== Plannr CRM API Client Example ===\n")
        
        # 1. Get firm information
        print("1. Getting firm information...")
        try:
            firm_info = client.get_firm_info()
            print(f"   Connected to firm: {firm_info.get('name', 'Unknown')}")
            print(f"   Firm ID: {firm_info.get('_id', 'Unknown')}")
        except PlannrAPIError as e:
            print(f"   Could not get firm info: {e.message}")
        
        # 2. List accounts
        print("\n2. Listing accounts...")
        try:
            accounts = client.get_accounts(limit=5)
            print(f"   Found {len(accounts)} accounts")
            for account in accounts[:3]:  # Show first 3
                print(f"   - {account.get('name', 'Unnamed')} (ID: {account.get('_id')})")
        except PlannrAPIError as e:
            print(f"   Could not get accounts: {e.message}")
        
        # 3. Create a new account (example)
        print("\n3. Creating a new account...")
        new_account_data = {
            "name": "API Test Client",
            "email": "test@example.com",
            "phone": "+1234567890",
            "description": "Test account created via API",
            "custom": {
                "source": "API Test",
                "priority": "Medium"
            }
        }
        
        try:
            created_account = client.create_account(new_account_data)
            print(f"   Created account: {created_account['name']} (ID: {created_account['_id']})")
            account_id = created_account['_id']
            
            # 4. Create a task for the new account
            print("\n4. Creating a task for the new account...")
            new_task_data = {
                "title": "Welcome Call",
                "description": "Initial welcome call with new API test client",
                "accountId": account_id,
                "dueDate": "2025-01-20T10:00:00.000Z",
                "priority": "High"
            }
            
            try:
                created_task = client.create_task(new_task_data)
                print(f"   Created task: {created_task['title']} (ID: {created_task['_id']})")
            except PlannrAPIError as e:
                print(f"   Could not create task: {e.message}")
            
            # 5. Update the account
            print("\n5. Updating the account...")
            update_data = {
                "description": "Test account created via API - Updated!",
                "custom": {
                    "source": "API Test",
                    "priority": "High",
                    "last_updated": "2025-01-10"
                }
            }
            
            try:
                updated_account = client.update_account(account_id, update_data)
                print(f"   Updated account description: {updated_account['description']}")
            except PlannrAPIError as e:
                print(f"   Could not update account: {e.message}")
            
        except PlannrAPIError as e:
            print(f"   Could not create account: {e.message}")
            if e.response_data:
                print(f"   Response data: {e.response_data}")
        
        # 6. Search functionality
        print("\n6. Searching for accounts...")
        try:
            search_results = client.search("API Test", model_type="Account", limit=5)
            print(f"   Search found {len(search_results)} results")
            for result in search_results:
                print(f"   - {result.get('name', 'Unnamed')}")
        except PlannrAPIError as e:
            print(f"   Search failed: {e.message}")
        
        # 7. List tasks
        print("\n7. Listing recent tasks...")
        try:
            tasks = client.get_tasks(limit=5, sort="-createdAt")
            print(f"   Found {len(tasks)} tasks")
            for task in tasks:
                print(f"   - {task.get('title', 'Untitled')} (Status: {task.get('status', 'Unknown')})")
        except PlannrAPIError as e:
            print(f"   Could not get tasks: {e.message}")
        
        print("\n=== Example completed successfully! ===")
        
    except PlannrAPIError as e:
        print(f"API Error: {e.message}")
        if e.status_code:
            print(f"Status Code: {e.status_code}")
        if e.response_data:
            print(f"Response Data: {e.response_data}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")


def bulk_operations_example():
    """Example of bulk operations"""
    
    try:
        client = create_client_from_env()
    except ValueError as e:
        print(f"Error: {e}")
        return
    
    print("=== Bulk Operations Example ===\n")
    
    # Bulk create accounts
    bulk_accounts = [
        {
            "name": "Bulk Client 1",
            "email": "bulk1@example.com",
            "externalId": "bulk-001",
            "custom": {"source": "Bulk Import", "tier": "Standard"}
        },
        {
            "name": "Bulk Client 2", 
            "email": "bulk2@example.com",
            "externalId": "bulk-002",
            "custom": {"source": "Bulk Import", "tier": "Premium"}
        },
        {
            "name": "Bulk Client 3",
            "email": "bulk3@example.com", 
            "externalId": "bulk-003",
            "custom": {"source": "Bulk Import", "tier": "Standard"}
        }
    ]
    
    try:
        result = client.bulk_upsert_accounts(bulk_accounts)
        print(f"Bulk operation results:")
        print(f"  Created: {result.get('created', 0)}")
        print(f"  Updated: {result.get('updated', 0)}")
        print(f"  Errors: {len(result.get('createdErrors', []))}")
        
        if result.get('createdErrors'):
            print("  Creation errors:")
            for error in result['createdErrors']:
                print(f"    - {error}")
                
    except PlannrAPIError as e:
        print(f"Bulk operation failed: {e.message}")


if __name__ == "__main__":
    # Run the main example
    main()
    
    # Uncomment to run bulk operations example
    # print("\n" + "="*50 + "\n")
    # bulk_operations_example()