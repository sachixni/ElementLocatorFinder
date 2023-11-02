import requests
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By


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

def generate_relative_xpath(element):
    path = [element.tag]
    for parent in element.iterancestors():
        path.insert(0, parent.tag)
    return '/'.join(path)

def extract_xpaths(url, desired_tags):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve the webpage. Status code: {response.status_code}")

    tree = html.fromstring(response.text)
    xpaths_dict = {}

    for tag in desired_tags:
        elements_with_tag = tree.xpath(f'//{tag}')
        for element in elements_with_tag:
            xpaths = generate_all_xpaths(element)
            for xpath in xpaths:
                xpaths_dict.setdefault(tag, []).append(xpath)

    return xpaths_dict


def save_xpaths_to_file(xpaths_dict, filename='xpath_1.txt'):
    with open(filename, 'w') as file:
        for tag, xpaths in xpaths_dict.items():
            for xpath in xpaths:
                file.write(f"{tag} XPath: {xpath}\n")
    print(f"XPaths saved to '{filename}' file.")


def xpath_extractor(tags):
    def decorator(func):
        def wrapper(url):
            desired_tags = [tag.strip() for tag in tags.split(',')]
            xpaths_dict = extract_xpaths(url, desired_tags)
            save_xpaths_to_file(xpaths_dict)
            return func(url)

        return wrapper

    return decorator


@xpath_extractor("button,a,img")
def process_webpage(url):
    # Open the URL in a web browser with selenium
    driver = webdriver.Chrome()
    driver.get(url)
    driver.quit()


# Get user input for the URL
url = input("Enter the URL of the webpage: ")
process_webpage(url)