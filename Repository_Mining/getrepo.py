import urllib.request, json
import subprocess
import pandas as pd
import time
import requests

id=[]
html_url=[]
api_url=[]
full_name=[]
open_issues=[]
pushed_at=[]
created_at=[]
topics=[]
description=[]
commits_url=[]


#######################################
# put your personal access token here
#######################################
token = ""


urlFront = "https://api.github.com/search/repositories?q=stars:"
#urlForks = "+forks:"
urlEnd = "+language:c+is:public&per_page=100&order=asc&page="

stars_split = [">1000"]

for star_num in stars_split:
    # for forks in ["<15",">=15"]:
    for fork_num in range(1):
        '''
        if fork_num == 10:
            forks = ">=10"
        else:
            forks = str(fork_num) + ".." + str(fork_num)
        print(star_num)
        print(forks)
        '''
        for page in range(1,11):
            id = []
            html_url = []
            api_url = []
            full_name = []
            open_issues = []
            pushed_at = []
            created_at = []
            topics = []
            description = []
            commits_url = []
            c_percent = []
            py_percent = []
            print(f"page:{page}")
            #url = url_src + str(page)
            url = urlFront + str(star_num) + urlEnd + str(page)


            request = urllib.request.Request(url=url)
            request.add_header('Authorization', 'token %s' % token)
            response = urllib.request.urlopen(request)
            
            data = json.loads(response.read())
            if len(data['items']) == 0:
                break
            counter = 1
            for project in data['items']:
                print(counter)
                counter += 1
                req = urllib.request.Request(url=project['languages_url'])
                req.add_header('Authorization', 'token %s' % token)
                resp = urllib.request.urlopen(req)
                languages = json.loads(resp.read())
                # print(languages)
                if 'C' in languages.keys() and 'Python' in languages.keys() and languages["Python"]/sum(languages.values())+languages["C"]/sum(languages.values()) > 0.5:
                    c_count = languages["C"]
                    py_count = languages["Python"]
                    total_count = sum(languages.values())
                    c_percentage = (c_count / total_count) * 100
                    py_percentage = (py_count / total_count) * 100
                    id.append(project['id'])
                    html_url.append(project['html_url'])
                    api_url.append(project['url'])
                    full_name.append(project['full_name'])
                    open_issues.append(project['open_issues'])
                    pushed_at.append(project['pushed_at'])
                    created_at.append(project['created_at'])
                    topics.append(project['topics'])
                    description.append(project['description'])
                    commits_url.append(project['commits_url'])
                    c_percent.append(c_percentage)
                    py_percent.append(py_percentage)
                time.sleep(5)
            time.sleep(30)

        
            repo_list = pd.DataFrame({'id':id,
                                    'html_url':html_url,
                                    'api_url':api_url,
                                    'full_name':full_name,
                                    'open_issues':open_issues,
                                    'pushed_at':pushed_at,
                                    'created_at':created_at,
                                    'topics':topics,
                                    'description':description,
                                    'commits_url':commits_url,
                                    'c_percent':c_percent,
                                    'py_percent':py_percent})
            repo_list.to_csv("pyc_repo_list.csv",mode='a', header=True, index=False, sep=',')
            print(f"saved star({star_num}),page:{page} data")
        time.sleep(60)

print("-------------------DONE--------------------")
