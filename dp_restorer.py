from scripts import comic_generator
import os
import sys

# Append directory to PATH to load scripts
sys.path.append("scripts")

# Generate comic only if it's not ready yet
if not os.path.exists("data/generator_lock"):
    comic_generator.generate()

# Start the comic
comic_generator.start()
