from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from termcolor import colored  # You may need to install this package via `pip install termcolor`
import time

# Set up the WebDriver
driver = webdriver.Chrome()

try:
    # Open the URL
    driver.get("http://127.0.0.1:8000/")
    time.sleep(2)

    # Click on the "Register" button
    register_button = driver.find_element(By.XPATH, "/html/body/nav/div[3]/div[3]/a")
    register_button.click()
    time.sleep(2)

    # Fill in the form fields
    driver.find_element(By.XPATH, "/html/body/div/div/form/div[1]/div[1]/input").send_keys("FirstName")
    driver.find_element(By.XPATH, "/html/body/div/div/form/div[1]/div[2]/input").send_keys("LastName")
    driver.find_element(By.XPATH, "/html/body/div/div/form/div[2]/div[1]/input").send_keys("email5@example.com")

    # Select Account Type
    account_select = Select(driver.find_element(By.XPATH, "/html/body/div/div/form/div[2]/div[2]/select"))
    account_select.select_by_visible_text("saving")

    # Select Gender
    gender_select = Select(driver.find_element(By.XPATH, "/html/body/div/div/form/div[3]/div[1]/select"))
    gender_select.select_by_visible_text("Male")

    # Enter Birthday
    driver.find_element(By.XPATH, "/html/body/div/div/form/div[3]/div[2]/input").send_keys("01/01/1990")

    # Enter Password and Confirm Password
    driver.find_element(By.XPATH, "/html/body/div/div/form/div[4]/div[1]/input").send_keys("poiu0192")
    driver.find_element(By.XPATH, "/html/body/div/div/form/div[4]/div[2]/input").send_keys("poiu0192")

    # Enter Address Details
    driver.find_element(By.XPATH, "/html/body/div/div/form/div[5]/div[1]/input").send_keys("123 Street")
    driver.find_element(By.XPATH, "/html/body/div/div/form/div[5]/div[2]/input").send_keys("CityName")
    driver.find_element(By.XPATH, "/html/body/div/div/form/div[6]/div[1]/input").send_keys("12345")
    driver.find_element(By.XPATH, "/html/body/div/div/form/div[6]/div[2]/input").send_keys("CountryName")

    # Click the "Submit" button
    submit_button = driver.find_element(By.XPATH, "/html/body/div/div/form/div[7]/button")
    submit_button.click()

    # Wait briefly for response page to load
    time.sleep(3)

    # Check for success message
    try:
        success_message = driver.find_element(By.XPATH, "/html/body/div/div[1]/div/div[2]/p[1]")
        print(colored("Register: Test Success!", "green"))
    except:
        print(colored("Register: Test Failed!", "red"))
except:
    print(colored("Register: Test Failed!", "red"))
finally:
    # Close the browser
    driver.quit()
