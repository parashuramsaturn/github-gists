# Plannr CRM Client Creator

This repository contains scripts to automatically create 100 clients in Plannr CRM with the following specifications:

- **Total clients**: 100
- **Advisor**: parashuram joshi  
- **Status distribution**: Evenly split across active, deceased, archived, inactive (25 each)
- **Data**: Realistic client information with random names, addresses, financial details, etc.

## Files Included

1. `create_plannr_clients.py` - Full-featured version with Faker library for realistic data
2. `create_plannr_clients_simple.py` - Simple version using only built-in Python libraries  
3. `requirements.txt` - Dependencies for the full-featured version
4. `README.md` - This file with instructions

## Prerequisites

### For Simple Version (Recommended)
- Python 3.6 or higher
- Your Plannr CRM API key

### For Full-Featured Version  
- Python 3.6 or higher
- Your Plannr CRM API key
- External dependencies (install with: `pip install -r requirements.txt`)

## Setup Instructions

### 1. Get Your API Key

1. Log into your Plannr CRM account
2. Navigate to Settings → API or Developer section
3. Generate or copy your API key
4. Keep this key secure and private

### 2. Choose Your Script Version

**Option A: Simple Version (Recommended)**
- Uses only built-in Python libraries
- No additional installations required
- Still generates realistic client data

**Option B: Full-Featured Version**
- Uses Faker library for more realistic data generation
- Requires installing dependencies: `pip install -r requirements.txt`

### 3. Configure the Script

Edit your chosen script file and update these variables:

```python
API_KEY = "YOUR_PLANNR_CRM_API_KEY"  # Replace with your actual API key
BASE_URL = "https://apidocs.plannrcrm.com"  # Update if your CRM uses a different URL
CLIENT_COUNT = 100  # Number of clients to create
```

**Important**: Replace `"YOUR_PLANNR_CRM_API_KEY"` with your actual API key from Plannr CRM.

## Usage

### Running the Simple Version

```bash
python create_plannr_clients_simple.py
```

### Running the Full-Featured Version

```bash
# First install dependencies
pip install -r requirements.txt

# Then run the script
python create_plannr_clients.py
```

## What the Script Does

1. **Generates realistic client data** including:
   - Names, emails, phone numbers
   - Addresses across major US cities
   - Birth dates, occupations, companies
   - Financial information (income, net worth)
   - Investment goals and risk tolerance
   - Contact preferences and notes

2. **Distributes statuses evenly**:
   - Active: 25 clients
   - Deceased: 25 clients  
   - Archived: 25 clients
   - Inactive: 25 clients

3. **Assigns advisor**: All clients are assigned to "parashuram joshi"

4. **Creates clients via API**: Makes HTTP POST requests to the Plannr CRM API

5. **Provides progress tracking**: Shows real-time progress and success/failure rates

6. **Exports results**: Saves detailed results to `client_creation_results.json`

## Output

The script will:
- Display progress in the terminal as it creates each client
- Show a summary at the end with success/failure statistics
- Create a JSON file with detailed results for each client creation attempt

### Example Output

```
Creating 100 clients with advisor 'parashuram joshi'
Status distribution: {'active': 25, 'deceased': 25, 'archived': 25, 'inactive': 25}
------------------------------------------------------------
Creating client 1/100 with status: active
✅ Successfully created: John Smith
Creating client 2/100 with status: inactive
✅ Successfully created: Sarah Johnson
...
Progress: 10/100 clients processed
Success: 10, Failed: 0
------------------------------
...
============================================================
SUMMARY
============================================================
Total clients processed: 100
Successfully created: 98
Failed: 2
Success rate: 98.0%

Status Distribution:
  Active: 25
  Deceased: 25
  Archived: 25
  Inactive: 25

Results exported to: client_creation_results.json
```

## Error Handling

The script includes comprehensive error handling:

- **Invalid API key**: Clear error message if API key is not updated
- **Network errors**: Handles connection issues and timeouts
- **API errors**: Captures and displays HTTP error codes and messages
- **Rate limiting**: Includes small delays between requests
- **Detailed logging**: All attempts are logged to the results file

## Customization

You can easily customize the script by modifying:

- **CLIENT_COUNT**: Change the number of clients to create
- **Status distribution**: Modify the `statuses` list or distribution logic
- **Client data fields**: Add/remove fields in the `generate_client_data()` method
- **Base URL**: Update if your CRM uses a different API endpoint
- **Delay between requests**: Adjust `time.sleep()` value for rate limiting

## Troubleshooting

### Common Issues

1. **"Invalid API key" errors**
   - Verify your API key is correct
   - Check that the key has permission to create clients
   - Ensure the key is not expired

2. **"Connection refused" errors**  
   - Verify the BASE_URL is correct
   - Check your internet connection
   - Confirm the Plannr CRM API is accessible

3. **Rate limiting errors**
   - Increase the delay between requests (`time.sleep()` value)
   - Consider creating clients in smaller batches

4. **Field validation errors**
   - Check if required fields are missing
   - Verify field formats match API expectations
   - Review the API documentation for field requirements

### Getting Help

1. Check the `client_creation_results.json` file for detailed error information
2. Review the Plannr CRM API documentation
3. Contact Plannr CRM support for API-specific issues
4. Verify your account has appropriate permissions for client creation

## Security Notes

- **Never commit your API key** to version control
- Store API keys securely (consider environment variables)
- Limit API key permissions to only what's needed
- Regularly rotate API keys for security

## API Structure Assumptions

This script is based on common CRM API patterns. The actual Plannr CRM API might use different:
- Field names (firstName vs first_name)
- Authentication methods  
- Request/response formats
- Required fields

If you encounter field-related errors, you may need to adjust the client data structure to match your CRM's specific API requirements.

## License

This script is provided as-is for educational and practical purposes. Please ensure compliance with your Plannr CRM terms of service when using automated client creation.
