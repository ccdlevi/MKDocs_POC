"""
Setup script to install the MkDocs Confluence Publisher plugin locally.
"""

from setuptools import setup, find_packages

setup(
    name='mkdocs-confluence-publisher-local',
    version='1.0.0',
    description='MkDocs plugin for publishing to Confluence',
    py_modules=['mkdocs_confluence_publisher'],
    install_requires=[
        'mkdocs>=1.0',
        'requests',
        'python-dotenv',
        'markdown',
    ],
    entry_points={
        'mkdocs.plugins': [
            'confluence_publisher = mkdocs_confluence_publisher:ConfluencePublisherPlugin',
        ]
    },
    python_requires='>=3.6',
)
