from scripts import comic_generator
import os

if not os.path.exists("data/generator_lock"):
    comic_generator.generate()

comic_generator.start()
