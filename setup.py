from distutils.core import setup

setup(
    name = 'casio-registrations',
    version = '1.6',
    description = 'For reading and writing Casio registration bank (.RBK) files',
    long_description = open('README.md').read(),
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/michgz/casio-registrations',
    classifiers =
        ['Programming Language :: Python :: 3',
         'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
         'Operating System :: OS Independent' ],
    license = 'LGPLv2+',
    packages = ['casio_rbk'],
    package_data = {'casio_rbk': ['patch_data/CT-X5000 tone.csv', 'patch_data/README.md']}
)
