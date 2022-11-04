from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from requests import get

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")


def extract_saramin_jobs(keyword):
    driver = webdriver.Chrome(executable_path='C:/chromedriver.exe')
    driver.implicitly_wait(3)
    driver.get(f"https://www.saramin.co.kr/zf_user/search?search_area=main&search_done=y&search_optional_item=n&searchType=recently&searchword={keyword}")

    results = []
    soup = BeautifulSoup(driver.page_source, "html.parser")
    jobs_section = soup.find("section", class_="section_search")
    jobs = jobs_section.find_all("div", class_="item_recruit")
    for job in jobs:
        companys_section = job.find("div", class_="area_corp")
        company = companys_section.find("a")
        job_tit = job.find("h2", class_="job_tit")
        anchor = job_tit.find_all("a")[0]
        title = anchor["title"]
        link = anchor["href"]
        region_section = job.find("div", class_="job_condition")
        region = region_section.find("a")
        job_data = {
          'company': company.string.strip(),
          'region': region.string,
          'position': title.replace(","," "),
          'link': f"https://www.saramin.co.kr{link}"
        }
        results.append(job_data)
    return results