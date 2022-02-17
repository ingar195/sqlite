import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='sqlite',
    version='0.0.1',
    author='ingar195',
    author_email='ingar@megarden.no',
    description='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ingar195/sqlite',
    project_urls = {
        "Bug Tracker": "https://github.com/ingar195/sqlite/issues"
    },
    license='MIT',
    packages=['sqlite'],
    install_requires=[""]
)