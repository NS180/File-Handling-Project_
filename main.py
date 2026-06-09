# libraries needed
from pathlib import Path
import os
def createfile():
    try:
        name = input("Tell your file name: ")
        path = Path(name)
        if not path.exists():
            with open(path, "w") as file:
                data = input("Write inside your file: ")
                file.write(data)
            print("File created successfully!")
        else:
            print("Error name already exists")         
    except Exception as err:
        print("Some error occured as{err}")

def readfile():
    try:
        name = input("\nTell your file name: ")
        path = Path(name)
        if path.exists():
            with open(path, "r") as file:
                content = file.read()
                print(f"Your file content is \n {content}")
        else:
            print("Sorry, No such file exists") 
    except Exception as err:
        print("Some error occured as {err}")
                
def updatefile():
    try:
        name = input("\nTell your file name: ")
        path = Path(name)
        if path.exists():
            print("operations: ")
            print("1 . Renaming the file")
            print("2 . Appending the file")
            print("3 . Overwriting the file")

            choice = int(input("Enter the operation: "))
            if choice == 1:
                newname = input("\n Tell new file name: ")
                new_path = Path(newname)
                if not new_path.exists():
                    path.rename(new_path)
                    print("File renamed successfully")
                else:
                    print("File already exists")
            elif choice == 2:
                with open(path, 'a') as file:
                    data = input("What do you want to append: ")  #for appending
                    file.write("\n" + data)
                print("Successfully appended!")
            elif choice == 3:
                with open(path, "w") as file:
                    data = input("Write in your file: ")
                    file.write("\n" + data)
                print("Overwritten successfully!")            

    except Exception as err:
        print("An error occured as {err}")                 

def deletefile():
    try:

        name = input("\n Tell your file name: ")
        path = Path(name)
        if path.exists():
            path.unlink()   
            print("File deleted successfully!")
        else:
            print("No such file exists")
    except Exception as err:
        print("An error occured as {err}")             

print("press 1 for creating a file")
print("press 2 for reading a file")
print("press 3 for updating a file")
print("press 4 for deleting a file")

a = int(input("\ntell your response: "))

if a == 1:
    createfile()
if a == 2:
    readfile()
if a == 3:
    updatefile()
if a == 4:
    deletefile()            
    