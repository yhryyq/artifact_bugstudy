from subprocess import Popen, PIPE, STDOUT
import pandas as pd
from tqdm import tqdm
from filter import checkProject
import re

def exe_command(command):
    print("command: "+command)
    process = Popen(command, stdout=PIPE, stderr=STDOUT, shell=True)
    result = ""
    with process.stdout:
        for line in iter(process.stdout.readline, b''):
            try:
                result = result + line.decode().strip() + "$#$"
                print(line.decode().strip())
            except Exception as e:
                pass
    exitcode = process.wait()
    return result, process, exitcode

def hasCorPy(sha,repo_path):
    output = exe_command(f"cd {repo_path} && git show -m {sha}")
    lines = re.split(r'\$\#\$',output[0])
    end_tag = False
    for line in lines:
        if line[0:7] == "commit ":
            if end_tag:
                break
            else:
                end_tag = True
        if line.startswith('+++ ') or line.startswith('--- '):
            line_list = line.split('/')
            if line_list[-1].endswith('c') or line_list[-1].endswith('py'):
                return True
    return False

data1 = pd.read_csv('./pyc_bug_commit.csv',sep=',',header=None,names=['sha','proj_name', 'tag'])
sha_list = list(data1['sha'])
proj_list = list(data1['proj_name'])
tag_list = list(data1['tag'])


for i in tqdm(range(len(sha_list))):
    print(i)
    new_sha = []
    new_proj = []
    new_tag = []
    sha = sha_list[i]
    proj = proj_list[i]
    repo_name = proj.split('/')[1]
    proj_dir = f"{repo_name}_{sha}"
    
    repo_path = f"./{proj_dir}"
    exe_command(f"bash downloadsha.sh {sha} {proj}")
    if hasCorPy(sha, repo_path):
        cfunc, ctype = checkProject(repo_path)
        if cfunc != []:
            print("{i} commit saved to the csv")
            new_sha.append(sha)
            new_proj.append(proj)
            new_tag.append(tag_list[i])

    exe_command(f"rm -rf {repo_path}")

    inter_bug = pd.DataFrame({'sha': new_sha, 'proj': new_proj, 'tag': new_tag})
    inter_bug.to_csv("pyc_inter_bug_commits.csv",mode='a',header=False,index=False,sep=',')
