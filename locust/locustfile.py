from locust import HttpUser, task, between, constant
import string, random

def generate_random_email_password():
    length = 10
    letters = string.ascii_lowercase
    email = ''.join(random.choice(letters) for _ in range(length))
    email += "@denrox.com"
    password = ''.join(random.choice(letters) for _ in range(8))
    return email, password

class ApiUser(HttpUser):
    wait_time = between(1,5)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
  
    def on_start(self) -> None:
      self.email, self.password = generate_random_email_password()
      response = self.client.post("/users", json={"email": self.email, "password": self.password})
      self.token = response.json()["data"]["token"]
      self.client.headers["Authorization"] = "Bearer " + self.token
      self.user_tasks = []
      return super().on_start()
    @task(1)
    def login(self):
        response = self.client.post("/users/login", json={"email": self.email, "password": self.password})
        if (response.status_code == 200):
          self.token = response.json()["data"]["token"]
          self.client.headers["Authorization"] = "Bearer " + self.token

    @task(10)
    def get_user(self):
        self.client.get("/users")

    @task(3)
    def create_task(self):
        response = self.client.post("/tasks", json={"name":"test", "description": "description", "start_time":10, "duration":10})
        if (response.status_code == 200):
          self.user_tasks.append(response.json()["data"]["task"]["id"])
    @task(10)
    def get_tasks(self):
        response = self.client.get("/tasks")
        if (response.status_code == 200):
          self.user_tasks = list(map(lambda task: task["id"], response.json()["data"]["tasks"]))
    @task(2)
    def delete_task(self):
        if (len(self.user_tasks)!=0):
          user_task = random.choice(self.user_tasks)
          response = self.client.delete("/tasks/%s" %user_task, name="/tasks/{id}")
          if (response.status_code == 200):
              self.user_tasks.remove(user_task)
    @task(3)
    def update_task(self):
      if (len(self.user_tasks)!=0):
        user_task = random.choice(self.user_tasks)
        response = self.client.put("/tasks/%s" %user_task, name="/tasks/{id}", json={"is_solved": True})




