import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Initialize Selenium WebDriver
service = Service()  # Update with the path to your chromedriver
driver = webdriver.Chrome(service=service)

# URL of the blog site to scrape
url = 'https://realpython.com/'  # Replace this with the actual URL
driver.get(url)

# Function to extract blog data from the HTML content
def extract_blog_data(soup):
    data_list = []

    # Find all blog card divs
    blog_divs = soup.find_all('div', class_='col-12 col-md-6 col-lg-4 mb-5')
    for blog in blog_divs:
        card = blog.find('div', class_='card border-0')
        
        # Extract URL
        url = card.find('a')['href']
        
        # Extract image source
        img_tag = card.find('img', class_='card-img-top')
        img_src = img_tag['src'] if img_tag else None
        
        # Extract title
        title_tag = card.find('h2', class_='card-title h4 my-0 py-0')
        title = title_tag.get_text(strip=True) if title_tag else None
        
        # Extract date
        date_span = card.find('span', class_='mr-2')
        date = date_span.get_text(strip=True) if date_span else None
        
        # Extract categories
        categories = [a.get_text(strip=True) for a in card.find_all('a', class_='badge badge-light text-muted')]

        data_list.append({
            'URL': url,
            'Image_Src': img_src,
            'Title': title,
            'Date': date,
            'Categories': ', '.join(categories)
        })
    
    return data_list

# Scroll and click "Load More" button 5 times
for _ in range(5):
    try:
        load_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'frontpageLoadMore'))
        )
        driver.execute_script("arguments[0].scrollIntoView();", load_more_button)
        load_more_button.click()
        time.sleep(5)  # Wait for the new content to load
    except Exception as e:
        print(f"Exception occurred: {e}")
        break

# Get the page source after loading more content
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

# Extract the blog data
blog_data = extract_blog_data(soup)

# Convert to DataFrame
df = pd.DataFrame(blog_data)

# Save the DataFrame to a CSV file
df.to_csv('extracted_blog_data.csv', index=False)
print("Data saved to extracted_blog_data.csv")

# Close the browser
driver.quit()
