from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random

# Launch browser
driver = webdriver.Chrome()
driver.maximize_window()

wait = WebDriverWait(driver, 10)

driver.get("https://parabank.parasoft.com/parabank/index.htm")

# ---------------- REGISTER ---------------- #

wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Register']"))).click()

wait.until(EC.visibility_of_element_located((By.ID, "customer.firstName"))).send_keys("John")
driver.find_element(By.ID, "customer.lastName").send_keys("Doe")
driver.find_element(By.ID, "customer.address.street").send_keys("123 Main Street")
driver.find_element(By.ID, "customer.address.city").send_keys("New York")
driver.find_element(By.ID, "customer.address.state").send_keys("NY")
driver.find_element(By.ID, "customer.address.zipCode").send_keys("560076")
driver.find_element(By.ID, "customer.phoneNumber").send_keys("9835084672")
driver.find_element(By.ID, "customer.ssn").send_keys("123456")

# Generate random username
username = "john_doe" + str(random.randint(1000, 9999))

driver.find_element(By.ID, "customer.username").send_keys(username)
driver.find_element(By.ID, "customer.password").send_keys("john@doe1")
driver.find_element(By.ID, "repeatedPassword").send_keys("john@doe1")

driver.find_element(By.XPATH, "//input[@value='Register']").click()

# Verify Registration
success_message = wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, "//*[contains(text(),'Your account was created successfully')]")
    )
)

assert success_message.is_displayed()
print("Registration Successful")

# ---------------- LOGOUT ---------------- #

wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Log Out']"))).click()
print("Logout Successful")

# ---------------- LOGIN ---------------- #

wait.until(EC.visibility_of_element_located((By.NAME,"username"))).send_keys(username)
driver.find_element(By.NAME,"password").send_keys("john@doe1")

wait.until(EC.element_to_be_clickable((By.XPATH,"//input[@value='Log In']"))).click()

# Verify Login using Logout button
logout_btn = wait.until(
    EC.visibility_of_element_located((By.XPATH,"//a[text()='Log Out']"))
)

assert logout_btn.is_displayed()
print("Login Successful")

# ---------------- TRANSFER FUNDS ---------------- #

wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Transfer Funds"))).click()

# Wait until Transfer Funds page loads
wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[contains(text(),'Transfer Funds')]")))

# Wait for amount field
amount_field = wait.until(
    EC.visibility_of_element_located((By.ID, "amount"))
)

amount_field.clear()
amount_field.send_keys("1")

# Wait for dropdowns to populate
wait.until(
    EC.presence_of_element_located((By.ID, "fromAccountId"))
)

wait.until(
    EC.presence_of_element_located((By.ID, "toAccountId"))
)
sleep(2)

# Click Transfer
transfer_btn = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//input[@value='Transfer']"))
)

transfer_btn.click()

# Verify Transfer Success
success_msg = wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, "//h1[contains(text(),'Transfer Complete')]")
    )
)

assert success_msg.is_displayed()
print("Fund Transfer Successful")

# ---------------- FINAL LOGOUT ---------------- #

wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Log Out']"))).click()

print("Final Logout Successful")

driver.quit()