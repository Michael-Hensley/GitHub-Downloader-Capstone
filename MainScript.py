from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import os
import schedule
from colorama import Fore as textColor, Style
from userInfo import New_Download_Directory, Default_Download_Directory

#Function to check whether the user entered a valid number
def checkInput(message, myList):
    while True:
        try:
            userInput = int(input(message))
            if(userInput >= len(myList) or userInput < 0):
                raise ValueError
        except ValueError:
            print("Invalid Option")
            continue
        else:
            return userInput 
#Function navigates BB to download CSV file
def getCSVFile(driver):
    
    from userInfo import BB_User, BB_Pw
    print(textColor.RED,"Downloading CSV file", Style.RESET_ALL)

    driver.get("https://bb.nsuok.edu/ultra/stream")

    driver.find_element_by_id("username").send_keys(BB_User)
    driver.find_element_by_id("password").send_keys(BB_Pw, Keys.ENTER)

    driver.get("https://bb.nsuok.edu/webapps/gradebook/do/instructor/downloadGradebook?dispatch=viewDownloadOptions&course_id=_51855_1") #BB gradebook download page

    driver.find_element_by_id("downloadByColumn").click() #Specifies downloading of an individual assignment

    select_box = driver.find_element_by_xpath('//*[@id="item"]') #Finds dropbox with potential assignments

    options = [x for x in select_box.find_elements_by_tag_name("option")]
    for positionInList, item in enumerate(options):                         #Extracts the text from the options and shows them to the user
        print (f"({positionInList}) {item.text}")

    userSelection = checkInput("Select an assignment to download: ", options) #Asks user which file they would like to download

    driver.find_element_by_xpath(f'//*[@id="item"]/option[{userSelection + 1}]').click() #Uses list index + 1 to specify the file name by xpath

    driver.find_element_by_xpath('//*[@id="delimiterComma"]').click() #Click CSV option
    driver.find_element_by_xpath('//*[@id="bottom_Submit"]').click() #Submit download request
    driver.find_element_by_xpath('//*[@id="download_form"]/a').click() #Downloads assignment

    waitForFile = True
    fileName = ""

    while (waitForFile):
        for file in os.listdir(New_Download_Directory):
            if (".csv" in file and ".crdownload" not in file): #Waits for file to be created before continuing, without this the next function would not be able to 
                waitForFile = False                            #function since it would not be able to find a completed file.  Also finds the newly created file 
                fileName = file                                 
            else:
                waitForFile = True

    print(textColor.GREEN, "Downloading CSV file")
    print(Style.RESET_ALL)   

    return (f"{New_Download_Directory}\\{fileName}") #Returns the file path to be used by the CSV parser
#Function parses through CSV, extracting and formatting student links and names
def getCSVInfo(myCSVFile):
    import pandas
    print(textColor.RED,"Extracting CSV info", end = "\r")

    CSV_info = pandas.read_csv(myCSVFile, header = 0)

    names =[row for row in CSV_info["Last Name"] + " " + CSV_info["First Name"]] #Extracts first and last name from pandas dataframe object.
    links = [row for row in CSV_info["Answer 1"]] #Extracts Answer 1 column from pandas dataframe object
    fileNames = []

    for positionInList, item in enumerate(links):
        try:
            startIndex = item.index('"') + (1) #returns the first position of (")
            endingIndex = item.rindex('"') #returns the second position of (")
            links.pop(positionInList) #Removes old unformatted link
            links.insert(positionInList, item[startIndex : endingIndex]) #Adds formatted link into old list

            positionOfSlash = item.rindex('/', 0, endingIndex) #Finds slash to the left of the (")
            assignmentName = item[positionOfSlash + 1 : endingIndex] #Finds assignment to the left of the (")

            #Sometimes links would have a '/' at the end, causing the assignmentName to be recorded as a blank string
            if(assignmentName == ''):
                positionOfSlash = item.rindex('/', 0, endingIndex - 1) #Finds slash to the left of the (")
                assignmentName = item[positionOfSlash + 1 : endingIndex - 1] #Finds assignment to the left of the (")

            #if statements to extract out unwanted or problematic strings in file names.
            if(".git" in assignmentName):
                assignmentName = assignmentName.replace(".git","") 
            if("#" in assignmentName):
                positionOfCharacter = assignmentName.rindex("#")
                assignmentName = assignmentName[0:positionOfCharacter]

            fileNames.insert(positionInList, assignmentName) #adds assignment name to a list

        except ValueError: #No quotes found, assumed no need to format, keeps original link
            positionOfSlash = item.rindex('/', 0) #Finds slash without the need to end at (")
            assignmentName = item[positionOfSlash + 1 : ] #Finds assignment name without the need to end at (")
            fileNames.insert(positionInList, assignmentName) #adds assignment name to a list

    print(textColor.GREEN, "Extracting CSV info")
    print(Style.RESET_ALL)
    
    return (names, links, fileNames)
#Function downloads assignments
def downloadGitHubFiles(student_names, student_links, driver, downloaded_file_names):
    
    for positionInList, link in enumerate(student_links):
        print(textColor.RED,f"Downloading Github Files ({positionInList + 1}/{len(student_links)})", end = "\r")
        nameOfFileMain = New_Download_Directory + "\\" + downloaded_file_names[positionInList] + '-main.zip'
        nameOfFileMaster = New_Download_Directory + "\\" + downloaded_file_names[positionInList] + '-master.zip'
        newFileName = New_Download_Directory + "\\" + student_names[positionInList] + "-" + downloaded_file_names[positionInList] + ".zip"

        if (os.path.exists(newFileName)):
            print(f"Duplicate file: {newFileName}")
            continue
        else:
            driver.get(link)
            downloadButton = driver.find_element_by_xpath('//*[@id="repo-content-pjax-container"]/div/div[2]/div[1]/div[1]/span/get-repo/details/summary')
            downloadButton.click()
            downloadLink = driver.find_element_by_xpath('//*[@id="repo-content-pjax-container"]/div/div[2]/div[1]/div[1]/span/get-repo/details/div/div/div[1]/ul/li[2]/a')
            downloadLink.click()

            timeoutAfter = time.time() + 300
            while(not(os.path.exists(nameOfFileMain) or os.path.exists(nameOfFileMaster))):
                if(time.time()>timeoutAfter):
                    print(newFileName + "Timedout")
                    break
                continue
            
            if(os.path.exists(nameOfFileMain)):
                renameFile(nameOfFileMain, newFileName)
            elif(os.path.exists(nameOfFileMaster)):
                renameFile(nameOfFileMaster, newFileName)
            
    print(textColor.GREEN, f"Downloading Github Files ({positionInList + 1}/{len(student_links)})", end = "\r")
    print(Style.RESET_ALL)
#Function sets up a web driver for chrome
def enable_download_headless():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_experimental_option("prefs", {
            "download.default_directory": Default_Download_Directory, 
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False 
    })
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging']) #Turns off annoying messages
    driver = webdriver.Chrome(options=chrome_options) #initialize chrome options
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': New_Download_Directory}} 
    driver.execute("send_command", params)

    driver.implicitly_wait(10) #Set a wait time of 10 seconds 

    return driver #Returns a driver that is setup for headless browsing
#Renames old file to be inclusive of student names
def renameFile(old, new): 
    while(not os.path.exists(new)):
        os.replace(old, new)
        time.sleep(0.5) 
    
    if(os.path.exists(old)): # process is fast and sometimes leaves a residual file, this removes it.
        os.remove(old)
#Shows the user the entries that are unable to be downloaded
def showBrokenLinks(broken_Links):
    print ("(Name, Issue, Link)")
    for link in broken_Links:
        print(f"{link[0]}, {link[1]}, {link[2]}")
    print(Style.RESET_ALL)
#Error handling that checks if the link is a valid webpage and if the link contains a download button
def checkLinks(links, names, assignment_names, driver):
    errorWithLink = []

    for positionInList, link in enumerate(links):
        print(textColor.RED,f"Checking links ({positionInList + 1}/{len(links)})", end = "\r")
        try:
            driver.get(link)
            #print(link)
            if ("Page not found" in driver.title):
                errorWithLink.append((  names[positionInList], "Page Not Found", links[positionInList], positionInList))
            else:
                findButton = driver.find_element_by_xpath('//*[@id="repo-content-pjax-container"]/div/div[2]/div[1]/div[1]/span/get-repo/details/summary')
                findButton.click()
        except NoSuchElementException:
            errorWithLink.append((names[positionInList],"Download Button Not Found", links[positionInList], positionInList))

    print(textColor.GREEN, f"Checking links ({(positionInList + 1) - len(errorWithLink)}/{len(links)})")
    print(Style.RESET_ALL)

    return errorWithLink
#Removes broken links from download Queue
def removeBrokenLinks(links, names, assignment_names, broken_Links):
    print(textColor.RED,"Removing broken links", end = "\r")
    time.sleep(2)
    for link in reversed(broken_Links):
        links.pop(link[3])
        names.pop(link[3])
        assignment_names.pop(link[3])

    print(textColor.GREEN, f"Removed {len(broken_Links)} broken links")
    print(Style.RESET_ALL)
#unzips all zip files in download folder
def unzipFiles():
    from zipfile import ZipFile as ZF

    for file in os.listdir(New_Download_Directory):
        if(".zip" in file):
            with ZF(f"{New_Download_Directory}\\{file}", 'r') as myZip:

                folderName = file.replace(".zip", "")
                posOfHyphen = file.index('-')           #Sets name of extraced files based on zip name, not what is contained inside zip
                folderName = file[:posOfHyphen]

                myZip.extractall(f"{New_Download_Directory}\\{folderName}")
#Removes zip files 
def removeZipFiles():
    for file in os.listdir(New_Download_Directory):
        if(".zip" in file):
            os.remove(f"{New_Download_Directory}\\{file}")
#Function that contains our call to download files
def startScript():

    headlessDriver = enable_download_headless() #Sets up and returns the loaded driver
    downloadGitHubFiles(studentNames, studentLinks, headlessDriver, downloadedFileNames) #Takes the lists and iterates through them in parallel, downloading GitHub files
    headlessDriver.quit() #Closes the headless webdriver

    global doSomething 
    doSomething = False

if __name__ == "__main__":
    headlessDriver = enable_download_headless() #Loads webdriver 

    CSVPath = getCSVFile(headlessDriver) #Navigates to BB and downloads the CSV file containing student information

    studentNames, studentLinks, downloadedFileNames = getCSVInfo(CSVPath) #Parse through the downloaded CSV file and creating lists for names, links, and assignment names

    linksWithErrors = checkLinks(studentLinks, studentNames, downloadedFileNames, headlessDriver) #Checks links for browser issues

    removeBrokenLinks(studentLinks, studentNames, downloadedFileNames, linksWithErrors)

    showBrokenLinks(linksWithErrors) #Show links with errors 

    headlessDriver.quit() #Closes driver 

    schedule.every().sunday.at("00:01").do(startScript) #Schedule function call at specified time, uses 24 hr format  EX. "05:30", "13:59", "22:05"

    print("Script Scheduled\n")

    doSomething = True
    while(doSomething): 
        schedule.run_pending() 
        time.sleep(1)

    unzipFiles()
    removeZipFiles()