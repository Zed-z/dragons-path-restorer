# The Dragon's Path Comic Restorer

- A tool that fixes errors in the Yakuza Experience site and lets you read the comic
- Fits all comic panels into single pages instead of them being split into 8 for convenience
- Adds dark mode support and cleans up the design slightly
- Saves required sounds and images locally for 100% offline functionality

# Requirements

- Python 3, preferably added to the system PATH
- Basic file management, terminal and Python usage skills

# Setup

- Obtain and put the required files in the appropriate folders:
  - *Requires* a backed up copy of the website's files in the `data/experience` folder
    - `index.html` should be directly in the `experience` folder alongside files such as `comic-a-twist-of-fate-1`
  - *Optionally* put `edo-webfont.ttf` and `edo-webfont.woff` in the `data` folder
    - Not neccesary to view the comic, only fixes the appearance of buttons
- Edit the `config.py` configuration file to your liking (if you know what you're doing!)
- Open a terminal in the main project directory
- Install required python packages with `pip install -r requirements.txt`
- Run `python3 dp_restorer.py` to prepare files, apply fixes and launch the comic in your browser

# Notes and known issues

- This only fixes the comic, the other features of the Experience site are still non-functional
- Sounds don't work consistently, sometimes you need to click around or mute and unmute to make them play
- If the site doesn't work straight away, refresh a couple of times
