def add_task():
  
  open_todo_file = open(TODO_FILE< "a+") # Open file in append, read mode
  
  title = input("Enter Task Title: ")   #Ask user to input Title, description, due_date and priority of the task. 
  
  description = input("Enter Short Description: ")
  
  dute_date = input("Enter due date (YYYY-MM-DD): ")
  
  priority = input("Enter Priority (High/Medium/Low: ").capitalize()
  
  if not valid_date(due_date):  # testing if the user input date and priority is valid
    print("\nInvalid due_date. ")
    
  if priority not in ["High", "Medium", "Low"]: 
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
 
  
