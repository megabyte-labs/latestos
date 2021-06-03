from setuptools import setup, find_packages


setup(
    name='latestos',
    packages=find_packages(),
    version='0.5',
    license='MIT',
    description='Latest OS version checker for Linux Distros using the ' \
                'Arizona Mirror and Windows 10 Insiders Preview',
    author='Renny Montero',
    author_email='rennym19@gmail.com',
    url='https://github.com/rennym19/latestos',
    download_url='https://github.com/rennym19/latestos/archive/v_05.tar.gz',
    keywords=['OS', 'LINUX', 'VERSION', 'CHECKER', 'SCRAPER', 'WINDOWS'],
    install_requires=[
        'requests',
        'lxml',
        'selenium',
    ],
    include_package_data=True,
    entry_points={'console_scripts': ['latestos = latestos.commands:get_latest_os']},
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
