# Import 
import os
from xmlrpc.client import DateTime
import zipfile
import shutil
from datetime import datetime
import pandas as pd

# get all the files in a specific directory
def getFiles(directory):
    files = [f for f in os.listdir(directory)]
    return files

# check for zip/.zip file
def checkFile(directory,files,extension):
    for f in files :
        if(f.endswith(directory + extension) and (f.endswith(extension) or f.endswith("."+extension))):
            return f;

# Get file name after extracting
def newFolderName(files,directory):
    newFiles = [f for f in os.listdir(directory)]
    for f in newFiles:
        if f not in files:
            return f;
    return ""

# Patch Zip
def patchZip(file):
    file = file[0:len(file)-3]
    os.rename(file+"zip",file+".zip")
    return file+".zip"

# Extract Zip
def extractZip(fileName):
    with zipfile.ZipFile(fileName,"r") as zip_ref:
        zip_ref.extractall(".")

# Check for a specific file/tags
def checkFile(fileTag,extension,fileArray):
    files = []
    for f in fileArray:
        if(fileTag and fileTag.lower() not in f.lower()):
            continue
        if(f.endswith(extension)):
            if((fileTag != "RESUMES" and f != "RESUMES.zip") or (fileTag == "RESUMES" and f == "RESUMES.zip")):
                files.append(f);
    return files;

def zipper(resumeFolder,fileName):
    with zipfile.ZipFile(fileName, 'w') as zipObj:
        for folderName, subfolders, filenames in os.walk("./"+resumeFolder):
            for filename in filenames:
                filePath = os.path.join(folderName, filename)
                zipObj.write(filePath, os.path.basename(filePath))

# Print Array
def show(fileArray):
    for f in fileArray:
        print(f)

def printDivider():
    print("\n\n----------------------------------------------------\n\n")

files = getFiles(".")

zipFile = checkFile("","zip",files)

resumeFolder = ""

resumes = []

if(len(zipFile)):
    zipFile = zipFile[0]
    print("Found zip file: " + zipFile + "\n")
    if(not zipFile.endswith(".zip")): 
        print("Patching broken zip ....\n")
        zipFile = patchZip(zipFile)
        print("Zip file patched successfully\n")

    print("Extracting zip ....\n")
    extractZip(zipFile)
    print("Zip extracted successfully !")
    
    printDivider()

    resumeFolder = newFolderName(files,".")
    date = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    shutil.move(resumeFolder,resumeFolder + "-" + date)
    resumeFolder = resumeFolder + "-" + date

    resumes = getFiles("./"+resumeFolder)
    print("Found "+ str(len(resumes)) + " resumes\n")
    show(resumes)

else :
    print("No zip file found !")
    exit()

printDivider()

requiredResumes = []

resumeCSV = checkFile("resumes","csv",files)

if(len(resumeCSV) == 0) :
    print("resumes.csv not found  :(")
    print("Enter the Name/Roll no of the resumes of the candidates\nType 0 and press enter to stop the extraction\n")
    while(1):
        userInput = input()
        if(userInput == "0"):
            break
        requiredResumes.append(userInput)

else :
    resumeCSV = resumeCSV[0]
    print("Found : " + resumeCSV + "\n")
    print("Extracting resumes.csv ....\n")
    CSVReader = pd.read_csv(resumeCSV)
    for row in CSVReader.Resumes:
        requiredResumes.append(row)
    print("Extraction Success !!")
    print("\nTrying to fetch " + str(len(requiredResumes)) + " resumes : ")
    show(requiredResumes)

if(os.path.isdir("RESUMES_LIST")):
    shutil.rmtree("RESUMES_LIST")

os.mkdir("RESUMES_LIST")

resumesMoved = []
resumesNotFound = []
resumesFound = []
duplicates = 0

for res in requiredResumes: 
    matchingFiles = checkFile(res,"",resumes)
    for match in matchingFiles:
        shutil.copy2("./"+resumeFolder+"/"+match,"./RESUMES_LIST")
        resumesMoved.append(match)
    if(len(matchingFiles) == 0):
        resumesNotFound.append(res)
    else :
        resumesFound.append(res)
        if(len(matchingFiles) > 1):
            duplicates=duplicates + 1
        resumesMoved.append("")

printDivider()

if(len(resumesFound) > 0):
    print("Resumes Found : \n")
    show(resumesFound)
else :
    print("No Resumes Found :(")

printDivider()

if(len(resumesNotFound) > 0):
    print("Resumes Not Found : \n")
    show(resumesNotFound)
else :
    print("All the specified resumes are found !!")

printDivider()

if(len(resumesMoved) > 0):
    print("Resumes List Which are moved : \n")
    show(resumesMoved)
else :
    print("No Resumes Moved")

print("\n"+str(duplicates)+" duplicates found")

printDivider()

print("Checking if a past RESUMES.zip file is present")

resumesZip = checkFile("RESUMES","zip",files)

if(len(resumesZip) > 0):
    print("Found file " + resumesZip[0])
    print("\nRemoving pre-existing RESUMES.zip")
    os.remove(resumesZip[0])
    print("\nRemoved pre-existing RESUMES.zip")

print("\nZipping resumes ....")
zipper("RESUMES_LIST","RESUMES.zip")
print("\nZipping Success !!!")
print("\nYou can find all the resumes in RESUMES.zip")

printDivider()

print("Program Terminated ..")

printDivider()
