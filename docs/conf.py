import os
import sys
sys.path.insert(0, os.path.abspath('../'))

# Get the current directory
current_directory = os.getcwd()

# List the contents of the current directory
directory_contents = os.listdir(current_directory)

# Print the directory contents
for item in directory_contents:
    print(item)

extensions = [
   'sphinx.ext.duration',
   'sphinx.ext.doctest',
   'sphinx.ext.autodoc',
   'sphinx.ext.autosummary'
]

autosummary_generate = True

templates_path = ['templates']