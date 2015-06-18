#!/usr/bin/env python
#-*- coding:utf-8 -*-
#
'''
This is a one-file python script that analyze the content of a local folder
name ./cores and upload its content to github.

This script is to be used after opencores_scraper.py for the purpose of getting
all opencores.org code upload to a github account.

The Python libraries needed for this script can be installed with the command:

    sudo pip install tarfile

 HOW TO USE THIS SCRIPT

 1) install python and its dependencies
 2) configure the git address _github_addr
 3) run this script with the command:  ./local2git.py
'''

_github_addr = 'https://github.com/fabriziotappero/ip-cores.git'

import sys, os, shutil, glob
import tarfile
from distutils.dir_util import copy_tree

prj_categ = next(os.walk('./cores'))[1]
prjs = []
empty_prjs = 0
for x in prj_categ:
    _path = './cores/' + x
    for y in next(os.walk(_path))[1]:
        z = os.listdir(_path + "/" + y)
        for elem in z:
            #get only projects with a tar.gz file in it(not empty)
            if elem.endswith(".tar.gz"):
                z = x[:5] + "_" + y[:10] # branch name encoding
                prjs.append([[z],[x],[y]])
                break

# note that from now on prjs stores all info
print "Number of local non empty projects: ", len(prjs)

# detect projects with the same branch name
_branches = [x[0][0] for x in prjs]
dups = [x for x in _branches if _branches.count(x) > 1]
if len(dups)>0:
    print "ERROR. Projects with same branch name:", dups
    sys.exit(0)

if True:
    sys.exit(0)


_txt = '''
## VHDL/Verilog IP CORES

The following branch contains the following VHDL/VERILOG IP Code.

Project name: %s

Project category: %s

Project branch: %s

This whole github repository contains approximately **4.5GB of free and open source
IP cores**. To download only this project you can use the git command:

**git clone -b %s --single-branch https://github.com/fabriziotappero/ip-cores.git**

### License

This code was taken "as is" from the website opencores.org.
The copyright owner of this IP code is the original author of the code. For
more information have a look at index.html or at the website opencores.org

This code is free software; you can redistribute it and/or modify it under the
terms of the http://www.gnu.org/licenses/gpl.html (GNU General Public License)
as published by the Free Software Foundation; either version 2 of the License,
or (at your option) any later version.

This code is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A	PARTICULAR PURPOSE. See the GNU General Public License for
more details.
'''

for _ind,x in enumerate(prjs):
    prj_branch = x[0][0]
    prj_cat = x[1][0]
    prj_name = x[2][0]
    _dir = os.path.join('cores', prj_cat, prj_name)
    for _fl in os.listdir(_dir):
        if _fl.endswith('.tar.gz'):
            prj_real_name = _fl[: -7]
            print "From:", _dir, "\nUnzipping:", _fl, "\n"
            tfile = tarfile.open(os.path.join(_dir, _fl), 'r:gz')
            tfile.extractall(os.path.join(_dir, 'tmp'))
            tfile.close()
            if os.path.exists(os.path.join(_dir, 'src')):
                shutil.rmtree(os.path.join(_dir, 'src'))

            # copy all svn trunk in fresh src folder. If trunk does not exist
            # copy the whole thing.
            if os.path.isdir(os.path.join(_dir, 'tmp', _fl[: -7], 'trunk')):
                copy_tree(os.path.join(_dir, 'tmp', _fl[: -7], 'trunk'), os.path.join(_dir, 'src'))
            if os.path.isdir(os.path.join(_dir, 'tmp', _fl[: -7], 'web_uploads')):
                copy_tree(os.path.join(_dir, 'tmp', _fl[: -7], 'web_uploads'), os.path.join(_dir, 'src'))

            #elif os.path.isdir(os.path.join(_dir, 'tmp', _fl[: -7])):
            #    shutil.copytree(os.path.join(_dir, 'tmp', _fl[: -7]), os.path.join(_dir, 'src'))

            # add README.md file and index file
            if os.path.isdir(os.path.join(_dir,'src')):
                with open(os.path.join(_dir,'src','README.md'), 'w') as _file:
                    _file.write(_txt % (prj_name, prj_cat, prj_branch, prj_branch))
            if os.path.isfile(os.path.join(_dir, 'index.html')):
                if os.path.isdir(os.path.join(_dir,'src')):
                    shutil.copyfile(os.path.join(_dir, 'index.html'), os.path.join(_dir, 'src','index.html'))

            # just in case you unzipped a zip file(one zip inside another)
            for _x in glob.glob(os.path.join(_dir, 'src', '*')):
                if _x.endswith('.tar.gz') or _x.endswith('.tgz'):
                    tfile = tarfile.open(_x, 'r:gz')
                    tfile.extractall(os.path.join(_dir, 'src'))
                    tfile.close()
                    os.remove(_x)

            # deleted not needed files
            if os.path.isfile(os.path.join(_dir, _fl)):
                if False: # for debugging use False
                    os.remove(os.path.join(_dir, _fl))# remove tar.gz file
                    
            if os.path.isdir(os.path.join(_dir, 'tmp')):
                shutil.rmtree(os.path.join(_dir, 'tmp'))# remove original unzipped folder

if False:
    sys.exit(0)

# proceed with git, created a local git folder
_git_dir = os.path.join('cores', 'git_dir')
if os.path.isdir(_git_dir):
    shutil.rmtree(_git_dir)
os.mkdir(_git_dir)

# download (locally) only master branch from the defaul github repository that
# you specified at the beginning of this file
os.system('git clone --depth=1 ' + _github_addr + ' '+_git_dir)

# create a new branch per project. Copy the project content in it.
for _ind,x in enumerate(prjs):
    prj_branch = x[0][0]
    prj_cat = x[1][0]
    prj_name = x[2][0]
    prj_dir = os.path.join('cores', prj_cat, prj_name)

    if os.path.exists(os.path.join(_dir, 'src')) and len(os.listdir(os.path.join(prj_dir,'src')))>0:
        # this project is not empty
        os.chdir(_git_dir)
        os.system('git checkout --orphan ' + prj_branch + ' >/dev/null') # create new branch
        os.system('git rm --cached -r . >/dev/null') # empty the new branch
        os.system('rm -Rf ./*')

        os.system('cp -Rf ../../'+prj_dir+'/src/* .') # add all project files into branch

        os.system('git add .') # add project into branch
        os.system("git commit -m 'added content for project'") # add project into branch
        os.system("git checkout master") # add project into branch
        os.chdir(os.path.join('..','..'))

if False:
    # push all branches at once
    os.system('git push --all origin')
    # manually enter login and password

# if False:
#     # upload one by one all branches to github
#     for _ind,x in enumerate(prjs):
#         prj_branch = x[0][0]
#         prj_cat = x[1][0]
#         prj_name = x[2][0]
#         prj_dir = os.path.join('cores', prj_cat, prj_name)
#
#         if len(os.listdir(os.path.join(prj_dir,'src')))>0:
#             os.chdir(_git_dir)
#             os.system('git checkout ' + prj_branch)
#             os.system('git push origin '+ prj_branch)
#             # manually enter login and password
#             os.chdir(os.path.join('..','..'))
