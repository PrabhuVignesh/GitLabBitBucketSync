import subprocess
from git import Repo
import os
import urllib.parse
import errno, stat, shutil
import datetime

pwd = subprocess.check_output("pwd", shell=True, universal_newlines=True)
#================================== From GitLab ===============================
GitLab_Directory = os.getenv('GitLabDir')
GitLab_Branch = os.getenv('GitLabBRANCH')
GitLab_URL = os.getenv('GitLabURL')
GitLab_Username=urllib.parse.quote_plus(os.getenv('GitLabUsername'))
GitLab_Password=urllib.parse.quote_plus(os.getenv('GitLabPassword'))
GitLab_URL_Path_arr = GitLab_URL.split("https://")
if not os.path.exists(GitLab_Directory):
    os.mkdir(GitLab_Directory)
else:
  os.system("rm -rf "+GitLab_Directory)
  os.mkdir(GitLab_Directory)
base_location_gitlab = (str(pwd.rstrip("\n"))+"/"+GitLab_Directory)
Repo.clone_from("https://"+GitLab_Username+":"+GitLab_Password+"@"+GitLab_URL_Path_arr[1],base_location_gitlab,branch=GitLab_Branch)

#================================== From BitBucket ===============================
Bitbucket_Directory = os.getenv('BitbuckerDir')
Bitbucket_Branch = os.getenv('BitbuckerBRANCH')
Bitbucket_URL = os.getenv('BitbuckerURL')
Bitbucket_Username=urllib.parse.quote_plus(os.getenv('BitbucketUsername'))
Bitbucket_Password=urllib.parse.quote_plus(os.getenv('BitbuckerPassword'))
Bitbucket_URL_Path_arr = Bitbucket_URL.split("https://")
if not os.path.exists(Bitbucket_Directory):
    os.mkdir(Bitbucket_Directory)
else:
  os.system("rm -rf "+Bitbucket_Directory)
  os.mkdir(Bitbucket_Directory)
base_location_bitbucket = (str(pwd.rstrip("\n"))+"/"+Bitbucket_Directory)
Repo.clone_from("https://"+Bitbucket_Username+":"+Bitbucket_Password+"@"+Bitbucket_URL_Path_arr[1],base_location_bitbucket,branch=Bitbucket_Branch)

#==================================== Directory Operations ================================
os.system("rm -rf "+base_location_gitlab+"/.git/")
os.system("cp -R "+base_location_bitbucket+"/.git "+base_location_gitlab)
#====================================
COMMIT_MESSAGE = "GitLab Sync from jenkins @" datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p") + os.getenv('BUILD_ID')

repo = Repo(base_location_gitlab+"/.git/")
repo.git.checkout('origin/sync') 
repo.git.add('--all')
repo.index.commit(COMMIT_MESSAGE)
repo.git.push('origin', 'HEAD:sync') 
