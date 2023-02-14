import os
import setuptools

def requirements():
    with open(os.path.join(os.path.dirname(__file__), "requirements.txt"), encoding="utf-8") as f:
        return f.read().splitlines()

setuptools.setup(
    name="default-scraper",
    version="1.1.1",
    license="MIT",
    author="Seongbum Seo",
    author_email="sbumseo@bigpicture.team",
    description="Web Scraper",
    long_description=open("README.md").read(),
    url="https://github.com/bigpicture-kr/default-scraper",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={
        "default_scraper": ["drivers/chromedriver"],
    },
    zip_safe=True,
    install_requires=requirements(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)
