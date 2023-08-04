import sys
import re
import json
import subprocess

# Check if the correct number of arguments are provided
if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "<ha_public_url>")
    sys.exit(1)

# Store the new URL provided as argument
ha_public_url = sys.argv[1]

# Check if the new URL contains "https://" prefix
if ha_public_url.startswith("http") :
    print("Error: Please provide your Home Assitant public URL without 'https://' prefix.")
    sys.exit(1)

# Add "https://" prefix to the new URL
ha_public_url = "https://" + ha_public_url

def prepare_account_linkking(ha_public_url):
  # Set the file paths
  input_file = "account_linking_request_template.json"
  output_file = "account_linking_request.json"

  try:
      # Read the content of the input file
      with open(input_file, 'r') as file:
          content = file.read()

      # Use regex to replace the string "[YOUR_HA_URL]" with the new URL
      updated_content = re.sub(r'\[YOUR_HA_URL\]', ha_public_url, content)
      return updated_content

  except FileNotFoundError:
      print(f"Error: File '{input_file}' not found.")
      sys.exit(1)
  except IOError as e:
      print(f"Error: Unable to read or write to the files - {e}")
      sys.exit(1)

def get_skill_id():
  # Set the file path
  json_file = ".ask/ask-states.json"

  try:
      # Read the JSON data from the file
      with open(json_file) as file:
          data = json.load(file)

      # Extract the skillId value
      skill_id = data.get("profiles", {}).get("default", {}).get("skillId")

      # Check if the skillId is not empty
      if skill_id is None:
          print("Error: Failed to extract skillId from the JSON file.")
      else:
          print("The extracted skillId is:", skill_id)
          return skill_id

  except FileNotFoundError:
      print(f"Error: File '{json_file}' not found.")
  except json.JSONDecodeError:
      print(f"Error: Invalid JSON format in '{json_file}'.")

def update_account_linking_info(skill_id, account_linking_request):
    command = [
        'ask',
        'smapi',
        'update-account-linking-info',
        '-g',
        'development',
        '--skill-id',
        skill_id,
        '--account-linking-request',
        account_linking_request
    ]
    print(command)

    try:
        # Run the command using subprocess
        subprocess.run(command, check=True)
        print("Account linking info updated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing the command: {e}")
        # Handle any errors or exceptions if necessary

updated_content = prepare_account_linkking(ha_public_url)
skill_id = get_skill_id()

update_account_linking_info(skill_id, updated_content)
