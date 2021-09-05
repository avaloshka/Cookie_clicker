from selenium import webdriver
import time


driver = webdriver.Chrome("C:\Development\chromedriver.exe")
driver.get("https://orteil.dashnet.org/cookieclicker/")
driver.maximize_window()

cookie = driver.find_element_by_id("bigCookie")

# Get upgrade item ids.
items = []
for num in range(17):
    try:
        item = driver.find_element_by_id(f"product{num}")
        items.append(item)
    except:
        print("Something went wrong with finding an item")
items_text = [item.text for item in items]
item_ids = [item.get_attribute("id") for item in items]

timeout = time.time() + 5
five_min = time.time() + 60 * 5  # 5 minutes

while True:
    cookie.click()

    #Every 5 seconds.
    if time.time() > timeout:

        # Get All upgrade tags
        all_prices = driver.find_elements_by_css_selector("#store span")
        item_prices = []
        for price in all_prices:
            element_text = price.text
            if element_text != "":
                try:
                    cost = int(element_text.replace(",", ""))
                    item_prices.append(cost)
                except:
                    item_prices.append(element_text)

        # Create dictionary of store items and prices
        cookie_upgrades = {}
        for n in range(len(item_prices)):
            cookie_upgrades[item_prices[n]] = item_ids[n]

        #Get current cookie count
        money_element = driver.find_element_by_id("cookies").text
        cookie_count = int(money_element.split(" ")[0])

        #Find upgrades that we can currently afford
        affordable_upgrades = {}
        for cost, id in cookie_upgrades.items():
            if cookie_count > cost:
                 affordable_upgrades[cost] = id
        print("Affordable upgrade: ", affordable_upgrades)

        # Purchase the most expensive affordable upgrade
        highest_price_affordable_upgrade = max(affordable_upgrades)
        print("Highest price affordable upgrade: ", highest_price_affordable_upgrade)
        to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]
        print("To purchase id: ", to_purchase_id)

        # Not working! Why?????????? Something changed on website, possibly 
        driver.find_element_by_css_selector(f"#{to_purchase_id}").click()

        timeout = time.time() + 5

        if time.time() > five_min:
            cookie_per_s = driver.find_element_by_id("cps").text
            print(cookie_per_s)
            break
