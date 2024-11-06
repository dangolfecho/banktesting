from selenium import webdriver
from selenium.webdriver.common.by import By
from termcolor import colored  # Ensure `termcolor` is installed with `pip install termcolor`
import time

# Set up the WebDriver
driver = webdriver.Chrome()

try:
    # Open the login page
    driver.get("http://127.0.0.1:8000/")
    time.sleep(2)

    # Click on the "Login" button
    login_button = driver.find_element(By.XPATH, "/html/body/nav/div[3]/div[2]/a")
    login_button.click()
    time.sleep(2)

    # Enter email and password
    driver.find_element(By.XPATH, "/html/body/div/div/form/div[1]/input").send_keys("email@example.com")  # Email
    driver.find_element(By.XPATH, "/html/body/div/div/form/div[2]/input").send_keys("poiu0192")  # Password

    # Click the "Submit" button to login
    submit_button = driver.find_element(By.XPATH, "/html/body/div/div/form/div[3]/button")
    submit_button.click()
    time.sleep(3)  # Wait for the dashboard to load

    # Click the "Deposit" anchor
    deposit_link = driver.find_element(By.XPATH, "/html/body/nav/div[3]/div[1]/a[2]")
    deposit_link.click()
    time.sleep(2)

    # Enter amount to deposit
    amount = "100"  # Change this to the desired amount
    driver.find_element(By.XPATH, "/html/body/div/div/form/div/input").send_keys(amount)

    # Click the "Submit" button to deposit
    submit_button = driver.find_element(By.XPATH, "/html/body/div/div/form/button")
    submit_button.click()
    time.sleep(3)  # Wait for the response

    # Check for success message
    success_message = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/p[1]").text
    msg_content = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/p[2]").text


    if success_message and "deposited" in msg_content and f"{amount}" in msg_content:
        print(colored("Deposit: Success!", "green"))
    else:
        print(colored("Deposit: Failed!", "red"))
except:
    print(colored("Deposit: Failed!", "red"))
finally:
    # Close the browser
    driver.quit()
