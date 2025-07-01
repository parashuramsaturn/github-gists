# Plannr CRM API Client

A comprehensive Python client for interacting with the Plannr CRM API. This client provides a simple and intuitive interface to access all major Plannr CRM endpoints.

## Features

- **Full API Coverage**: Support for all major Plannr CRM endpoints (Accounts, Plans, Tasks, Cases, etc.)
- **Authentication**: Bearer token authentication with proper header management
- **Error Handling**: Comprehensive error handling with custom exceptions
- **Rate Limiting**: Built-in rate limiting to respect API limits (200 requests/minute)
- **Bulk Operations**: Support for bulk create/update operations (up to 5000 records)
- **Custom Fields**: Full support for custom field management
- **Type Safety**: Type hints for better IDE support and code quality
- **Logging**: Built-in logging for debugging and monitoring

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Set your API token as an environment variable:
```bash
export PLANNR_API_TOKEN="your-api-token-here"
```

## Quick Start

### Basic Usage

```python
from plannr_client import PlannrClient, PlannrAPIError

# Initialize the client
client = PlannrClient(api_token="your-api-token-here")

try:
    # Get firm information
    firm_info = client.get_firm_info()
    print(f"Connected to: {firm_info['name']}")
    
    # List accounts
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
    
except PlannrAPIError as e:
    print(f"API Error: {e.message}")
```

### Using Environment Variables

```python
from plannr_client import create_client_from_env

# Create client from environment variables
client = create_client_from_env()  # Uses PLANNR_API_TOKEN env var
```

## API Coverage

### Account Management
- `get_accounts()` - List all accounts
- `get_account(account_id)` - Get specific account
- `create_account(account_data)` - Create new account
- `update_account(account_id, account_data)` - Update account
- `delete_account(account_id)` - Delete account
- `bulk_upsert_accounts(accounts_data)` - Bulk create/update accounts

### Plans Management
- `get_plans()` - List all plans
- `get_plan(plan_id)` - Get specific plan
- `create_plan(plan_data)` - Create new plan
- `update_plan(plan_id, plan_data)` - Update plan
- `delete_plan(plan_id)` - Delete plan

### Tasks Management
- `get_tasks()` - List all tasks
- `get_task(task_id)` - Get specific task
- `create_task(task_data)` - Create new task
- `update_task(task_id, task_data)` - Update task
- `delete_task(task_id)` - Delete task
- `complete_task(task_id)` - Mark task as complete

### Cases Management
- `get_cases()` - List all cases
- `get_case(case_id)` - Get specific case
- `create_case(case_data)` - Create new case
- `update_case(case_id, case_data)` - Update case
- `delete_case(case_id)` - Delete case

### Conversations Management
- `get_conversations()` - List all conversations
- `get_conversation(conversation_id)` - Get specific conversation
- `create_conversation(conversation_data)` - Create new conversation
- `update_conversation(conversation_id, conversation_data)` - Update conversation
- `delete_conversation(conversation_id)` - Delete conversation

### Notes Management
- `get_notes()` - List all notes
- `get_note(note_id)` - Get specific note
- `create_note(note_data)` - Create new note
- `update_note(note_id, note_data)` - Update note
- `delete_note(note_id)` - Delete note

### Document Management
- `get_documents()` - List all documents
- `get_document(document_id)` - Get specific document
- `create_document(document_data)` - Create new document
- `update_document(document_id, document_data)` - Update document
- `delete_document(document_id)` - Delete document

### Automation Management
- `get_automation_blueprints()` - List automation blueprints
- `get_automation_blueprint(blueprint_id)` - Get specific blueprint
- `create_automation_blueprint(blueprint_data)` - Create new blueprint
- `trigger_automation(blueprint_id, trigger_data)` - Trigger automation

### Form Builder
- `get_forms()` - List all forms
- `get_form(form_id)` - Get specific form
- `create_form(form_data)` - Create new form
- `get_form_submissions(form_id)` - Get form submissions

### Utility Methods
- `get_firm_info()` - Get current firm information
- `get_employees()` - List all employees
- `search(query, model_type)` - Search across data
- `get_api_usage()` - Get API usage statistics

## Advanced Usage

### Bulk Operations

```python
# Bulk create/update accounts
bulk_accounts = [
    {
        "name": "Client 1",
        "email": "client1@example.com",
        "externalId": "ext-001"
    },
    {
        "name": "Client 2", 
        "email": "client2@example.com",
        "externalId": "ext-002"
    }
]

result = client.bulk_upsert_accounts(bulk_accounts)
print(f"Created: {result['created']}, Updated: {result['updated']}")
```

### Custom Fields

```python
# Create account with custom fields
account_data = {
    "name": "Custom Client",
    "email": "custom@example.com",
    "custom": {
        "industry": "Healthcare",
        "annual_revenue": 1000000,
        "priority_level": "High",
        "tags": ["VIP", "Enterprise"]
    }
}

account = client.create_account(account_data)
```

### Search Functionality

```python
# Search for accounts
results = client.search("Healthcare", model_type="Account", limit=10)
for result in results:
    print(f"Found: {result['name']}")
```

### Error Handling

```python
try:
    account = client.get_account("invalid-id")
except PlannrAPIError as e:
    if e.status_code == 404:
        print("Account not found")
    elif e.status_code == 403:
        print("Permission denied")
    else:
        print(f"API Error: {e.message}")
        if e.response_data:
            print(f"Details: {e.response_data}")
```

## Configuration

### Environment Variables

- `PLANNR_API_TOKEN` - Your Plannr API access token (required)
- `PLANNR_BASE_URL` - Base URL for API (optional, defaults to https://api.plannrcrm.com)

### Rate Limiting

The client automatically handles rate limiting to stay within Plannr's API limits:
- 200 requests per minute (soft limit)
- 150 requests per second with bursts up to 50 parallel requests (hard limit)

### Logging

Enable debug logging to see API requests:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Examples

See `example_usage.py` for comprehensive examples including:
- Basic CRUD operations
- Bulk operations
- Error handling
- Search functionality
- Custom fields usage

Run the example:
```bash
python example_usage.py
```

## API Documentation

This client is based on the official Plannr API documentation:
- **API Docs**: https://apidocs.plannrcrm.com/
- **Base URL**: https://api.plannrcrm.com
- **Authentication**: Bearer token

## Error Handling

The client provides comprehensive error handling:

- `PlannrAPIError` - Custom exception for API errors
- Status code specific handling (400, 403, 500, etc.)
- Detailed error messages and response data
- Automatic retry logic for rate limiting

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is provided as-is for integration with Plannr CRM. Please refer to Plannr's terms of service for API usage guidelines.

## Support

For API-related questions:
- Check the [Plannr API Documentation](https://apidocs.plannrcrm.com/)
- Contact Plannr support through their official channels

For client-specific issues:
- Check the example usage
- Review error messages and status codes
- Enable debug logging for detailed request information