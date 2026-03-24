from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="spyn",
    version="2.0.0",
    author="Jefferson Richard Dias da Silva, Luiz Henrique Keng Queiroz Junior",
    author_email="lhkengqueiroz@ufg.br",
    description="GUI platform for NMR crystallography workflows (GIPAW/GIAO/Conformer Search)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jeffrichardchemistry/spyn",
    package_dir={"": "code"},
    packages=find_packages(where="code"),
    python_requires=">=3.9",
    install_requires=[
        "PyQt5>=5.12",
        "pandas>=0.25",
        "numpy>=1.17",
        "scipy>=1.3",
        "matplotlib>=3.1",
    ],
    entry_points={
        "console_scripts": ["spyn=spyn.spyn_main:main"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Physics",
        "Intended Audience :: Science/Research",
    ],
)
