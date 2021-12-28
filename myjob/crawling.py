import requests
from bs4 import BeautifulSoup
import re

def extract_remote_job(html):
  urls=[]
  titles=[]
  companies = []
  remote_job_list = []
  url_raw = html.find_all("tr", attrs={'data-href': re.compile("^/remote-jobs/")})
  for url in url_raw:
    url = url.get("data-href")
    url = "https://remoteok.com" + url
    urls.append(url)
  title_raw =  html.find_all("h2", {"itemprop":"title"})
  for title in title_raw:
     title = title.text
     title = title.replace("\n","")
     titles.append(title)
  companies_raw =  html.find_all("h3", {"itemprop":"name"})
  for company in companies_raw:
     company = company.text
     company = company.replace("\n","")
     companies.append(company)
  for i in range(len(urls)):
    job_dict = {}
    for i in range(len(urls)):
      job_dict["title"] = titles[i]
      job_dict["company"] = companies[i]
      job_dict["url"] = urls[i]
    remote_job_list.append(job_dict)
  return remote_job_list


def extract_remote_jobs(URL,header):
  print(f"Scrapping remote page")
  remote_jobs = []
  result = requests.get(URL,headers = header)
  soup = BeautifulSoup(result.text, "html.parser")
  results = soup.select("table",{"id":"jobsboard"})
  for result in results:
    job = extract_remote_job(result)
    remote_jobs.append(job)
  return remote_jobs


def get_remote_jobs(word):
    URL = f"https://remoteok.io/remote-dev+{word}-jobs"
    header = {'user-agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}
    remote_jobs = extract_remote_jobs(URL,header)
    return remote_jobs


def get_so_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class": "s-pagination"})
    links = pagination.find_all("a")
    pages = []
    for page in links[:-1]:
        pages.append(int(page.text))
    max_so_page = pages[-1]
    return max_so_page


def extract_so_job(html):
    job_id = html["data-jobid"]
    title = html.find("h2", {"class": "mb4 fc-black-800 fs-body3"}).a.string
    company_raw = html.find("h3", {"class": "fc-black-700 fs-body1 mb4"}).text
    company_raw = ''.join(company_raw.splitlines())
    company_raw = company_raw.split(" • ")
    company = company_raw[0].strip()
    link = f'https://stackoverflow.com/jobs/{job_id}/?so=i&q=python&r=true'

    return {
        "title": title,
        "company": company,
        "url": link
    }


def extract_so_jobs(last_page,url):
    so_jobs = []
    for page in range(last_page):
        print(f"Scrapping So page : {page}")
        result = requests.get(f"{url}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})

        for result in results:
            job = extract_so_job(result)
            so_jobs.append(job)
    return so_jobs


def get_so_jobs(word):
    url = f"https://stackoverflow.com/jobs?r=true&q={word}"
    last_page = get_so_last_page(url)
    so_jobs = extract_so_jobs(last_page,url)
    return so_jobs

def get_wwr_url(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.select("h2 > a")
    urls = []
    for a in pagination:
        if a["href"][-3:] != "rss":
            url = "https://weworkremotely.com" + a["href"]
            urls.append(url)
    return wwr_urls


def extract_wwr_job(html):
    urls = html.find_all("a", attrs={'href': re.compile("^/remote-jobs/")})
    for url in urls:
        url = url.get("href")
        url = "https://weworkremotely.com" + url
    titles = html.find_all("span", {"class": "title"})
    for title in titles:
        title = title.text
    companies = html.find_all("span", {"class": "company"})
    for company in companies:
        company = company.text

    return {"title": title, "company": company, "url": url}


def extract_wwr_jobs(urls):
    wwr_jobs = []

    for url in urls:
        print("Scrapping wwr page : " + url)
        result = requests.get(url)
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.select("ul > li.feature")
        for result in results:
            job = extract_wwr_job(result)
            wwr_jobs.append(job)
    return wwr_jobs


def get_wwr_jobs(word):
    url = f"https://weworkremotely.com/remote-jobs/search?term={word}"
    urls = get_wwr_url(url)
    wwr_jobs = extract_wwr_jobs(urls)
    return wwr_jobs
