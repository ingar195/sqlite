import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='custom_pip',
    version='0.0.1',
    author='Ingar195',
    author_email='ingar@megarden.no',
    description='Testing installation of Package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ingar195/sqlite',
    project_urls = {
        "Bug Tracker": "https://github.com/ingar195/sqlite/issues"
    },
    license='MIT',
    packages=['custom_pip'],
    install_requires=['sqlite3', 'logging']
)