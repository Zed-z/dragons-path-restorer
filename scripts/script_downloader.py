import os
import urllib.request
import pathlib
import shutil


def url_to_filename(url):
	return url.replace("/", "_").replace(":", "_").replace(",", "_").replace("?", "_").replace("=", "_")\
		+ (".css" if "Teko" in url else "")


def main(log=False):

	# TODO: The font css files have their own downloads

	# Download scripts
	urls = ["https://code.createjs.com/preloadjs-0.6.2.min.js",
			"//code.jquery.com/jquery-latest.min.js",
			"https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js",
			"http://cdnjs.cloudflare.com/ajax/libs/gsap/latest/TweenMax.min.js",
			"https://cdnjs.cloudflare.com/ajax/libs/gsap/latest/TweenMax.min.js",
			"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js",
			"https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js",

			"https://opensource.keycdn.com/fontawesome/4.7.0/font-awesome.min.css",
			"https://fonts.googleapis.com/css?family=Teko:400,500,600",

			"https://fonts.gstatic.com/s/teko/v20/LYjYdG7kmE0gV69VVPPdFl06VN8XG4S11zY.ttf",
			"https://fonts.gstatic.com/s/teko/v20/LYjYdG7kmE0gV69VVPPdFl06VN8lG4S11zY.ttf",
			"https://fonts.gstatic.com/s/teko/v20/LYjYdG7kmE0gV69VVPPdFl06VN_JHIS11zY.ttf"
		]
	urls_fixed = [("/css/" if "css" in url else ("/fonts/" if "ttf" in url else "/js/")) + url_to_filename(url.split("//")[-1]) for url in urls]
	filenames = ["data/" + url_to_filename(url.split("//")[-1]) for url in urls]
	filenames_final = ["experience_restored" + ("/css/" if "css" in url else ("/fonts/" if "ttf" in url else "/js/")) + url_to_filename(url.split("//")[-1]) for url in urls]

	for i in range(len(urls)):
		if not os.path.exists(filenames[i]):
			u = urls[i]
			fn = filenames[i]

			# Fix a dead link by replacing it with a different one
			if u == "https://opensource.keycdn.com/fontawesome/4.7.0/font-awesome.min.css":
				u = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"

			urllib.request.urlretrieve(u if (u.startswith("https:") or u.startswith("http:")) else "https:" + u, fn)

			# Patch an issue in the script (PreloadJS only)
			if "preloadjs" in u:
				with open(fn) as f: fixed_text = f.read().replace("b(_this._tag)", "b(this._tag)")
				with open(fn, "w") as f: f.write(fixed_text)

			# Patch Teko font files)
			if "Teko" in u:
				with open(fn) as f: fixed_text = f.read().replace("https://fonts.gstatic.com/s/teko/v20/", "/fonts/fonts.gstatic.com_s_teko_v20_")
				with open(fn, "w") as f: f.write(fixed_text)

		# Copy the script to its destination
		shutil.copyfile(filenames[i], filenames_final[i])

	# Replace references to scripts
	data_path = pathlib.Path("experience_restored").rglob("*")
	for item in data_path:
		if item.is_file():
			if log: print(item)
			try:

				with open(item) as f: text = f.read()

				fixed_text = text
				for i in range(len(urls)):
					u = urls[i]
					uf = urls_fixed[i]

					if log:
						print("Finding", u, fixed_text.find(u))

					fixed_text = fixed_text.replace(u, uf)

				if text != fixed_text:
					if log: print("Fixed scripts!")
					with open(item, "w") as f: f.write(fixed_text)

			except:
				if log: print("An error happened, this should be fine to ignore.")


if __name__ == '__main__':
	main(True)
