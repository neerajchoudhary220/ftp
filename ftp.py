import os
import json
from ftplib import FTP

def read_json(json_file_path):
    """Reads a JSON file and returns its content."""
    try:
        with open(json_file_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Failed to read JSON file {json_file_path}: {e}")
        return None

def get_remote_file_path(remote_directory, local_file_path):
    """Generates the remote file path on the FTP server."""
    return os.path.join(remote_directory, os.path.basename(local_file_path))

def upload_file_to_ftp(ftp, local_file_path, remote_file_path):
    """Uploads a file to the FTP server."""
    try:
        with open(local_file_path, 'rb') as file:
            ftp.storbinary(f'STOR {remote_file_path}', file)
        print(f"Uploaded: {local_file_path} to {remote_file_path}")
    except Exception as e:
        print(f"Failed to upload {local_file_path}: {e}")

def main():
    # Read configuration from JSON file
    ftp_config = read_json('./files/ftp.json')
    if ftp_config is None:
        return  # Exit if configuration is not available

    # Extract FTP server details and root paths
    credentials = ftp_config.get('ftp_credentials', {})
    host = credentials.get('host')
    username = credentials.get('username')
    password = credentials.get('password')

    root_paths = ftp_config.get('root_paths', {})
    local_root_path = root_paths.get('local', '')
    remote_root_path = root_paths.get('remote', '')

    # List of files to upload
    files = read_json('./files/files.json')
    uploading_files = files.get('files')

    # Connect to the FTP server
    try:
        with FTP(host) as ftp:
            ftp.login(user=username, passwd=password)
            print(f"Connected to FTP server: {host}")

            # Upload each file
            for file_info in uploading_files:
                # Construct local and remote paths
                local_file_path = os.path.join(local_root_path, file_info['path'], file_info['fileName'])
                remote_directory = os.path.join(remote_root_path, file_info['path'])
             
                remote_file_path = get_remote_file_path(remote_directory, local_file_path)
                
                #Check if the local file exists before uploading
                if os.path.exists(local_file_path):
                    upload_file_to_ftp(ftp, local_file_path, remote_file_path)
                else:
                    print(f"File does not exist: {local_file_path}")

            print("File upload process completed.")
    except Exception as e:
        print(f"Failed to connect to FTP server {host}: {e}")

if __name__ == '__main__':
    main()
