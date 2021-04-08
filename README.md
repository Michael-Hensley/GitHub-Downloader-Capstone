# GitHub Homework Downloader

## About
This is a project developed to streamline the process of downloading GitHub projects.  The script navigates to Blackboard using selenium (chrome driver) and downloads a CSV file.  It then parses through the CSV file using pandas to extract out student names and GitHub project links.  The links are then checked for formatting errors and to make sure that the pages exist.  After the invalid links are filtered out, the download portion of the script is then scheduled to run at a user specified time.  Once the time elapses, the links are then loaded using selenium and downloaded.  To prevent naming conflicts, the projects are renamed using the previously mentioned extracted student names.  After all the projects are downloaded, they are then unzipped and placed into their respective folders.  Finally, the selenium webdriver is closed and the leftover zip files are removed.

## Requirements
There are several requirements to use this program *as is*:
- Blackboard account containing test results
- Sufficient storage space
- [Chromedriver](https://chromedriver.chromium.org/downloads) matching your own version of chrome ***must*** be in same directory as the scripts
- Download folder needs to be somewhat close to root directory to avoid path name too long error
- Download folder needs to be empty before run for best results

## Usage
User needs to fill out the *userInfo* script with their own information.  After doing that, set your desired download time and start the script, thats it!  

