#!/usr/bin/env python3
"""
Configuration Template for Plannr CRM Client Creator

Copy this file to 'config.py' and update with your actual values.
Then import these values in your main script.

IMPORTANT: 
- Never commit config.py with real API keys to version control
- Add config.py to your .gitignore file
"""

# ==========================================
# REQUIRED CONFIGURATION
# ==========================================

# Your Plannr CRM API Key
# Find this in: Plannr CRM → Settings → API/Developer Section
API_KEY = "your_actual_plannr_crm_api_key_here"

# Plannr CRM API Base URL
# Update this if your CRM instance uses a different URL
BASE_URL = "https://apidocs.plannrcrm.com"

# ==========================================
# CLIENT CREATION SETTINGS
# ==========================================

# Number of clients to create
CLIENT_COUNT = 100

# Advisor name to assign to all clients
ADVISOR_NAME = "parashuram joshi"

# Client status options (will be distributed evenly)
CLIENT_STATUSES = ["active", "deceased", "archived", "inactive"]

# ==========================================
# API SETTINGS
# ==========================================

# Delay between API requests (seconds) - helps avoid rate limiting
REQUEST_DELAY = 0.1

# Maximum number of retries for failed requests
MAX_RETRIES = 3

# Timeout for API requests (seconds)
REQUEST_TIMEOUT = 30

# ==========================================
# OUTPUT SETTINGS
# ==========================================

# Filename for results export
RESULTS_FILE = "client_creation_results.json"

# Enable detailed logging
VERBOSE_LOGGING = True

# Progress update frequency (show progress every N clients)
PROGRESS_UPDATE_FREQUENCY = 10

# ==========================================
# ALTERNATIVE API ENDPOINTS (if different)
# ==========================================

# Uncomment and modify if your Plannr CRM uses different endpoints
# CREATE_CLIENT_ENDPOINT = "/api/v1/clients"  # Alternative endpoint
# AUTH_HEADER_PREFIX = "Bearer"               # Alternative: "Token", "API-Key", etc.
# CONTENT_TYPE = "application/json"           # Alternative: "application/x-www-form-urlencoded"

# ==========================================
# EXAMPLE USAGE IN MAIN SCRIPT
# ==========================================
"""
To use this configuration in your main script:

from config import (
    API_KEY, 
    BASE_URL, 
    CLIENT_COUNT, 
    ADVISOR_NAME, 
    CLIENT_STATUSES,
    REQUEST_DELAY
)

# Then use these variables instead of hardcoded values
crm_client = PlannrCRMClient(api_key=API_KEY, base_url=BASE_URL)
"""