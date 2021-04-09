# GitHub Homework Downloader

## Table of Contents
1. [About](https://github.com/Michael-Hensley/GitHub-Downloader-Capstone#about)
2. [Requirements](https://github.com/Michael-Hensley/GitHub-Downloader-Capstone#requirements)
3. [Usage](https://github.com/Michael-Hensley/GitHub-Downloader-Capstone#usage)
4. [Common Errors](https://github.com/Michael-Hensley/GitHub-Downloader-Capstone#common-errors)
5. [Program Flow](https://github.com/Michael-Hensley/GitHub-Downloader-Capstone#program-flow)

## About
This is a project developed to streamline the process of downloading GitHub projects.  The script navigates to Blackboard using selenium (chrome driver) and downloads a CSV file.  It then parses through the CSV file using pandas to extract out student names and GitHub project links.  The links are then checked for formatting errors and to make sure that the pages exist.  After the invalid links are filtered out, the download portion of the script is then scheduled to run at a user specified time.  Once the time elapses, the links are then loaded using selenium and downloaded.  To prevent naming conflicts, the projects are renamed using the previously mentioned extracted student names.  After all the projects are downloaded, they are then unzipped and placed into their respective folders.  Finally, the selenium webdriver is closed and the leftover zip files are removed.

## Requirements
There are several requirements to use this program *as is*:
- Blackboard account containing test results
- Sufficient storage space
- [Chromedriver](https://chromedriver.chromium.org/downloads) matching your own version of chrome ***must*** be in same directory as the scripts
- Download folder needs to be somewhat close to root directory 
- Download folder needs to be empty before run for best results

## Usage
User needs to fill out the *userInfo* script with their own information.  After doing that, set your desired download time and start the script, thats it! 

## Common Errors
- Path too long error can occur when the zip files are extracted
    - Solution: move download folder closer to root directory or enable long path names in registry
- Pandas can't find the columns to extract
    - Solution: make sure the file headers in the CSV match what pandas is trying to extract
- Chromedriver not found
    - Solution: make sure the chromedriver is the right version and in the same directory as the scripts
- Element not found error in selenium
    - Solution: close other chrome browsers; having multiple open can slow down the browser we are using, causing errors

## Program Flow
![Sequence Diagram](https://github.com/Michael-Hensley/GitHub-Downloader-Capstone/blob/main/Use%20Case%20Github%20Downloader%20-%20GitHub%20Downloader%20Sequence.jpeg)


