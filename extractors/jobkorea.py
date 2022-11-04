from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from requests import get

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")


def extract_jobkorea_jobs(keyword):
    driver = webdriver.Chrome(executable_path='C:/chromedriver.exe')
    driver.implicitly_wait(3)
    driver.get(f"https://www.jobkorea.co.kr/Search/?stext={keyword}")
    results = []
    soup = BeautifulSoup(driver.page_source, "html.parser")
    jobs = soup.find_all("li", class_="list-post")
    for job in jobs :
      section = job.find("div", class_="post")
      company = section.find_all("a")[0]
      job_post = job.find("div", class_="post-list-info")
      anchor = job_post.find_all("a")[0]
      link = anchor["href"]
      region_section = job.find("p", class_="option")
      region_anchor = region_section.find("span", class_="loc long")
      if region_anchor is not None:
        region = str(region_anchor.string)
      if anchor is not None:
        position = str(anchor.string)
      job_data = {
          "company": company.string.replace(","," "),
          "region": region.replace(","," "),
          "position" : position.replace(","," ").strip(),
          "link": f"https://www.jobkorea.co.kr{link}"
        }
      results.append(job_data)
    return results
