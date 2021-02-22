from distutils.core import setup
from setuptools import find_packages


setup(
    name='latestos',
    packages=find_packages(),
    version='0.2',
    license='MIT',
    description='Latest OS version checker for Linux Distros using the Arizona Mirror',
    author='Renny Montero',
    author_email='rennym19@gmail.com',
    url='https://github.com/rennym19/latestos',
    download_url='https://github.com/rennym19/latestos/archive/v_02.tar.gz',
    keywords=['OS', 'LINUX', 'VERSION', 'CHECKER', 'SCRAPER'],
    install_requires=[
        'requests',
        'lxml',
    ],
    entry_points={'console_scripts': ['latestos = latestos.commands:main']},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
