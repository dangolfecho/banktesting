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

    # Check for the presence of transaction, deposit, and withdraw links
    try:
        transaction_link = driver.find_element(By.XPATH, "/html/body/nav/div[3]/div[1]/a[1]")
        deposit_link = driver.find_element(By.XPATH, "/html/body/nav/div[3]/div[1]/a[2]")
        withdraw_link = driver.find_element(By.XPATH, "/html/body/nav/div[3]/div[1]/a[3]")
        print(colored("Login: Success!", "green"))
    except:
        print(colored("Login: Failed!", "red"))
except:
    print(colored("Login: Failed!", "red"))
  
finally:
    # Close the browser
    driver.quit()
