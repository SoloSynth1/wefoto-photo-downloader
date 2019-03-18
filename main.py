from selenium import webdriver
import re
import requests


def get_hdlinks(driver):
    photos = driver.find_elements_by_class_name("lazy-container")
    hdlinks = []
    for photo in photos:
        js_statement = photo.get_attribute('onclick')
        links = re.findall(r"(https://.*?)\'", js_statement)
        hdlink = links[1]
        hdlinks.append(hdlink)
    return hdlinks

def download_links(links):
    while links:
        response = requests.get(links[0])
        if response.status_code == 200:
            filename = re.findall(r'/357/(.*?\.JPG)', links[0])[0].lower()
            with open(filename, 'wb') as f:
                f.write(response.content)
            links.pop(0)
            print("{} saved".format(filename))
        else:
            print(response.status_code)

if __name__ == "__main__":
    driver = webdriver.Firefox()
    driver.get("https://www.wefoto.com/masterconcept")
    element = driver.find_element_by_xpath("//div/a")
    url = element.get_attribute('href')
    driver.get(url)
    current_page = 1
    hdlinks = []
    while True:
        hdlinks += get_hdlinks(driver)
        next = driver.find_element_by_class_name('next')
        if int(next.get_attribute('data-lp')) != current_page:
            driver.get(next.find_element_by_tag_name('a').get_attribute('href'))
            current_page += 1
        else:
            break
    driver.close()
    download_links(hdlinks)
