#!/usr/bin/env python3
"""
Plannr CRM API Client

A comprehensive Python client for interacting with the Plannr CRM API.
Based on the API documentation at https://apidocs.plannrcrm.com/

Features:
- Full authentication support (Bearer token)
- All major API endpoints (Accounts, Plans, Tasks, etc.)
- Proper error handling and response validation
- Rate limiting awareness
- Bulk operations support
- Custom field handling

Author: AI Assistant
Created: 2025
"""

import requests
import json
import time
from typing import Dict, List, Optional, Union, Any
# Type checking will be relaxed for API responses due to dynamic nature
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PlannrAPIError(Exception):
    """Custom exception for Plannr API errors"""
    def __init__(self, message: str, status_code: Optional[int] = None, response_data: Optional[Dict] = None):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(self.message)


class PlannrClient:
    """
    Plannr CRM API Client
    
    Provides a comprehensive interface to interact with the Plannr CRM API.
    """
    
    def __init__(self, api_token: str, base_url: str = "https://api.plannrcrm.com"):
        """
        Initialize the Plannr API client
        
        Args:
            api_token (str): Your Plannr API access token
            base_url (str): Base URL for the Plannr API (default: https://api.plannrcrm.com)
        """
        self.api_token = api_token
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json',
            'User-Agent': 'PlannrPythonClient/1.0'
        })
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 0.3  # 200 requests per minute = ~0.3 seconds between requests
    
    def _rate_limit(self):
        """Implement basic rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)
        self.last_request_time = time.time()
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Union[Dict, List[Dict]]] = None, params: Optional[Dict] = None) -> Union[Dict, List[Dict]]:
        """
        Make an HTTP request to the Plannr API
        
        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE)
            endpoint (str): API endpoint
            data (Dict, optional): Request body data
            params (Dict, optional): Query parameters
            
        Returns:
            Dict: Response data
            
        Raises:
            PlannrAPIError: If the request fails
        """
        self._rate_limit()
        
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data if data else None,
                params=params if params else None
            )
            
            # Handle different response codes as per API documentation
            if response.status_code == 200:
                # Success
                try:
                    return response.json()
                except json.JSONDecodeError:
                    return {"message": response.text}
            elif response.status_code == 206:
                # Partial success (bulk operations)
                return response.json()
            elif response.status_code == 400:
                # Bad request
                error_data = response.json() if response.content else {}
                raise PlannrAPIError(
                    f"Bad request: {error_data.get('message', 'Invalid request payload')}",
                    status_code=400,
                    response_data=error_data
                )
            elif response.status_code == 403:
                # Permission error
                error_data = response.json() if response.content else {}
                raise PlannrAPIError(
                    f"Permission denied: {error_data.get('message', 'Insufficient permissions')}",
                    status_code=403,
                    response_data=error_data
                )
            elif response.status_code == 500:
                # Server error
                raise PlannrAPIError(
                    "Server error occurred. Please try again later.",
                    status_code=500
                )
            else:
                # Other errors
                error_data = response.json() if response.content else {}
                raise PlannrAPIError(
                    f"HTTP {response.status_code}: {error_data.get('message', response.text)}",
                    status_code=response.status_code,
                    response_data=error_data
                )
                
        except requests.RequestException as e:
            raise PlannrAPIError(f"Request failed: {str(e)}")
    
    # Account Management
    def get_accounts(self, limit: int = 100, offset: int = 0, **kwargs) -> List[Dict]:
        """
        Get all accounts
        
        Args:
            limit (int): Maximum number of records to return (default: 100, max: 2000)
            offset (int): Number of records to skip
            **kwargs: Additional query parameters (sort, select, etc.)
            
        Returns:
            List[Dict]: List of account objects
        """
        params = {'limit': limit, 'offset': offset, **kwargs}
        return self._make_request('GET', '/accounts', params=params)  # type: ignore
    
    def get_account(self, account_id: str) -> Dict:
        """
        Get a specific account by ID
        
        Args:
            account_id (str): Account ID (can be _id, externalId with 'extid-' prefix, or sourceId with 'srcid-' prefix)
            
        Returns:
            Dict: Account object
        """
        return self._make_request('GET', f'/accounts/{account_id}')  # type: ignore
    
    def create_account(self, account_data: Dict) -> Dict:
        """
        Create a new account
        
        Args:
            account_data (Dict): Account data (name is required)
            
        Returns:
            Dict: Created account object
        """
        return self._make_request('POST', '/accounts', data=account_data)  # type: ignore
    
    def update_account(self, account_id: str, account_data: Dict) -> Dict:
        """
        Update an existing account
        
        Args:
            account_id (str): Account ID
            account_data (Dict): Updated account data
            
        Returns:
            Dict: Updated account object
        """
        return self._make_request('PUT', f'/accounts/{account_id}', data=account_data)  # type: ignore
    
    def delete_account(self, account_id: str) -> Dict:
        """
        Delete an account
        
        Args:
            account_id (str): Account ID
            
        Returns:
            Dict: Deletion confirmation
        """
        return self._make_request('DELETE', f'/accounts/{account_id}')  # type: ignore
    
    def bulk_upsert_accounts(self, accounts_data: List[Dict]) -> Dict:
        """
        Bulk create/update accounts
        
        Args:
            accounts_data (List[Dict]): List of account objects (max 5000)
            
        Returns:
            Dict: Bulk operation results
        """
        if len(accounts_data) > 5000:
            raise PlannrAPIError("Maximum 5000 accounts allowed per bulk operation")
        return self._make_request('PUT', '/accounts', data=accounts_data)  # type: ignore
    
    # Plans Management
    def get_plans(self, limit: int = 100, offset: int = 0, **kwargs) -> List[Dict]:
        """Get all plans"""
        params = {'limit': limit, 'offset': offset, **kwargs}
        return self._make_request('GET', '/plans', params=params)
    
    def get_plan(self, plan_id: str) -> Dict:
        """Get a specific plan by ID"""
        return self._make_request('GET', f'/plans/{plan_id}')
    
    def create_plan(self, plan_data: Dict) -> Dict:
        """Create a new plan"""
        return self._make_request('POST', '/plans', data=plan_data)
    
    def update_plan(self, plan_id: str, plan_data: Dict) -> Dict:
        """Update an existing plan"""
        return self._make_request('PUT', f'/plans/{plan_id}', data=plan_data)
    
    def delete_plan(self, plan_id: str) -> Dict:
        """Delete a plan"""
        return self._make_request('DELETE', f'/plans/{plan_id}')
    
    # Tasks Management
    def get_tasks(self, limit: int = 100, offset: int = 0, **kwargs) -> List[Dict]:
        """Get all tasks"""
        params = {'limit': limit, 'offset': offset, **kwargs}
        return self._make_request('GET', '/tasks', params=params)
    
    def get_task(self, task_id: str) -> Dict:
        """Get a specific task by ID"""
        return self._make_request('GET', f'/tasks/{task_id}')
    
    def create_task(self, task_data: Dict) -> Dict:
        """Create a new task"""
        return self._make_request('POST', '/tasks', data=task_data)
    
    def update_task(self, task_id: str, task_data: Dict) -> Dict:
        """Update an existing task"""
        return self._make_request('PUT', f'/tasks/{task_id}', data=task_data)
    
    def delete_task(self, task_id: str) -> Dict:
        """Delete a task"""
        return self._make_request('DELETE', f'/tasks/{task_id}')
    
    def complete_task(self, task_id: str) -> Dict:
        """Mark a task as complete"""
        return self._make_request('PATCH', f'/tasks/{task_id}/complete')
    
    # Cases Management
    def get_cases(self, limit: int = 100, offset: int = 0, **kwargs) -> List[Dict]:
        """Get all cases"""
        params = {'limit': limit, 'offset': offset, **kwargs}
        return self._make_request('GET', '/cases', params=params)
    
    def get_case(self, case_id: str) -> Dict:
        """Get a specific case by ID"""
        return self._make_request('GET', f'/cases/{case_id}')
    
    def create_case(self, case_data: Dict) -> Dict:
        """Create a new case"""
        return self._make_request('POST', '/cases', data=case_data)
    
    def update_case(self, case_id: str, case_data: Dict) -> Dict:
        """Update an existing case"""
        return self._make_request('PUT', f'/cases/{case_id}', data=case_data)
    
    def delete_case(self, case_id: str) -> Dict:
        """Delete a case"""
        return self._make_request('DELETE', f'/cases/{case_id}')
    
    # Conversations Management
    def get_conversations(self, limit: int = 100, offset: int = 0, **kwargs) -> List[Dict]:
        """Get all conversations"""
        params = {'limit': limit, 'offset': offset, **kwargs}
        return self._make_request('GET', '/conversations', params=params)
    
    def get_conversation(self, conversation_id: str) -> Dict:
        """Get a specific conversation by ID"""
        return self._make_request('GET', f'/conversations/{conversation_id}')
    
    def create_conversation(self, conversation_data: Dict) -> Dict:
        """Create a new conversation"""
        return self._make_request('POST', '/conversations', data=conversation_data)
    
    def update_conversation(self, conversation_id: str, conversation_data: Dict) -> Dict:
        """Update an existing conversation"""
        return self._make_request('PUT', f'/conversations/{conversation_id}', data=conversation_data)
    
    def delete_conversation(self, conversation_id: str) -> Dict:
        """Delete a conversation"""
        return self._make_request('DELETE', f'/conversations/{conversation_id}')
    
    # Notes Management
    def get_notes(self, limit: int = 100, offset: int = 0, **kwargs) -> List[Dict]:
        """Get all notes"""
        params = {'limit': limit, 'offset': offset, **kwargs}
        return self._make_request('GET', '/notes', params=params)
    
    def get_note(self, note_id: str) -> Dict:
        """Get a specific note by ID"""
        return self._make_request('GET', f'/notes/{note_id}')
    
    def create_note(self, note_data: Dict) -> Dict:
        """Create a new note"""
        return self._make_request('POST', '/notes', data=note_data)
    
    def update_note(self, note_id: str, note_data: Dict) -> Dict:
        """Update an existing note"""
        return self._make_request('PUT', f'/notes/{note_id}', data=note_data)
    
    def delete_note(self, note_id: str) -> Dict:
        """Delete a note"""
        return self._make_request('DELETE', f'/notes/{note_id}')
    
    # Document Management
    def get_documents(self, limit: int = 100, offset: int = 0, **kwargs) -> List[Dict]:
        """Get all documents"""
        params = {'limit': limit, 'offset': offset, **kwargs}
        return self._make_request('GET', '/documents', params=params)
    
    def get_document(self, document_id: str) -> Dict:
        """Get a specific document by ID"""
        return self._make_request('GET', f'/documents/{document_id}')
    
    def create_document(self, document_data: Dict) -> Dict:
        """Create a new document"""
        return self._make_request('POST', '/documents', data=document_data)
    
    def update_document(self, document_id: str, document_data: Dict) -> Dict:
        """Update an existing document"""
        return self._make_request('PUT', f'/documents/{document_id}', data=document_data)
    
    def delete_document(self, document_id: str) -> Dict:
        """Delete a document"""
        return self._make_request('DELETE', f'/documents/{document_id}')
    
    # Automation Management
    def get_automation_blueprints(self, limit: int = 100, offset: int = 0, **kwargs) -> List[Dict]:
        """Get all automation blueprints"""
        params = {'limit': limit, 'offset': offset, **kwargs}
        return self._make_request('GET', '/automation-blueprints', params=params)
    
    def get_automation_blueprint(self, blueprint_id: str) -> Dict:
        """Get a specific automation blueprint by ID"""
        return self._make_request('GET', f'/automation-blueprints/{blueprint_id}')
    
    def create_automation_blueprint(self, blueprint_data: Dict) -> Dict:
        """Create a new automation blueprint"""
        return self._make_request('POST', '/automation-blueprints', data=blueprint_data)
    
    def trigger_automation(self, blueprint_id: str, trigger_data: Dict = None) -> Dict:
        """Trigger an automation blueprint"""
        return self._make_request('POST', f'/automation-blueprints/{blueprint_id}/trigger', data=trigger_data or {})
    
    # Form Builder
    def get_forms(self, limit: int = 100, offset: int = 0, **kwargs) -> List[Dict]:
        """Get all forms"""
        params = {'limit': limit, 'offset': offset, **kwargs}
        return self._make_request('GET', '/forms', params=params)
    
    def get_form(self, form_id: str) -> Dict:
        """Get a specific form by ID"""
        return self._make_request('GET', f'/forms/{form_id}')
    
    def create_form(self, form_data: Dict) -> Dict:
        """Create a new form"""
        return self._make_request('POST', '/forms', data=form_data)
    
    def get_form_submissions(self, form_id: str, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Get submissions for a specific form"""
        params = {'limit': limit, 'offset': offset}
        return self._make_request('GET', f'/forms/{form_id}/submissions', params=params)
    
    # Utility Methods
    def get_firm_info(self) -> Dict:
        """Get current firm information"""
        return self._make_request('GET', '/firms/current')
    
    def get_employees(self, limit: int = 100, offset: int = 0, **kwargs) -> List[Dict]:
        """Get all employees"""
        params = {'limit': limit, 'offset': offset, **kwargs}
        return self._make_request('GET', '/employees', params=params)
    
    def search(self, query: str, model_type: str = None, limit: int = 100) -> List[Dict]:
        """
        Search across Plannr data
        
        Args:
            query (str): Search query
            model_type (str, optional): Specific model type to search
            limit (int): Maximum results to return
            
        Returns:
            List[Dict]: Search results
        """
        params = {'q': query, 'limit': limit}
        if model_type:
            params['type'] = model_type
        return self._make_request('GET', '/search', params=params)
    
    def get_api_usage(self) -> Dict:
        """Get current API usage statistics"""
        return self._make_request('GET', '/api/usage')


# Example usage and helper functions
def create_client_from_env() -> PlannrClient:
    """
    Create a Plannr client using environment variables
    
    Environment variables:
    - PLANNR_API_TOKEN: Your Plannr API token
    - PLANNR_BASE_URL: Base URL (optional, defaults to https://api.plannrcrm.com)
    
    Returns:
        PlannrClient: Configured client instance
    """
    import os
    
    api_token = os.getenv('PLANNR_API_TOKEN')
    if not api_token:
        raise ValueError("PLANNR_API_TOKEN environment variable is required")
    
    base_url = os.getenv('PLANNR_BASE_URL', 'https://api.plannrcrm.com')
    
    return PlannrClient(api_token=api_token, base_url=base_url)


def example_usage():
    """
    Example usage of the Plannr API client
    """
    # Initialize client (replace with your actual API token)
    client = PlannrClient(api_token="your-api-token-here")
    
    try:
        # Get firm information
        firm_info = client.get_firm_info()
        print(f"Connected to firm: {firm_info.get('name', 'Unknown')}")
        
        # Get all accounts
        accounts = client.get_accounts(limit=10)
        print(f"Found {len(accounts)} accounts")
        
        # Create a new account
        new_account = {
            "name": "Example Client",
            "email": "client@example.com",
            "phone": "+1234567890",
            "custom": {
                "industry": "Technology",
                "priority": "High"
            }
        }
        created_account = client.create_account(new_account)
        print(f"Created account: {created_account['_id']}")
        
        # Create a task for the account
        new_task = {
            "title": "Welcome Call",
            "description": "Initial welcome call with new client",
            "accountId": created_account['_id'],
            "dueDate": "2025-01-15T10:00:00.000Z",
            "status": "pending"
        }
        created_task = client.create_task(new_task)
        print(f"Created task: {created_task['_id']}")
        
        # Search for accounts
        search_results = client.search("Example", model_type="Account")
        print(f"Search found {len(search_results)} results")
        
    except PlannrAPIError as e:
        print(f"API Error: {e.message}")
        if e.response_data:
            print(f"Response data: {e.response_data}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    # Run example usage
    example_usage()