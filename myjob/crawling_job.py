
from bs4 import BeautifulSoup
from django.db.models import Q
import requests,re, os, django
from datetime import datetime


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myjob.settings")

django.setup()
from jobapp.models import GetInfo


def extract_remote_job(html,word):
    remote_jobs = []
    for row in html:
        title = row.find("h2", {"itemprop": "title"})

        title = title.text.strip()
        link = row["data-url"]

        link = f"https://remoteok.com{link}"
        company = row.find("h3", {"itemprop": "name"})

        company = company.text.strip()
        job = {"title": title, "company": company, "url": link,"word":word}
        remote_jobs.append(job)
    return remote_jobs


def extract_remote_jobs(URL, header, word):
    print(f"Scrapping remote page")

    result = requests.get(URL, headers=header)
    soup = BeautifulSoup(result.text, "html.parser")
    raw = soup.find("table", {"id": "jobsboard"})
    if raw is None:
        results = []
        job = extract_remote_job(results, word)
        return job

    if raw is not None:


        results = raw.find_all("tr", {"class": "job"})
        job = extract_remote_job(results, word)

        return job


def get_remote_jobs(word):
    URL = f"https://remoteok.io/remote-{word}-jobs"
    header = {
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}

    remote_jobs = extract_remote_jobs(URL, header, word)
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


def extract_so_job(html, word):
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
        "url": link,
        "word":word
    }


def extract_so_jobs(last_page, url, word):
    so_jobs = []
    for page in range(last_page):
        print(f"Scrapping So page : {page}")
        result = requests.get(f"{url}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})

        for result in results:
            job = extract_so_job(result, word)
            so_jobs.append(job)
    return so_jobs


def get_so_jobs(word):
    url = f"https://stackoverflow.com/jobs?r=true&q={word}"
    last_page = get_so_last_page(url)
    so_jobs = extract_so_jobs(last_page, url, word)
    return so_jobs

def get_wwr_url(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.select("h2 > a")
    wwr_urls = []
    for a in pagination:
        if a["href"][-3:] != "rss":
            url = "https://weworkremotely.com" + a["href"]
            wwr_urls.append(url)
    return wwr_urls


def extract_wwr_job(html, word):
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

    return {"title": title, "company": company, "url": url, "word":word}


def extract_wwr_jobs(urls, word):
    wwr_jobs = []

    for url in urls:
        print("Scrapping wwr page : " + url)
        result = requests.get(url)
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.select("ul > li.feature")
        for result in results:
            job = extract_wwr_job(result, word)
            wwr_jobs.append(job)
    return wwr_jobs


def get_wwr_jobs(word):
    url = f"https://weworkremotely.com/remote-jobs/search?term={word}"
    urls = get_wwr_url(url)
    wwr_jobs = extract_wwr_jobs(urls, word)
    return wwr_jobs


def getCrawler(word="python"):
    word = str(word).lower()

    so_jobs = get_so_jobs(word)

    wwr_jobs = get_wwr_jobs(word)

    remote_jobs = get_remote_jobs(word)

    jobs = so_jobs + wwr_jobs+ remote_jobs

    return jobs


def add_new_items(crawled_items):

    # last_inserted_items = GetInfo.objects.last()

    if GetInfo.objects.last() is None:
        last_inserted_specific_id = ""
    else:
        last_inserted_specific_id = getattr(GetInfo.objects.last(), 'url')

    items_to_insert_into_db = []
    for item in crawled_items:
        if item['url'] == last_inserted_specific_id:
            break
        items_to_insert_into_db.append(item)
    items_to_insert_into_db.reverse()

    for item in items_to_insert_into_db:
        print("new item added!! : " + item['title'])

        GetInfo(
                word = item["word"],
                title=item["title"],
                company=item["company"],
                url=item["url"]).save()

    return items_to_insert_into_db

import csv

def DBtoCSV(word):
    with open("jobs.csv","w",newline="",encoding="utf-8") as csvfile:
        fieldnames=["title","company","url","word"]
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames)

        writer.writeheader()

        for job in GetInfo.objects.all().filter(Q(word__icontains=word)):
            # print(job)
            writer.writerow({"title":job.title, "company":job.company, "url":job.url, "word":job.word})





def crwler_job(word):
    from crawling_job import getCrawler, add_new_items

    print("start - " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    crawled_data = getCrawler(word)
    add_new_items(crawled_data)

#
    # for if __name__ == "__main__":
# #     crawler_data = DBtoCSV("python")
# #     print(crawler_data)data in crawler_data:
    #     GetInfo(word = data["word"],title=data["title"], company=data["company"], url=data["url"]).save()
