tsv-sulzfeld-plone
==================

    $ virtualenv --no-site-packages venv
    $ rm plone-python/
    $ source venv/bin/activate
    $ pip install pil
    $ python bootstrap.py
    $ bin/buildout
    $ bin/instance fg 
