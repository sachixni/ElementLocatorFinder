import requests
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
import pyautogui
import time

# Function to generate all possible XPaths for an element
def generate_all_xpaths(element):
    xpaths = []

    # Generate absolute XPaths for attributes
    for attribute in element.attrib:
        xpaths.append(f"//{element.tag}[@{attribute}='{element.get(attribute)}']")

    # Generate absolute XPaths for positions
    for i, sibling in enumerate(element.itersiblings(preceding=True), start=1):
        if sibling.tag == element.tag:
            xpaths.append(f"//{element.tag}[{i}]")

    # Generate absolute XPaths for text content
    if element.text:
        xpaths.append(f"//{element.tag}[text()='{element.text.strip()}']")

    # Generate relative XPaths
    xpaths.append(generate_relative_xpath(element))

    return xpaths


# Function to generate relative XPath for an element
def generate_relative_xpath(element):
    path = [element.tag]
    for parent in element.iterancestors():
        path.insert(0, parent.tag)
    return '/'.join(path)


# Get user input for the URL
url = input("Enter the URL of the webpage: ")

# Get user input for the list of desired HTML tags
tags_input = input("Enter a comma-separated list of desired HTML tags (e.g., button,a,img): ")
desired_tags = [tag.strip() for tag in tags_input.split(',')]

# Send an HTTP GET request to fetch the webpage's HTML content
response = requests.get(url)

# Open the URL in a web browser with selenium
driver = webdriver.Chrome()
driver.get(url)
driver.quit()

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using lxml
    tree = html.fromstring(response.text)

    # Create a text file to save the XPaths
    with open('xpath_2.txt', 'w') as file:

        for tag in desired_tags:
            elements_with_tag = tree.xpath(f'//{tag}')
            for element in elements_with_tag:
                xpaths = generate_all_xpaths(element)
                for xpath in xpaths:
                    file.write(f"{tag} XPath: {xpath}\n")

    print("XPaths saved to 'xpath_2.txt' file.")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

############################################with selenium web driver #################################
# from selenium import webdriver
# from selenium.webdriver.common.by import By
#
# driver = webdriver.Chrome()
# #chromeDriverPath = "C:\Program Files (x86)\chromeDrivers\chromedriver.exe"
#
# url = "https://the-internet.herokuapp.com/add_remove_elements/"
# driver.get(url)
#
# # Function to generate XPath for an element
# def generate_xpath(element):
#     xpath = ''
#     while element.tag_name != 'html':
#         tag_name = element.tag_name.lower()
#         attributes = []
#
#         # Add attributes such as ID, class, src (for images), text, and name
#         element_id = element.get_attribute('id')
#         if element_id:
#             attributes.append(f'@id="{element_id}"')
#
#         element_class = element.get_attribute('class')
#         if element_class:
#             attributes.append(f'contains(@class, "{element_class}")')
#
#         element_src = element.get_attribute('src')
#         if element_src:
#             attributes.append(f'contains(@src, "{element_src}")')
#
#         element_text = element.text.strip()
#         if element_text:
#             attributes.append(f'contains(text(), "{element_text}")')
#
#         element_name = element.get_attribute('name')
#         if element_name:
#             attributes.append(f'@name="{element_name}"')
#
#         attributes_str = ' and '.join(attributes)
#
#         xpath_segment = f'//{tag_name}[{attributes_str}]'
#         xpath = xpath_segment + xpath
#         element = element.find_element(By.XPATH, '..')
#     return  xpath
#
# # List of desired HTML tags
# desired_tags = ['img', 'input', 'button', 'label', 'textarea', 'a', 'li', 'th', 'td', 'ol', 'ul', 'footer', 'header', 'table']
#
# # Find the root element (usually the 'html' tag)
# root_element = driver.find_element(By.TAG_NAME, 'html')
#
# # Generate XPaths for specific HTML tags
# all_xpaths = []
#
# for tag_name in desired_tags:
#     elements_with_tag = root_element.find_elements(By.TAG_NAME, tag_name)
#     for element in elements_with_tag:
#         xpath = generate_xpath(element)
#         all_xpaths.append(xpath)
#
# # Print the generated XPaths
# for xpath in all_xpaths:
#     print(xpath)
#
# # Define the file path where you want to save the XPaths
# file_path = 'xpaths.txt'
#
# # Save the generated XPaths to a text file
# with open(file_path, 'w') as file:
#     for xpath in all_xpaths:
#         file.write(xpath + '\n')
#
# driver.quit()
#
# print(f'XPaths have been saved to {file_path}')
#
