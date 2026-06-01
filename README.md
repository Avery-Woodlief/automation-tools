# automation-tools
Tools that automate things like git, requirements.txt, etc.

## Tools for git

### example usage from command line

$ python3
Python 3.10.12 (main, Mar  3 2026, 11:56:32) [GCC 11.4.0] on linux

> from tools_for_git.helper_git_class import *

> git = GitHelper()

created parsing pattern...

> git.run("git status")

no deleted files

no untracked files

initialized and ordered the sections

Searching for modified files...

successfully grabbed files from section: modified

> git.run("git commit -a -m")
>> update

[main 2ca7c14] update
 1 file changed, 1 insertion(+), 1 deletion(-)

> git.run("git push")

COMMAND: g i t p u s h

STDOUT:

STDERR:
To https://github.com/Avery-Woodlief/automation-tools.git
   984383c..2ca7c14  main -> main

RETURN CODE: 0

## Other File Tools

### Creating a requirements.txt

#### example 1

>def example_usage2(packages, dest = ""):
>>    req = RequirementsMixin() # this just does the one package it uses, importlib.metadata. sys is part of standard

>>    for package in packages:

>>      req.add(package)

>>    req.upload(dest)

>example_usage2(["pygame", "regex", "importlib.metadata"], "../")

#### output of example 1 in generated file requirements.txt

>pygame==2.5.2

>regex==2023.10.3

>importlib.metadata==4.6.4

