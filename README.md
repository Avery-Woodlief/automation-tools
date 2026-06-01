# automation-tools
Tools that automate things like git, requirements.txt, etc.

## Tools for git

~/Documents/projects/automation_tools$ python3
Python 3.10.12 (main, Mar  3 2026, 11:56:32) [GCC 11.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from tools_for_git.helper_git_class import *
>>> git = GitHelper()
created parsing pattern...
>>> git.run("git status")
no deleted files
no untracked files
initialized and ordered the sections
Searching for modified files...
successfully grabbed files from section: modified
>>> git.run("git commit -a -m")
> update
[main 2ca7c14] update
 1 file changed, 1 insertion(+), 1 deletion(-)
>>> git.run("git push")
COMMAND: g i t   p u s h
STDOUT: 
STDERR: To https://github.com/Avery-Woodlief/automation-tools.git
   984383c..2ca7c14  main -> main

RETURN CODE: 0
>>> 

