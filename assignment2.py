#!/usr/bin/env python3

'''
OPS445 Assignment 2
Program: assignment2.py 
Authors: "Emmanuel Onah", "Cristian Fedor", "Biswas Turja Nandini Dia", "Kevin Ho"
Semester: "Winter 2025"

The python code in this file (assignment1.py) is original work written by
Members of Group 4. No code in this file is copied from any other source
except those provided by the course instructor, including any person,
textbook, or on-line resource. We have not shared this python script
with anyone or anything except for between each other and submission for grading. We understand
that the Academic Honesty Policy will be enforced and violators will be reported and appropriate action will be taken.

The valid_date, mon_max and leap_year function were all gotten from the the previous assignment, Assignment 1. Specifically gotten from Emmanuel's assignment solution.
'''
import os
from datetime import datetime
import argparse
import json
import re

# Todo File path
TODO_FILE = "todo_list.json"

parser = argparse.ArgumentParser()
parser.add_argument("-s","--show", help="Show todo list without running loop", action="store_true")
args = parser.parse_args()

class TodoItem:
    """Item class definition for object creation"""
    def __init__(self, title, description, due_date, priority):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority

    def __repr__(self):
        return f"{self.title} - {self.description} (Due: {self.due_date}, Priority: {self.priority})"

def add_task():
    """Function for getting user input, creating task item and adding the item to todo_list.json file"""
  
  open_todo_file = open(TODO_FILE< "a+") # Open file in append, read mode
  
  title = input("Enter Task Title: ")   #Ask user to input Title, description, due_date and priority of the task. 
  
  description = input("Enter Short Description: ")
  
  dute_date = input("Enter due date (YYYY-MM-DD): ")
  
  priority = input("Enter Priority (High/Medium/Low: ").capitalize()
  
  if not valid_date(due_date):  # testing if the user input date and priority is valid
    print("\nInvalid due_date. ")
    
  if priority not in ["High", "Medium", "Low"]: #testing if the priority inputted is valid
    print("\nInvalid priority! Defaulting to 'Low'.")
    priority = "Low"
    
  todo_item = TodoItem(title, description, due_date, priority)  # create a new task object using the TodoItem class
  todo_dict = todo_item.__dict__ # convert the task object to a dictionary so it can be saved as JSON
  todo_string = json.dumps(todo_dict) # convert dict to json string
  print(type(json.dumps(todo_dict)))  
  open_todo_file.write("\n" + todo_string) # wite the task to the file with a new line before it
  #close the file after writing and inform the user the task has been added 
  open_todo_file.close() 
  print("\nTask added successfully!")

def view_tasks():
    """Function for viewing all tasks in the todo_list.json file"""
    open_todo_file = open(TODO_FILE, "r")   # open the to-do file in read mode ("r")
    todo_str = open_todo_file.read().strip('\n')#.split('{')
    
    # Use regex to find all blocks of text that look like a JSON object (anything between { and }) which will give us just a list of task entries
    todo_list = re.findall(r'\{[^}]*\}', todo_str)
    
    # Check if the list is empty
    if len(todo_list) == 0 or (len(todo_list) == 1 and len(todo_list[0]) == 0):
        print("\nYou have zero items in your todo list. \nRun the program again and select option 1, if you would like to add a task")
        open_todo_file.close() #close file before exiting
        return False
    # loop the list of tasks and print each one with numbers
    for i, task in enumerate(todo_list, 1):
        print(f"\n{i}. {task}")
    
    open_todo_file.close()

def remove_task():
"""Function for removing individual tasks from the todo_list.json file"""
    # show the current list of tasks using view_tasks, if there are no tasks it will exit the program

    if not view_tasks():
        exit()

    # open the to-do file in read mode to load all tasks
    open_todo_file = open(TODO_FILE, "r")

    # remove any trailing newline characters
    todo_str = open_todo_file.read().strip('\n')

    #using regex to find all the JSON-style task entries in the file
    todo_list = re.findall(r'\{[^}]*\}', todo_str)

    try:
        # the user can choose which task they want to remove (by number)
        index = int(input("\nEnter task number to remove: "))

        # print debug info (can be removed later)
        print(len(todo_list))  # total number of tasks
        print(index)  # index entered by the user

        # Check if the entered index is valid
        if 0 < index <= len(todo_list):
            index = index - 1  # adjust because list indexes start at 0
            removed_task = todo_list.pop(index)  # Remove the task from the list

            print(f"\nRemoved task: {removed_task}")
            open_todo_file.close()  # Close the file

            # overwrite the file with the updated task list
            open_todo_file = open(TODO_FILE, "w")
            for todo_string in todo_list:
                open_todo_file.write("\n" + todo_string)  # write each task
            open_todo_file.close()  # Close the file after writing
        else:
            # if the entered number is not the correct range
            print("\nInvalid task number.")
    except ValueError:
        # If the user entered something other than a number
        print("\nPlease enter a valid number.")

def leap_year(year: int) -> bool:
    """Check if year is a leap year. Returns True if leap year and False if it isn't"""

    lyear = year % 4 # % returns the remainder of a division and stores it in lyear. Value is either 0 or 1

    if year % 100 == 0:
        if year % 400 == 0:
            return True # If year % 400 == 0 then it's a leap year
        else: # return false
            return False
    else: # Check for regular years if the year isn't a century year
        if lyear == 0:
            return True # If returns 0 then it's a leap year, return True
        else: # any other value in lyear will return false
            return False

def mon_max(month:int, year:int) -> int:
    """Returns the maximum amount of days in a single month. Takes account of leap years"""
    mon_max = { 1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31} # Mapping of months numerically to max days in calendar year 

    is_leap_year = leap_year(year) # Returns True or False if the corresponding year is a leap year
    if is_leap_year:
        mon_max[2] = 29 # this is a leap year
    else:
        mon_max[2] = 28 # this is not a leap year

    return mon_max[month]

def valid_date(date: str) -> bool:
    """Check validity of date and returns True if valid or False if invalid"""
    str_year, str_month, str_day = date.split('-')

    # Check if date have right number of characters
    if len(str_year)!= 4 or len(str_month)!= 2 or len(str_day)!= 2:
        return False

    year = int(str_year)
    month = int(str_month)
    day = int(str_day)
    
    # Check if day is within range
    if day < 1 or day > 31:
        return False

    # Check if month is within range
    if month < 1:
        return False
    elif month > 12:
        return False

    # Check if day is within range for the given month and year
    if day < 1 or day > mon_max(month, year):
        return False


    #TODO: Make sure date is either todays date or future date 

    return True

def main():
    # Define the to-do list for temporary storage access 
    todo_list = []

    if not os.path.isfile(TODO_FILE):
        print(f"{TODO_FILE} does not exist. Created file {TODO_FILE} in current directory")
        todo_file = open(TODO_FILE, "w")
        todo_file.close()



if __name__ == "__main__":
    main()
