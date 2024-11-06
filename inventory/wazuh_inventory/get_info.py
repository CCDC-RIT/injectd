# Unfinished and untested proof of concept.
# Acquires a list of information from the Wazuh manager that is then visualized by another script.

#pip install requests
import requests
import json

def get_agents_method2(wazuh_url,api_user,api_password,use_ssl=True):
    # Disable warnings for insecure SSL requests (optional, we may not have valid certs)
    if not use_ssl:
        requests.packages.urllib3.disable_warnings()

    # API endpoint to get agents
    endpoint = '/agents'

    # Prepare the request URL
    url = f"{wazuh_url}{endpoint}"

    # Make the request to get connected agents
    response = requests.get(url, auth=(api_user, api_password), verify=False) # TODO what does verify mean?

    # Check if the request was successful
    if response.status_code == 200:
        # Parse JSON response
        agents_data = json.loads(response.text)
        # Filter out disconnected agents
        connected_agents = [agent for agent in agents_data['data']['affected_items'] if agent['status'] == 'active']
        # Return/Print the list of connected agents
        #print(f"Connected Agents: {connected_agents}")
        return connected_agents
    else:
        print(f"Failed to retrieve agents. Status code: {response.status_code}, Response: {response.text}")

def wazuh_api_request(method, endpoint, data=None):
    """
    Function to make requests to the Wazuh API.
    # Example usage:
    agents = wazuh_api_request("GET", "/agents")
    print(agents)
    """

    base_url = "https://localhost:55000"  # Replace with your Wazuh API URL
    headers = {
        "Authorization": f"Bearer {get_wazuh_token()}",  # Replace with your token retrieval function
        "Content-Type": "application/json"
    }

    url = f"{base_url}{endpoint}"

    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "POST":
        response = requests.post(url, headers=headers, data=json.dumps(data))
    elif method == "PUT":
        response = requests.put(url, headers=headers, data=json.dumps(data))
    elif method == "DELETE":
        response = requests.delete(url, headers=headers)
    else:
        raise ValueError("Invalid HTTP method")

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API request failed with status code {response.status_code}")

def get_wazuh_token():
    """
    Function to get a Wazuh API token. 
    Replace this with your actual token retrieval logic.
    """
    # Example using basic auth
    username = "your_username"
    password = "your_password"
    auth_data = {
        "user": username,
        "password": password
    }
    response = requests.post("https://localhost:55000/security/user/authenticate", data=json.dumps(auth_data))
    if response.status_code == 200:
        return response.json()["token"]
    else:
        raise Exception("Token retrieval failed")

def main():
    connected_agents = get_agents_method2("https://localhost:55000","user1","pwd1",True)
    print(f"Connected Agents: {connected_agents}")

    agents = wazuh_api_request("GET", "/agents")
    print(agents)

main()