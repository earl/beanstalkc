# -*- coding: utf-8 -*-
#
import sys, os
sys.path.insert(0, os.path.abspath('..'))
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'beanstalkc'
copyright = u'2011, Andreas Bolka'
version = '0.2'
release = '0.2'
exclude_patterns = ['_build']
pygments_style = 'sphinx'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.viewcode',
]

# -- Options for HTML output ---------------------------------------------------

if on_rtd:
    html_theme = 'default'
else:
    html_theme = 'nature'
#html_last_updated_fmt = '%Y-%m-%d'
html_use_smartypants = True
html_sidebars = {
    '**': [
        'localtoc.html',
        'relations.html',
        'sourcelink.html',
        'searchbox.html',
    ]
}

htmlhelp_basename = 'beanstalkcdoc'


# -- Options for LaTeX output --------------------------------------------------

latex_paper_size = 'a4'
#latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
  ('tutorial', 'beanstalkc.tex',
   u'beanstalkc Tutorial', u'Andreas Bolka',
   'howto'),
]


# -- Options for Epub output ---------------------------------------------------

epub_title = u'beanstalkc Documentation'
epub_author = u'Andreas Bolka'
epub_publisher = u'Andreas Bolka'
epub_copyright = u'2011, Andreas Bolka'
