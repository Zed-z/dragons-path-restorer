# imports --------------------------------------------------------------------------------------------------------------

import bs4
import shutil
import os


# Define comic names ---------------------------------------------------------------------------------------------------

comic_names = [
	"comic-a-twist-of-fate-1", "comic-days-gone-by-1", "comic-old-haunts-1", "comic-pride-of-kamurocho-1",
	"comic-showdown-at-serena-1", "comic-the-dragons-protege-1", "comic-the-golden-palace-1",
	"comic-the-murder-of-dojima-1", "comic-the-ties-that-bind-part-1-1", "comic-the-ties-that-bind-part-2-1"
]


# Copy data folder -----------------------------------------------------------------------------------------------------

print("Making a copy of provided data...")

if os.path.exists("experience_restored"):
	shutil.rmtree("experience_restored")
shutil.copytree("data/experience", "experience_restored")


# Fix site extensions --------------------------------------------------------------------------------------------------

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

# Comic references in comic menu - FIX THIS
with open("experience_restored/comic.html") as fr:
	comic_data = fr.read()
with open("experience_restored/comic.html", "w") as fw:
	for comic in comic_names:
		comic_data = comic_data.replace(comic, comic + ".html")
	fw.write(comic_data)

# Comic cels
for chid in range(1, 11):
	for pid in range(1, 9):
		for cid in range(1, 5):
			to_rename = "experience_restored/comics/ch{0}/ch{0}-page{1}-cel{2}".format(chid, pid, cid)
			os.rename(to_rename, to_rename + ".html")


# Remove broken age gates ----------------------------------------------------------------------------------------------

print("Removing broken age gates...")

for f in ["experience_restored/comic.html", "experience_restored/index.html"]:
	with open(f) as file:
		comicdata = bs4.BeautifulSoup(file.read(), features="html.parser")
	for script in comicdata.findAll("script"):
		if "agegate" in script.text:
			script.extract()
	with open(f, "w") as file:
		file.write(str(comicdata))


# Add missing fonts ----------------------------------------------------------------------------------------------------

print("Adding missing fonts...")

shutil.copy("data/edo-webfont.ttf", "experience_restored/fonts/edo_regular_macroman/edo-webfont.ttf")
shutil.copy("data/edo-webfont.woff", "experience_restored/fonts/edo_regular_macroman/edo-webfont.woff")


# Recover comic pages --------------------------------------------------------------------------------------------------

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

	with open("experience_restored/" + comic + ".html", "w") as f:
		f.write(str(comicdata).replace("=4", "=32").replace("href=\"comic\"", "href=\"comic.html\""))


# Ready ----------------------------------------------------------------------------------------------------------------

print("Ready!")
