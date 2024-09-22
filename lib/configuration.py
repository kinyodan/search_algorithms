
import configparser
import os
import json
import ssl
from typing import Any, Dict


def get_config_path(filename: str) -> str:
    """Get the full path to the configuration file.

    Args:
        filename (str): Name of the configuration file.

    Returns:
        str: Full path to the configuration file.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, filename)


def read_config(config_file: str) -> Dict[str, Any]:
    """Read the configuration file and fetch settings.

    Args:
        config_file (str): Path to the configuration file.

    Returns:
        Dict[str, Any]: Dictionary containing the configuration settings.
    """
    config = configparser.ConfigParser()
    config.read(config_file)

    settings: Dict[str, Any] = {
        'file_path': None,
        'use_ssl': False,
        'ssl_certfile': None,
        'ssl_keyfile': None,
        'ssl_psk_keyfile': None,
        'reread_on_query_config': None,
        'metrics_json_path': None
        
    }

    for section in config.sections():
        settings['file_path'] = config.get(section, 'linuxpath', fallback=settings['file_path'])
        settings['use_ssl'] = config.getboolean(section, 'use_ssl', fallback=settings['use_ssl'])
        settings['ssl_certfile'] = config.get(section, 'ssl_certfile', fallback=settings['ssl_certfile'])
        settings['ssl_keyfile'] = config.get(section, 'ssl_keyfile', fallback=settings['ssl_keyfile'])
        settings['ssl_psk_keyfile'] = config.get(section, 'ssl_psk_keyfile', fallback=settings['ssl_psk_keyfile'])
        settings['reread_on_query_config'] = config.get(section, 'reread_on_query_config', fallback=settings['reread_on_query_config'])
        settings['metrics_json_path'] = config.get(section, 'metrics_json_path', fallback=settings['metrics_json_path'])

    return settings


def load_reread_on_query_config(config_file_path: str, data_file_path: str) -> bool:
    """
    Load or update the 'reread_on_query' configuration from a specified config file.
    
    Parameters:
    config_file_path (str): The path to the configuration file.
    data_file_path (str): The path to the data file.
    
    Returns:
    bool: The status of 'reread_on_query'. Defaults to True if not found.
    """
    file_name = get_file_name_without_extension(data_file_path)

    try:
        # Open the config file for reading and writing
        with open(config_file_path, 'r+') as f:
            # Load the JSON data
            data = json.load(f)

            # Check if the file_name exists in "files"
            if file_name in data.get("files", {}):
                return data["files"][file_name]["reread_on_query"]
            else:
                # Create the new configuration if it doesn't exist
                new_config = {"file_path": data_file_path, "reread_on_query": True}
                data.setdefault("files", {})[file_name] = new_config

                # Write the updated data to the file
                f.seek(0)  # Move to the beginning of the file
                json.dump(data, f, indent=4)
                f.truncate()  # Remove any old content beyond the new data

                return new_config["reread_on_query"]

    except FileNotFoundError:
        # If config file doesn't exist, create it with initial structure
        new_config = {
            "files": {
                file_name: {
                    "file_path": data_file_path,
                    "reread_on_query": True
                }
            }
        }
        with open(config_file_path, 'w') as f:
            json.dump(new_config, f, indent=4)
        return True  # Default value if the file is created

    except json.JSONDecodeError:
        # Handle the case where the JSON is malformed
        print(f"Error: The file {config_file_path} is not a valid JSON.")
        raise

    except Exception as e:
        # Catch any other unexpected errors
        print(f"An unexpected error occurred: {e}")
        raise


def get_file_name_without_extension(file_path: str) -> str:
    """
    Extract the file name without its extension from the given file path.

    Parameters:
    file_path (str): The full path to the file.

    Returns:
    str: The file name without the extension.
    """
    return os.path.splitext(os.path.basename(file_path))[0]

