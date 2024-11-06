from selenium import webdriver
from selenium.webdriver.common.by import By
from termcolor import colored  # Ensure `termcolor` is installed with `pip install termcolor`
import time
import re

# Set up the WebDriver
driver = webdriver.Chrome()

try:
    # Open the page with the transaction table
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
    
    # Click the "Transaction Report" anchor
    transaction_link = driver.find_element(By.XPATH, "/html/body/nav/div[3]/div[1]/a[1]")
    transaction_link.click()
    time.sleep(2)

    # Locate the transaction table body
    tbody = driver.find_element(By.XPATH, "/html/body/div[1]/table/tbody")
    rows = tbody.find_elements(By.TAG_NAME, "tr")

    calculated_balance = 0.0  # Start with an initial balance (can be 0 or an opening balance if known)
    
    for row in rows[:-1]:  # Exclude the last row as it's meant to show only the final balance
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) >= 4:
            transaction_type = cells[0].text.strip()  # Transaction Type (Deposit/Withdraw)
            amount_text = cells[2].text.strip()       # Amount for the transaction
            
            # Remove currency symbol and commas, then convert to float
            amount = float(re.sub(r"[^\d.]", "", amount_text))

            # Update calculated balance based on transaction type
            if transaction_type == "Deposit":
                calculated_balance += amount
            elif transaction_type == "Withdrawal":
                calculated_balance -= amount

    # Get the final balance from the last row
    last_row = rows[-1]
    last_row_cells = last_row.find_elements(By.TAG_NAME, "th")

    # Ensure the last row has the balance displayed
    if len(last_row_cells) >= 2:
        final_balance_text = last_row_cells[1].text.strip()
        final_balance = float(re.sub(r"[^\d.]", "", final_balance_text))  # Balance after the last transaction

        # Validate calculated balance against the final balance displayed
        if calculated_balance == final_balance:
            print(colored("Balance validation: Success! Calculated balance matches the final balance.", "green"))
        else:
            print(colored("Balance validation: Failed! Calculated balance does not match the final balance.", "red"))
    else:
        print(colored("Balance validation: Failed! Final balance cell is missing or inaccessible.", "red"))

finally:
    # Close the browser
    driver.quit()
