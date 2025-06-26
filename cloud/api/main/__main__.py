# __main__.py - Client for connecting to the Raspberry Pi API

import requests
import time
from typing import Dict, Any, Optional, List

class PiApiClient:
    """Client for interacting with the Raspberry Pi API."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize the Pi API client.

        Args:
            base_url: Base URL of the Pi API, including protocol and port
        """
        self.base_url = base_url

    def health_check(self) -> Dict[str, str]:
        """Check if the Pi API is healthy."""
        response = requests.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()

    def pump_on(self, name: str) -> Dict[str, Any]:
        """
        Turn on a pump.

        Args:
            name: Name of the pump to turn on

        Returns:
            Response from the API
        """
        response = requests.post(f"{self.base_url}/pump/{name}/on")
        response.raise_for_status()
        return response.json()

    def pump_off(self, name: str) -> Dict[str, Any]:
        """
        Turn off a pump.

        Args:
            name: Name of the pump to turn off

        Returns:
            Response from the API
        """
        response = requests.post(f"{self.base_url}/pump/{name}/off")
        response.raise_for_status()
        return response.json()

def test_pi_api_connection(pi_api_url: str = "http://localhost:8000") -> None:
    """
    Test connection to the Pi API.

    Args:
        pi_api_url: URL of the Pi API
    """
    client = PiApiClient(pi_api_url)

    # Test health check
    try:
        health_response = client.health_check()
        print(f"Health check successful: {health_response}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return

    # List of available pumps (from pump_config.py)
    available_pumps = [
        "calcium_nitrate", "magnesium_sulfate", "micronutrients",
        "ph_down", "ph_up", "potassium", "flush_1", "flush_2",
        "fill_1", "fill_2"
    ]

    # Test turning on and off a pump (using the first available pump)
    test_pump = available_pumps[0]
    try:
        # Turn on pump
        on_response = client.pump_on(test_pump)
        print(f"Turned on {test_pump}: {on_response}")

        # Wait a moment
        time.sleep(2)

        # Turn off pump
        off_response = client.pump_off(test_pump)
        print(f"Turned off {test_pump}: {off_response}")

        print("Pi API connection test completed successfully!")
    except Exception as e:
        print(f"Pump control test failed: {e}")

if __name__ == "__main__":
    # Replace with the actual IP address of your Raspberry Pi
    pi_ip = "localhost"  # Change this to your Pi's IP address
    pi_port = 8000

    test_pi_api_connection(f"http://{pi_ip}:{pi_port}")
