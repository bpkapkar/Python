import os
import shutil
import pandas as pd
data = pd.read_csv('filename.csv',header=None)
print("Developed by Bhushan Kapkar 9028434644")
b = list(data.iloc[:,0])
mydir = input("Source path: ")
destination = input("Destination Path: ")
print("Processing")
for (path , folder, files) in os.walk(mydir):
    for file in files:
        for i in b:
            if i== file:
                path_file = os.path.join(path,file)
                shutil.copy(path_file,destination)
            else:
                continue
print("Task Completed")


