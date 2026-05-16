import random
import string
from locust import HttpUser, task, between

def random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

class TelemetryUser(HttpUser):
    wait_time = between(1, 5)
    
    def on_start(self):
        # Create a user
        self.username = f"user_{random.randint(1, 10000)}_{random_string(5)}"
        self.password = "securepassword"
        self.token = None
        self.user_id = None
        self.device_id = None
        
        # 1. Register
        register_response = self.client.post("/users/", json={
            "username": self.username,
            "password": self.password
        })
        
        if register_response.status_code == 200:
            self.user_id = register_response.json()["id"]
            
            # 2. Login to get token
            login_response = self.client.post("/users/login", data={
                "username": self.username,
                "password": self.password
            })
            
            if login_response.status_code == 200:
                self.token = login_response.json()["access_token"]
                self.headers = {"Authorization": f"Bearer {self.token}"}
                
                # 3. Create a device
                device_response = self.client.post(
                    "/devices/", 
                    json={"user_id": self.user_id},
                    headers=self.headers
                )
                if device_response.status_code == 200:
                    self.device_id = device_response.json()["id"]

    @task(3)
    def send_telemetry(self):
        if self.device_id and self.token:
            self.client.post(f"/telemetry/{self.device_id}", json={
                "x": random.uniform(-100, 100),
                "y": random.uniform(-100, 100),
                "z": random.uniform(-100, 100)
            }, headers=self.headers)

    @task(1)
    def trigger_analysis(self):
        if self.device_id and self.token:
            self.client.post(f"/analytics/device/{self.device_id}", json={}, headers=self.headers)

    @task(1)
    def check_root(self):
        self.client.get("/")
