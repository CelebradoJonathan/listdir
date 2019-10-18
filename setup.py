import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="listdir",
    version="0.0.1",
    author="CelebradoJonathan",
    description="A package for listdir",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CelebradoJonathan/listdir/tree/with-date-filename",
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
    entry_points={
        'console_scripts':['listdir=listdir_pkg.listdir:main'],
    },
    include_package_data = True,
)