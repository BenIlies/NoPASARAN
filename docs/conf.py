import os
import sys
import sphinx_pdj_theme
sys.path.insert(0, os.path.abspath('../'))

html_theme = 'sphinx_pdj_theme'
html_theme_path = [sphinx_pdj_theme.get_html_theme_path()]

extensions = [
   'sphinx.ext.duration',
   'sphinx.ext.doctest',
   'sphinx.ext.autodoc',
   'sphinx.ext.autosummary'
]

autosummary_generate = True

templates_path = ['templates']