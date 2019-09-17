import subprocess
from git import Repo
import os
import urllib.parse
import errno, stat, shutil

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
# git.Git(base_location_gitlab).clone("https://"+GitLab_Username+":"+GitLab_Password+"@"+GitLab_URL_Path_arr[1])
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
# git.Git(base_location_bitbucket).clone("https://"+Bitbucket_Username+":"+Bitbucket_Password+"@"+Bitbucket_URL_Path_arr[1])
Repo.clone_from("https://"+Bitbucket_Username+":"+Bitbucket_Password+"@"+Bitbucket_URL_Path_arr[1],base_location_bitbucket,branch=Bitbucket_Branch)

#==================================== Directory Operations ================================
os.system("rm -rf "+base_location_gitlab+"/.git/")
os.system("cp -R "+base_location_bitbucket+"/.git "+base_location_gitlab)
# os.system("cat "+base_location_gitlab+"/.git/config")
#====================================
COMMIT_MESSAGE = "Commiting from Python1" + os.getenv('BUILD_ID')
# try:
#     repo = Repo(base_location_gitlab+"/.git/")
#     repo.git.add(update=True)
#     repo.index.commit(COMMIT_MESSAGE)
#     origin = repo.remote(name="https://"+Bitbucket_Username+":"+Bitbucket_Password+"@"+Bitbucket_URL_Path_arr[1])
#     origin.push()
# except:
#     print('Some error occured while pushing the code')

repo = Repo(base_location_gitlab+"/.git/")
repo.git.checkout('origin/sync') #checkout to a branch linked to the other repo
repo.git.add('--all')
repo.index.commit(COMMIT_MESSAGE)
repo.git.push('origin', 'HEAD:sync') # git push remote_to_push HEAD:master

# os.system("cd "+base_location_gitlab+" && git checkout "+Bitbucket_Branch+" && git add --all "+" && git commit -m "+COMMIT_MESSAGE+ " && git push origin "+Bitbucket_Branch)
