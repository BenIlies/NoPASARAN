import os
import sys
sys.path.insert(0, os.path.abspath('../'))

extensions = [
   'sphinx.ext.duration',
   'sphinx.ext.doctest',
   'sphinx.ext.autodoc',
   'sphinx.ext.autosummary',
   "sphinxawesome_theme"
]

autosummary_generate = True

templates_path = ['templates']

html_theme = "sphinxawesome_theme"