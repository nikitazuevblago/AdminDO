import os
from dotenv import load_dotenv
import digitalocean
from typing import Optional, List
import paramiko
import time

class DropletManager:
    def __init__(self):
        load_dotenv()
        self.token = os.getenv("DO_TOKEN")
        if not self.token:
            raise ValueError("No DO_TOKEN found in .env file")
        self.manager = digitalocean.Manager(token=self.token)
        self.ssh_password = "4Coding4bttrlife"
        self.ssh_user = os.getenv("SSH_USER", "root")

    def get_all_droplets(self) -> List[digitalocean.Droplet]:
        """Get all droplets in your account"""
        return self.manager.get_all_droplets()

    def get_droplet_by_name(self, name: str) -> Optional[digitalocean.Droplet]:
        """Get a specific droplet by name"""
        droplets = self.get_all_droplets()
        for droplet in droplets:
            if droplet.name == name:
                return droplet
        return None

    def get_droplet_status(self, name: str) -> dict:
        """Get status of a specific droplet"""
        droplet = self.get_droplet_by_name(name)
        if not droplet:
            return {"error": f"Droplet {name} not found"}
        
        return {
            "name": droplet.name,
            "status": droplet.status,
            "ip_address": droplet.ip_address,
            "region": droplet.region["name"],
            "size": droplet.size_slug,
            "created_at": droplet.created_at
        }

    def power_action(self, name: str, action: str) -> dict:
        """Perform power action on droplet (power_on, power_off, reboot)"""
        droplet = self.get_droplet_by_name(name)
        if not droplet:
            return {"error": f"Droplet {name} not found"}
        
        try:
            if action == "power_on":
                droplet.power_on()
            elif action == "power_off":
                droplet.power_off()
            elif action == "reboot":
                droplet.reboot()
            else:
                return {"error": "Invalid action. Use power_on, power_off, or reboot"}
            
            return {"success": f"{action} action initiated on {name}"}
        except Exception as e:
            return {"error": str(e)}

    def execute_command(self, droplet_name: str, command: str) -> dict:
        """Execute a command on the droplet via SSH"""
        droplet = self.get_droplet_by_name(droplet_name)
        if not droplet:
            return {"error": f"Droplet {droplet_name} not found"}

        try:
            # Create SSH client
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Connect to the droplet using password
            try:
                ssh.connect(
                    droplet.ip_address,
                    username=self.ssh_user,
                    password=self.ssh_password,
                    timeout=10
                )
            except Exception as e:
                return {"error": f"Failed to connect: {str(e)}"}

            # Execute command
            stdin, stdout, stderr = ssh.exec_command(command)
            
            # Get output
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()

            # Close connection
            ssh.close()

            if error:
                return {"error": error}
            return {"output": output}

        except Exception as e:
            return {"error": f"Command execution failed: {str(e)}"}

# Example usage
if __name__ == "__main__":
    try:
        manager = DropletManager()
        
        # List all droplets
        print("\nAll Droplets:")
        droplets = manager.get_all_droplets()
        for droplet in droplets:
            print(f"- {droplet.name} ({droplet.ip_address})")
        
        # Get specific droplet status
        if droplets:
            first_droplet = droplets[0].name
            print(f"\nStatus of {first_droplet}:")
            status = manager.get_droplet_status(first_droplet)
            for key, value in status.items():
                print(f"{key}: {value}")
    
    except Exception as e:
        print(f"Error: {e}") 