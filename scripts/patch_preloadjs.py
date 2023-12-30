import os
import urllib.request
import pathlib
import shutil


def main(log=False):

	# Download PreloadJS
	url = "https://code.createjs.com/preloadjs-0.6.2.min.js"
	filename = "data/preloadjs-0.6.2.min.js"
	filename_final = "experience_restored/js/preloadjs-0.6.2.min.js"

	if not os.path.exists(filename):
		urllib.request.urlretrieve(url, filename)

		# Patch an issue in the script
		with open(filename) as f: fixed_text = f.read().replace("b(_this._tag)", "b(this._tag)")
		with open(filename, "w") as f: f.write(fixed_text)

	# Copy the script to its destination
	shutil.copyfile(filename, filename_final)

	# Replace references to the script
	data_path = pathlib.Path("experience_restored").rglob("*")
	for item in data_path:
		if item.is_file():
			if log: print(item)
			try:
				with open(item) as f: text = f.read()
				fixed_text = text.replace("https://code.createjs.com/preloadjs-0.6.2.min.js", "/js/preloadjs-0.6.2.min.js")
				if text != fixed_text:
					if log: print("FIXED")
				with open(item, "w") as f: f.write(fixed_text)
			except:
				if log: print("An error happened, this should be fine to ignore.")


if __name__ == '__main__':
	main(True)
