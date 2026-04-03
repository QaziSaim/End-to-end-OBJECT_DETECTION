from setuptools import setup, find_packages

setup(
    name="bone-fracture-detection",
    version="0.0.1",
    author="Saim Qazi",
    author_email="kazisahim121@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"":"src"},
    install_requires=[]

)