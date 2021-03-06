"""
Uses python3.
Email: dr.mark.schultz@gmail.com
Github: schultzm

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from setuptools import setup, find_packages
import havic

LONG_DESCRIPTION = open("README.md").read()

setup(

    name=havic.__name__,
    version=havic.__version__,
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "havic = havic.__main__:main"
        ]
    },

    description=havic.__description__,
    long_description=LONG_DESCRIPTION,
    classifiers=["Development Status :: 3 - Alpha",
                 "License :: OSI Approved :: GNU Affero General " +
                 "Public License v3 or later (AGPLv3+)",
                 "Programming Language :: Python :: 3.9",
                 "Topic :: Scientific/Engineering :: Bio-Informatics",
                 "Topic :: Scientific/Engineering :: Medical Science Apps.",
                 "Intended Audience :: Science/Research"],
    keywords=["Hepatitis A Virus",
              "transmission",
              "cluster"],
    download_url=havic.__install__,
    author=havic.__author__,
    author_email=havic.__author_email__,
    license=havic.__license__,
    package_data={"": ["*.fa*",
                       "*.gbk",
                       "*.bed",
                       "*.fai",
                       "*.png",
                       "*.svg",
                       "*.tsv"]},
    install_requires=[#see environment.yml for python deps file
    ],
)
