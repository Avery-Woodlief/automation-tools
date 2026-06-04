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

### Downloading as python3 package

    1) navigate to `file_generation_tools`
    2) run python3 -m pip install -e . (installs `file_generation_tools` as a python3 package you can use anywhere)
        2.a) If you want to delete package then just do python3 -m pip uninstall file_generation_tools
#### Command Line use

    1) python3
    2) from requirements import Requirements
    3) Requirements()

#### In .py file use

    1) Goto the end of any working .py file in your python3 project
    2) from requirements import Requirements
    3) Requirements()

##### Explaination

    When you do Requirements() it creates an instance of a class that searches through (from root of project) all the .py files in your project.
    Then it parses through each one, line by line to search from keywords such as `import` or `from` in sentences such as: 
        'import \w+\.\w+', 'import \w+', 'from \w+\.\w+', 'from \w+'
    and it grabs whatever is the `\w+` or `\w+\.\w+`, checks validity of the found name to make sure its actually an import and puts it in a list. It also uses a dictionary that maps dependencies for a specific .py file.
    Then it writes to a `requirements.txt` file in root of your project and places the dependeces with version numbers as `name==version`.
    
    _WARNING_:
        some import names do not match the distribution names and may fail to be collected, however the following cases are handled by default:
            "dotenv":"python-dotenv", 
            "PIL":"Pillow", 
            "cv2":"opencv-python", 
            "sklearn":"scikit-learn", 
            "yaml":"PyYAML", 
            "re":"regex"
