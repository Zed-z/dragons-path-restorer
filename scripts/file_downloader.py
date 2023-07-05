import random
import os
import re
import urllib.request
import time


def main(logs=False):

    urls = []
    for root, dirs, files in os.walk("data/experience"):
        for file in files:
            with open(os.path.join(root, file), "r") as auto:
                try:
                    for line in auto:

                        pattern_html_quote = re.compile(r'"https://dcpcr4l1vpi6d.cloudfront.net/[^\"]*"', re.IGNORECASE)
                        pattern_html_apostrophe = re.compile(r"'https://dcpcr4l1vpi6d.cloudfront.net/[^\']*'", re.IGNORECASE)
                        pattern_css = re.compile(r"url\(https://dcpcr4l1vpi6d\.cloudfront\.[^\)]*\)", re.IGNORECASE)

                        for url in re.findall(pattern_html_quote, line):
                            urls.append(url.replace("\"", "").replace("\\", ""))
                            if logs: print(auto, url.replace("\"", "").replace("\\", ""))

                        for url in re.findall(pattern_html_apostrophe, line):
                            urls.append(url.replace("\'", "").replace("\\", ""))
                            if logs: print(auto, url.replace("\'", "").replace("\\", ""))

                        for url in re.findall(pattern_css, line):
                            urls.append(url.replace("url(", "").replace(")", "").replace("\\", ""))
                            if logs: print(auto, url.replace("url(", "").replace(")", "").replace("\\", ""))

                except UnicodeDecodeError:
                    if logs: print("Encode error!", os.path.join(root, file))

    if logs: print(urls, len(urls))

    errors = []
    for url in urls:
        print(" - Downloading:", url)

        filepath = url.replace("https://dcpcr4l1vpi6d.cloudfront.net", "data/dcpcr4l1vpi6d.cloudfront.net")
        filedir = "/".join(filepath.split("/")[:-1])
        if logs: print(filepath, filedir)

        if not os.path.exists(filepath):
            if not os.path.exists(filedir):
                os.makedirs(filedir, exist_ok=True)

            try:
                urllib.request.urlretrieve(url, filepath)

                sleeptime = random.randint(1, 3) + random.random()
                if logs: print("  - Waiting", sleeptime)
                time.sleep(sleeptime)

            except urllib.error.HTTPError:
                errors.append(url)
        else:
            print("  - Already exists, skipping!")

    print(" - Done! Errors:", list(dict.fromkeys(errors)))


if __name__ == '__main__':
    main(True)
