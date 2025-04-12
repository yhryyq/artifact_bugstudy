# Dissecting Real-World Cross-Language Bugs

This is the artifact of the paper *Dissecting Real-World Cross-Language Bugs*

## 1. Overview
This artifact contains the tools in methodology and manual bug analysis result.

## 2. Directory structure
Repository_Mining - This folder contains the tools of crawling repository list and get commits of each repository. 

CLB_Commit_Classification - This folder contains the tools used for identifying bug-fixing commit, cross-language code revision and cross-language-bug-fixing commit.

Manual_Bug_Analysis_Result - This folder contains the results of manual analysis on both Python-C and Java-C.

## 3. Usage
### Repository_Mining
In "Repository_Mining" folder, there are two files, which are "getrepo.py" and "getcommits.py".

####<u>getrepo.py</u>
First, users need to insert their GitHub personal access token into the "token" variable in the code.

Second, users can modify the "stars_split" list variable to set the desired star count for the repositories to be fetched. By default, it fetches repositories with more than 1000 stars.

Third, the code is set up to fetch Python-C repositories by default. If users need to fetch Java-C repositories, simply replace python with java in the code.

Finally, execute **python getrepo.py**, get output "pyc_repo_list.csv" file.

####<u>getcommits.py</u>
Users need to specify the input repository in the pd.read_csv（） method. By default, it is "pyc_repo_list.csv".

Execute **python getcommits.py**, get output "pyc_commit.csv" file.

### CLB_Commit_Classification
In "CLB Commit Classification" folder, there are two folders and one file, which are "getbugfixing.py", "Cross-Language_Code_Revision_Identification" and "Cross-Language-Bug-Fixing_Commit_Identification".

####<u>getbugfixing.py</u>
First, users need to insert their GitHub personal access token into the "token" variable in the code.

Second, users need to specify the input commits in the pd.read_csv（） method. By default, it is "./pyc_commit.csv".

Finally, execute **python getbugfixing.py**, get output "pyc_bug_commit.csv" file.

####<u>Cross-Language_Code_Revision_Identification</u>
Users need to specify the input bug commits in the pd.read_csv method in "getinter.py". By default, it is "./pyc_bug_commit.csv".

Execute **cd Cross-Language-Bug-Fixing_Commit_Identification && python getinter.py**, get output "pyc_inter_bug_commits.csv" file.

####<u>Cross-Language-Bug-Fixing_Commit_Identification</u>
First, users need to configure "file_name" as the input in runtool.sh. By default, this is set to "pyc_inter_bug_commits.csv".

Second, users need to configure "start_line" and "end_line" to specify the start and end index of the commits in the input file . By default, this is set to "1" and "20", which means the first 20 commints in the input file can be generated CICFG.

Then, executing **bash runtool.sh** will start the generation of CICFGs for the specified commits. Note that if the repository of the commits is large, this process may take some time.

Next, users can traverse the generated CICFG by executing the command **bash autorun.sh [sha_id] [repo_name] [function_name] [line_number] [traversal_direction]**. 
In this command, [sha_id] represents the commit's SHA ID, [repo_name] is the full name of the repository, [function_name] is the name of the function containing the traversal start point, [line_number] indicates the line number of the traversal start point, and [traversal_direction] has two options: "b" for backward traversal and "f" for forward traversal.
For example, **bash autorun.sh 8e870efd2345ba2549f7cb10b920c94baf38f17d DataSoft/Honeyd yyparse 1916 f**.

Finally, there is a traversal output file named "log_[repo_name]_[sha_id]_[traversal_direction]", which contains the cross-language control flow path.

The below result means no cross-language path has been found:
========starting traverse
function name:yyparse, start_line_number:1916
=============Done=============

The below result means cross-language path has been found:
========starting traverse
function name:pixels2d, start_line_number:132
mapping by 132(py__numpysurfarray_4-cfg.dot) (pixels2d),and 2170(c_surface_114-cfg.dot) (surf_get_view)
func_count:30
len:49
Path
: 132(py__numpysurfarray_4-cfg.dot) (pixels2d)
 -> 2170(c_surface_114-cfg.dot) (surf_get_view)
 -> 2168(c_surface_114-cfg.dot) (surf_get_view)
 ...

### Manual_Bug_Analysis_Result
In "Manual Bug Analysis Result" folder, there are four files, which are "javac_case_study.xlsx", "pyc_case_study.xlsx", "Case_Study_[Python-C]_raw_data.docx" and "Case_Study_[Java-C]_raw_data.docx".

####<u>javac_case_study.xlsx</u>
This file includes the manual analysis result on CLB symptom, location, manifestation, root cause, and fixing strategy in Java-C.

####<u>pyc_case_study.xlsx</u>
This file includes the manual analysis result on CLB symptom, location, manifestation, root cause, and fixing strategy in Python-C.

####<u>"Case_Study_[Python-C]_raw_data.docx</u>
This file includes the detailed raw data about each commits among Python-C.

####<u>"Case_Study_[Java-C]_raw_data.docx</u>
This file includes the detailed raw data about each commits among Java-C.
