import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime

url = "https://www.google.com/finance/markets/most-active?hl=en"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Find the specific ul element
ul_element = soup.find("ul", class_="sbnBtf")

if ul_element:
    # Find all li elements within the ul
    li_elements = ul_element.find_all("li")

    # Extract and write data from divs with known classes inside each li element
    data = []
    for li in li_elements:
        company_name_element = li.find("div", class_="ZvmM7")
        stock_price_element = li.find("div", class_="YMlKec")
        

        # Check if elements exist before getting text
        company_name = company_name_element.get_text(strip=True) if company_name_element else "N/A"
        stock_price = stock_price_element.get_text(strip=True) if stock_price_element else "N/A"
       

        data.append({
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Company Name": company_name,
            "Stock Price": stock_price
        })
    # Create a new CSV file with the filename "finance.csv"
    file_name = "finance.csv"

    with open(file_name, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Date", "Company Code", "Company Name", "Stock Price"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header
        writer.writeheader()

        # Write the data to the CSV file
        for row in data:
            writer.writerow(row)

    print(f"Data has been successfully saved to {file_name}")

else:
    print("Unable to find the specified ul element on the page.")