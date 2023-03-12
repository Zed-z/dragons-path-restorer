# The Dragon's Path Comic Restorer

-   A tool that fixes errors in the Yakuza Experience site and lets you read the comic
-   Fits all comic panels into single pages instead of them being split into 8 for convenience

# Requirements

-   Python 3 with BeautifulSoup4 installed
-   Requires a backed up copy of the website's files in the `data/experience` folder (`index.html` should be directly in the `experience` folder)
-   Requires putting `edo-webfont.ttf` and `edo-webfont.woff` in the `data` folder
-   Requires basic Python usage skills

# Setup

-   Obtain and put the required files in the appropriate folders
-   Run the `comic-generator.py` script to prepare files and apply fixes
-   Start the web server using `start-webserver.py` or a tool of your choice
-   If it doesn't work straight away, refresh a couple of times

# Note

-   This only fixes the comic, the other features of the Experience site are still non-functional
