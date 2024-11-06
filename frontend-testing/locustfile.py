from locust import HttpUser, task, between, events
import matplotlib.pyplot as plt

latency_data = []

@events.request.add_listener
def on_request_success(request_type, name, response_time, response_length, **kwargs):
    latency_data.append(response_time)

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)  # Simulate wait time between requests

    @task(2)  # Higher weight for login
    def login(self):
        # Replace with actual login data
        self.client.post("/accounts/login/", {
            "username": "email@example.com",
            "password": "poiu0192",
            "csrfmiddlewaretoken": "is1kTN8cifJ3AjBDBiBwKwSj133JQ3R4xGsoILB1RfM4lk20dCvfWHdBApgEtEL6",
        })

    # @task(1)  # Lower weight for registration
    # def register(self):
    #     # Replace with actual registration data
    #     self.client.post("/accounts/register/", {
    #         "username": "newuser",
    #         "password": "newpassword",
    #         "email": "newuser@example.com"
    #     })

    def on_start(self):
        # This method runs when a simulated user starts
        pass

@events.quitting.add_listener
def on_quitting(environment, **kwargs):
    # Plot latency results when the test is done
    plt.figure(figsize=(10, 5))
    plt.plot(latency_data, label='Response Time (ms)', color='blue')
    plt.title('Response Time for Login and Registration over Time')
    plt.xlabel('Requests')
    plt.ylabel('Response Time (ms)')
    plt.legend()
    plt.grid(True)
    plt.savefig('latency_plot.png')  # Save the plot as an image
    plt.show()  # Show the plot
