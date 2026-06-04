from importlib.metadata import version, PackageNotFoundError
from pathlib import Path
import sys
import re
import os


#from get_requirements import *;req = Requirements(prints=1);req.grab_file("get_requirements.py");req.get_file_imports();req.current_file_imports


class Requirements:

    def __init__(self, prints = 0, include_metadata = 0):
        if include_metadata:
            self.requirements = {"importlib.metadata":version("importlib.metadata")}
        else:
            self.requirements = {}
        self.prints = prints

        self.logs = {"part of standard":[], "import name and package name differ":[]}
        self.weird_import_names = {
                                    "dotenv":"python-dotenv", 
                                    "PIL":"Pillow", 
                                    "cv2":"opencv-python", 
                                    "sklearn":"scikit-learn", 
                                    "yaml":"PyYAML", 
                                    "re":"regex"
                                   }
        
        self.flags = (self.prints) # maybe add more flags here
        self.current_file = [] # list of lines in file
        self.project_imports = {}
        self.current_file_imports = []
        self.current_file_name = ""
        self.python_files = list(Path(".").rglob("*.py"))
        for file_ in self.python_files:
            self.grab_file(file_)
            self.get_file_imports()
            for import_ in self.project_imports[file_]:
                self.add(import_)
        self.logs["part of standard"] = list(set(self.logs["part of standard"]))
        self.logs["import name and package name differ"] = list(set(self.logs["import name and package name differ"]))
        self.upload()
        
    
    def grab_file(self, file_name):
        with open(file_name, "r") as file:
            self.current_file = file.readlines()
            self.current_file_name = file_name
            file.close()
        return

    def get_file_imports(self):
        ignoring = False
        for line in self.current_file:
            if (re.search(r"\s*'''|'''", line)):
                if (ignoring): # closing '''
                    ignoring = False
                elif (not ignoring): # opening '''
                    ignoring = True
            if (ignoring):
                continue
            if (re.search(r"\s*#", line)):
                continue
            if (re.search(r"(?<=from )(\w+\.\w+|\w+)", line)):
                #print(line)
                self.current_file_imports.append(re.search(r"(?<=from )(\w+\.\w+|\w+)", line).group(0))
            elif (re.search(r"(?<=import )(\w+\.\w+|\w+)", line)):
                self.current_file_imports.append(re.search(r"(?<=import )(\w+\.\w+|\w+)", line).group(0))

        for import_ in self.current_file_imports:
            if import_ in list(self.weird_import_names.keys()):
                self.current_file_imports.remove(import_)
                self.current_file_imports.append(self.weird_import_names[import_])
            
        self.project_imports[self.current_file_name] = self.current_file_imports

    def __setitem__(self, package_name, version):
        self.requirements[package_name] = version

    def add(self, package_name):
        try:
            self[package_name] = version(package_name)
        except (PackageNotFoundError):
            if (package_name in sys.stdlib_module_names):
                if (self.flags & self.prints):
                    self.logs["part of standard"].append(f"{package_name}")
            else:
                if (self.flags & self.prints):
                    self.logs["import name and package name differ"].append(f"{package_name}")

    def __str__(self):
        formatted=""
        for package, version in self.requirements.items():
            formatted += f"{package}=={version}\n"
        return formatted

    def upload(self, destination = ""):
        with open(destination + "requirements.txt", "w") as file:
            file.write(self.__str__())
        file.close()
