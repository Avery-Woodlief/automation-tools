from importlib.metadata import version, PackageNotFoundError
import sys


class RequirementsMixin:

    def __init__(self, prints = 0, include_metadata = 0):
        if include_metadata:
            self.requirements = {"importlib.metadata":version("importlib.metadata")}
        else:
            self.requirements = {}
        self.prints = prints
        
        self.flags = (self.prints) # maybe add more flags here

    def __setitem__(self, package_name, version):
        self.requirements[package_name] = version

    def add(self, package_name): # test comment
        try:
            self[package_name] = version(package_name)
        except (PackageNotFoundError):
            if (package_name in sys.stdlib_module_names):
                if (self.flags & self.prints):
                    print(f"{package_name} is part of python standard library")
            else:
                if (self.flags & self.prints):
                    print(f"{package_name} might be a typo")

    def __str__(self):
        formatted=""
        for package, version in self.requirements.items():
            formatted += f"{package}=={version}\n"
        return formatted

    def upload(self, destination = ""):
        with open(destination + "requirements.txt", "w") as file:
            file.write(self.__str__())

        file.close()

def example_usage():
    req = RequirementsMixin(include_metadata = 1) # this just does the one package it uses, importlib.metadata
                              # sys is part of standard

    #packages = ["pygame", "regex", "importlib.metadata"]

    #for package in packages:
        #req[package] = version(package)

    req.upload()
#example_usage()

def example_usage2(packages, dest = ""):
    req = RequirementsMixin() # this just does the one package it uses, importlib.metadata
                              # sys is part of standard

    for package in packages:
        req[package] = version(package)

    req.upload(dest)

#example_usage2(["pygame", "regex", "importlib.metadata"], "../")
