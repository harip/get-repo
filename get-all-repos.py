import requests as req
import math as math
from tqdm import tqdm

org=""
token=""
org_url=f'https://api.github.com/orgs/{org}?access_token={token}'

org_repo_data=req.get(org_url).json()
total_repo=org_repo_data["public_repos"]+org_repo_data["total_private_repos"]
num_of_pages=math.ceil(total_repo/30)

download_urls=[]
for i in range(1,num_of_pages+1):
    org_repos_url=f'https://api.github.com/orgs/{org}/repos?access_token={token}&page={i}'
    r=req.get(org_repos_url).json()
    
    page_download_links=[(repo_url["name"], repo_url["archive_url"].replace("{archive_format}","zipball").replace("{/ref}","/master")) for repo_url in r]
    download_urls=download_urls+page_download_links

download_urls.sort(key=lambda tup:tup[0].lower())

for download_url in download_urls:
    r=req.get(f'{download_url[1]}?access_token={token}')
    with open(f'{download_url[0]}.zip', "wb") as handle:
        for data in tqdm(r.iter_content()):
            handle.write(data) 

print("Finished")
 