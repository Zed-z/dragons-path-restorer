# imports --------------------------------------------------------------------------------------------------------------

import bs4
import shutil
import os

import config


def generate():

	# Define comic names -----------------------------------------------------------------------------------------------

	comic_names = [
		"comic-a-twist-of-fate-1", "comic-days-gone-by-1", "comic-old-haunts-1", "comic-pride-of-kamurocho-1",
		"comic-showdown-at-serena-1", "comic-the-dragons-protege-1", "comic-the-golden-palace-1",
		"comic-the-murder-of-dojima-1", "comic-the-ties-that-bind-part-1-1", "comic-the-ties-that-bind-part-2-1"
	]


	# Copy data folder -------------------------------------------------------------------------------------------------

	print("Making a copy of provided data...")

	if os.path.exists("experience_restored"):
		shutil.rmtree("experience_restored")
	shutil.copytree("data/experience", "experience_restored")


	# Fix site extensions ----------------------------------------------------------------------------------------------

	print("Fixing site extensions...")

	# Comic menu
	os.rename("experience_restored/comic", "experience_restored/comic.html")

	# Comic menu references in index
	with open("experience_restored/index.html") as fr:
		lines = fr.readlines()
	with open("experience_restored/index.html", "w") as fw:
		for line in lines:
			fw.write(line.replace("href=\"comic\"", "href=\"comic.html\""))

	# Comics
	for comic in comic_names:
		os.rename("experience_restored/" + comic, "experience_restored/" + comic + ".html")

	# Comic references in comic menu
	with open("experience_restored/comic.html") as fr:
		comic_data = fr.read()
	with open("experience_restored/comic.html", "w") as fw:
		for comic in comic_names:
			comic_data = comic_data.replace(comic, comic + ".html")
		comic_data = comic_data.replace("href=\"comic\"", "href=\"comic.html\"")
		fw.write(comic_data)

	# Comic cels
	for chid in range(1, 11):
		for pid in range(1, 9):
			for cid in range(1, 5):
				to_rename = "experience_restored/comics/ch{0}/ch{0}-page{1}-cel{2}".format(chid, pid, cid)
				os.rename(to_rename, to_rename + ".html")


	# Remove broken age gates ------------------------------------------------------------------------------------------

	print("Removing broken age gates...")

	for f in ["experience_restored/comic.html", "experience_restored/index.html"]:
		with open(f) as file:
			comicdata = bs4.BeautifulSoup(file.read(), features="html.parser")
		for script in comicdata.findAll("script"):
			if "agegate" in script.text:
				script.extract()
		with open(f, "w") as file:
			file.write(str(comicdata))


	# Add missing fonts ------------------------------------------------------------------------------------------------

	print("Adding missing fonts...")

	if os.path.exists("data/edo-webfont.ttf") and os.path.exists("data/edo-webfont.woff"):
		shutil.copy("data/edo-webfont.ttf", "experience_restored/fonts/edo_regular_macroman/edo-webfont.ttf")
		shutil.copy("data/edo-webfont.woff", "experience_restored/fonts/edo_regular_macroman/edo-webfont.woff")
	else:
		print(" - No font files provided, skipping!")


	# Recover comic pages ----------------------------------------------------------------------------------------------

	print("Recovering comic pages...")

	for comic in comic_names:

		with open("experience_restored/" + comic + ".html") as f:
			comicdata = bs4.BeautifulSoup(f.read(), features="html.parser")

		# Remove age gate
		for script in comicdata.findAll("script"):
			if "agegate" in script.text:
				script.extract()

		# Add missing panels
		comic_wrapper = comicdata.findAll("div", {"class": "swiper-wrapper"})[0]
		comic_panel = comic_wrapper.div

		comic_wrapper.clear()

		idx = 1
		for p in range(1, 9):
			for c in range(1, 5):
				ptext = str(comic_panel)
				cel = bs4.BeautifulSoup(
					ptext.replace("i01", "i0" + str(idx)).replace("page1-cel1", "page" + str(p) + "-cel" + str(c)),
				features="html.parser")
				comic_wrapper.append(cel)

				idx += 1

		# Replace data
		comicdata_write = str(comicdata)
		comicdata_write = comicdata_write.replace("isReady>=4", "isReady>=0")  # Ready cel threshold
		comicdata_write = comicdata_write.replace("=4", "=32")  # Cel count
		comicdata_write = comicdata_write.replace("href=\"comic\"", "href=\"comic.html\"")  # Comic menu references

		# Nav buttons
		comicdata_write = comicdata_write\
			.replace('<a href="javascript:void(0)" class="btn edo idx fx"><i aria-hidden="true" class="fa fa-chevron-left"></i> Page </a>', '<a href="comic.html" class="btn edo idx2 fx"> Back </a>')\
			.replace('<a href="comic-pride-of-kamurocho-2" class="btn edo idx fx"> Page 2 <i class="fa fa-chevron-right"></i></a>', '<a href="comic.html" class="btn edo idx2 fx"> Next </a>')

		with open("experience_restored/" + comic + ".html", "w") as f:
			f.write(str(comicdata_write))


	# Css rules --------------------------------------------------------------------------------------------------------

	if config.css_tweaks:

		print("Adding css rules...")
		with open("experience_restored/css/yakuza.min.css", "a") as fa:

			fa.write(".row.grid .col { opacity: 0.5; pointer-events: none; }")
			fa.write(".row.grid .col:nth-of-type(1) { opacity: 1; pointer-events: auto; }")

			fa.write(".col.pointer { opacity: 0.5; pointer-events: none; }")
			fa.write(".col.pointer:nth-of-type(1) { opacity: 1; pointer-events: auto; }")

			fa.write(".spoiler { display: none !important; }")

			fa.write(".actions { display: none !important; }")

			fa.write("#bottom { display: none !important; }")

			fa.write(".fb, .tw, a[rel=\"fb\"], a[rel=\"tw\"] { display: none !important; }")

			fa.write(".subscribe, .info { display: none !important; }")

			# Button positions
			fa.write("""
				.li_mute {
					position: fixed;
					right: 12em;
					top: 4em;
				}
				.li_home {
					position: fixed;
					right: 4em;
					top: 4em;
				}
				.li_home span {
					font-size: 3em !important;
					line-height: 1.25em !important;
				}
			""")

			# Dark mode
			fa.write("""
				@media(prefers-color-scheme: dark) {
					body { backdrop-filter: invert(); }
					.item.active:not(:hover) .teko { color: white; }
					.onClickCloseModal.close.edo { color: white !important; }
					.loader { background-color: black !important; }
				}
			""")

			# Blur
			fa.write("#modal { background: none !important; backdrop-filter: blur(1em); }")

			# Font size
			fa.write(".teko.regular { font-size: 4em; }")

		# Background fill fix
		with open("experience_restored/comic.html") as file:
			comicdata = bs4.BeautifulSoup(file.read(), features="html.parser")
		body_tag = comicdata.find("body")
		if "style" in body_tag.attrs:
			comicdata.find("body")["style"] += "height: auto !important;"
		else:
			comicdata.find("body")["style"] = "height: auto !important;"
		with open("experience_restored/comic.html", "w") as file:
			file.write(str(comicdata))


	# Download resources locally ---------------------------------------------------------------------------------------

	if config.local_resources:

		print("Downloading resources locally...")

		import file_downloader
		file_downloader.main()


	# Copying local resources ------------------------------------------------------------------------------------------

	if config.local_resources:

		print("Copying local resources...")

		shutil.copytree("data/dcpcr4l1vpi6d.cloudfront.net", "experience_restored/dcpcr4l1vpi6d.cloudfront.net")


	# Updating resource references -------------------------------------------------------------------------------------

	if config.local_resources:

		print("Updating resource references...")

		for root, dirs, files in os.walk('experience_restored'):
			for file in files:
				try:

					with open(os.path.join(root, file), "r") as fr:
						file_data = fr.read()
					with open(os.path.join(root, file), "w") as fw:
						fw.write(file_data.replace("https://dcpcr4l1vpi6d.cloudfront.net/", "/dcpcr4l1vpi6d.cloudfront.net/"))

				except UnicodeDecodeError:
					#print("Encode error!", os.path.join(root, file))
					pass


	# Patching PreloadJS -----------------------------------------------------------------------------------------------

	print("Patching PreloadJS...")

	import patch_preloadjs
	patch_preloadjs.main()


	# Adding redirect --------------------------------------------------------------------------------------------------

	if config.auto_redirect:

		print("Adding automatic comic redirect...")

		with open("experience_restored/index.html") as f:
			index = bs4.BeautifulSoup(f.read(), features="html.parser")

			metatag = index.new_tag('meta')
			metatag.attrs['http-equiv'] = 'refresh'
			metatag.attrs['content'] = '0; url="comic.html'
			index.head.append(metatag)

		with open("experience_restored/index.html", "w") as f:
			f.write(str(index))


	# Ready ------------------------------------------------------------------------------------------------------------

	with open("data/generator_lock", "w") as _:
		pass
	print("Ready!")


def start():

	# Start webserver --------------------------------------------------------------------------------------------------

	print("Starting webserver!")

	from scripts import start_webserver
	start_webserver.main()
