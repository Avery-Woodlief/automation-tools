import subprocess # part of standard python library
import re
import os

def make_requirements():
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from file_generation_tools.get_requirements import RequirementsMixin


    packages_used = ["subprocess", "regex", "os", "sys", "pathlib", "pygame"]

    requirements = RequirementsMixin()
    for package in packages_used:
        requirements.add(package)

    requirements.upload("tools_for_git/")

#make_requirements()

common_extensions = '''.py
.pyw
.pyi
.pyc
.js
.mjs
.cjs
.ts
.tsx
.jsx
.html
.htm
.css
.scss
.sass
.less
.json
.yaml
.yml
.xml
.toml
.ini
.cfg
.conf
.env
.txt
.md
.rst
.tex
.csv
.tsv
.xfc
.sql
.db
.sqlite
.sqlite3
.c
.h
.cpp
.cc
.cxx
.hpp
.hh
.java
.class
.jar
.kt
.kts
.scala
.go
.rs
.swift
.m
.mm
.cs
.fs
.vb
.php
.rb
.pl
.pm
.lua
.r
.mat
.sh
.bash
.zsh
.ps1
.bat
.cmd
.make
.mk
.gradle
.kts
.pom
.lock
.gitignore
.gitattributes
.dockerignore
.dockerfile
.docker-compose.yml
.tf
.tfvars
.hcl
.proto
.graphql
.gql
.ipynb
.notebook
.requirements
.whl
.egg
.zip
.tar
.gz
.7z
.rar
.so
.dll
.dylib
.exe
.bin
.obj
.o
.a
.lib
.log
.png
.jpg
.jpeg
.svg
.ico
.gif
.webp'''


commands = {
            "git add": lambda files : subprocess.run(["git", "add", files]),
            "git commit -m": lambda commit : subprocess.run(["git", "commit", "-m", commit]),
            "git commit -a -m": lambda commit : subprocess.run(["git", "commit", "-a", "-m", commit]),
            "git remote add": lambda repo_url : subprocess.run(["git", "remote", "add", repo_url]),
            "git pull": lambda repo_url: subprocess.run(["git", "pull", repo_url]),
            "git branch -M": lambda new_master_name_forced: subprocess.run(["git", "branch", "-M", new_master_name_forced]),
            "git branch -m": lambda new_master_name_checked: subprocess.run(["git", "branch", "-m", new_master_name_checked])
            }


class GitHelper:

    def __init__(self):
        self.output_string = ""
        self.exts = common_extensions.split("\n")
        self.hidden_files = [".gitignore", ".requirements", ".gitattributes", ".dockerignore", ".env"] # files that are supposed to be hidden
        self.pattern = self.create_pattern()
        self.untracked_files = None
        self.deleted_files = None
        self.modified_files = None
        self.section_names = ["deleted", "modified", "Untracked files"]
        self.files = {section : None for section in self.section_names}
        
        self.section_orders = {"deleted":-1, "modified":-1, "Untracked files":-1}
        self.sorted_orders = []
        self.ordered_sections = []
        self.current_section = ""

    def create_pattern(self):
        base = "[^\s*]"
        base += f"\w+\{self.exts[0]}"
        for i in range(1, len(self.exts)):
            if self.exts[i] in self.hidden_files:
                base += f"|\{self.exts[i]}"
            else:
                base += f"|\w+\{self.exts[i]}"
        print("created parsing pattern...")
        #print(base)
        return base

    def run(self, command):
        if ((command not in list(commands.keys())) and 
            (command != "git status") and (command != "git push") and
            (command != "git add .") and (command != "git init") and
            (command != "git branch")):
            print(f"'{command}' is not a valid command")
            return
        elif (command == "git push"):
            result = subprocess.run(command, capture_output=True, text=True)
            print("COMMAND:", " ".join(command))
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            print("RETURN CODE:", result.returncode)

            if result.returncode != 0:
                raise RuntimeError("Command failed")
        elif (command == "git status"):
            self.output_string = subprocess.check_output(["git", "status"],text=True)
            self.init_sections()     
        elif (command == "git add ."):# commands that just need the sub_process function
            commands[command]
        elif (command == "git init"):
            subprocess.run(["git", "init"])
        elif (command == "git add ."):
            subprocess.run(["git", "add", "."])
        elif (command == "git branch"):
            subprocess.run(["git","branch"])    
        else:
            commands[command](input("> "))
       
    def init_sections(self):
        for section in self.section_names:
            try:
                self.section_orders[section] = self.output_string.index(section)
            except (ValueError):
                continue
        substr = ""
        for section in self.section_names:
            try:
                substr = section
                self.section_orders[section] = self.output_string.index(section)
            except (IndexError, ValueError) as e:
                self.section_orders[section] = -1
                #print(f"None {section}")
                if (section == "Untracked files"):
                    print("no untracked files")
                else:
                    print(f"no {section} files")
        self.section_names = []
        for name, order in self.section_orders.items():
            if order != -1:
                self.section_names.append(name)
        #
        self.sorted_orders = sorted(list(self.section_orders.values()))
        swap = self.sorted_orders
        self.sorted_orders = [i for i in swap if i > -1]
        
        i = 0
        while (len(self.ordered_sections) < len(self.section_names)):
            for section, order in self.section_orders.items():
                #print(self.ordered_sections)
                #print(order)
                
                if order == self.sorted_orders[i % len(self.section_names)]:
                    self.ordered_sections.append(section)
                    i += 1
        #print(self.ordered_sections)
        print("initialized and ordered the sections")
        return

    def get_section_after(self, section):
        i = self.ordered_sections.index(section)
        if (i + 1 == len(self.ordered_sections)):
            return "last section"
        else:
            return self.ordered_sections[i + 1]

    def get_files(self, section):
        self.current_section = section
        if self.section_orders[self.current_section] == -1: # section does not exist or not found because no files from git
            return
        print(f"Searching for {self.current_section} files...")
        files_string = None
        if self.get_section_after(self.current_section) == "last section":
            #print("here")
            files_string = self.output_string[self.output_string.index(self.current_section + ":"):]
        else:
            next_section = self.get_section_after(self.current_section)
            #print(next_index)
            try:
                files_string = self.output_string[self.output_string.index(self.current_section + ":"):self.output_string.index(next_section + ":")]
            except (IndexError, ValueError):
                print("please do .run(\"git status\") on GitHelper() object")
                
                return
            if (not files_string):
                print("please do .run(\"git status\") on GitHelper() object")
                #print(next_section)
                return
        #print("\t"+files_string)
        self.files[section] = re.findall(self.pattern, files_string)
        print(f"successfully grabbed files from section: {section}")
        return
    

def example1():

    git_helper = GitHelper()
    git_helper.run("git status")
    #git_helper.run("git push")

    for section in git_helper.section_names:
        git_helper.get_files(section)

    #git_helper.run("add ext")

    #print(git_helper.files)

    git_helper.run("git add")
    git_helper.run("git commit -m")
    if (input("push? (Y/N): ") == "Y"):
        git_helper.run("git push")
    else:
        print("not pushing commits")

    print("program terminated safely\n")

#example1()


def example2():

    git_helper = GitHelper()
    #git_helper.run("git status")
    for section in git_helper.section_names:
        git_helper.get_files(section)

    import pygame

    pygame.init()

    screen = pygame.display.set_mode((1000, 600))
    font = pygame.font.Font(None, 36)

    screen_text = f"> {git_helper.files}"
    all_text = {screen_text:0}
    text = ""
    current_text = ""
    y = 0
    x = 0
    running = True

    while running:
        screen.fill((255, 255, 255))
        
        for text_, y_ in all_text.items():
            text_surface = font.render(text_, True, (0, 0, 0))
            screen.blit(text_surface, (x, y_))

        for event in pygame.event.get():
            
            #print(event)

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                if (event.key == pygame.K_RETURN):
                    all_text[screen_text] = y                
                    y += 36
                    
                    if text in list(commands.keys()):
                        git_helper.run(text)
                        text = ""
                    screen_text = "> " + text

                elif event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_BACKSPACE:
                    
                    text = text[:-1]
                    screen_text = "> " + text
                    current_text = screen_text
                else:
                    text += event.unicode
                    screen_text = "> " + text
                    current_text = screen_text
                    
        
        if (y > 600):
            screen.fill((255, 255, 255))
            y = 0
            all_text = {}

        

        text_surface = font.render(current_text, True, (0, 0, 0))
        screen.blit(text_surface, (x, y))
        
        pygame.display.flip()

    pygame.quit()

    if (input("push? (Y/N): ") == "Y"):
        git_helper.run("git push")
    else:
        print("not pushing commits")

    print("program terminated safely\n")

