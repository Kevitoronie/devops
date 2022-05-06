from setuptools import setup, find_packages

def read(filename):
    return[req.strip() for req in open(filename).readlines()]

setup(
    name='padaria',
    version='0.1.0', # m, mi,  f
    description='aplicativo da padaria',
    packages=find_packages(exclude='./venv'),
    include_package_data=True,
    install_requires=read("requeriments.txt"),
    extras_require={"dev":read("requeriments-dev.txt")}
)