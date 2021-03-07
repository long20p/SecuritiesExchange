try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


config = {
    'description': 'Trade System',
    'author': 'Long Pham',
    'url': '',
    'download_url': '',
    'author_email': '',
    'version': '0.1',
    'install_requires': [],
    'packages': ['tradesystem'],
    'scripts': [],
    'name': 'tradesystem'
}

setup(**config)
