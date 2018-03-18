from setuptools import setup, find_packages

setup(
    name='Optimus',
    version=__import__('optimus').__version__,
    description=__import__('optimus').__doc__,
    long_description=open('README.rst').read(),
    author='David Thenon',
    author_email='sveetch@gmail.com',
    url='http://pypi.python.org/pypi/Optimus',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'six',
        'docutils>=0.9.1',
        'click>=5.1,<6.0',
        'watchdog==0.8.3',
        'Jinja2>=2.6',
        'Babel',
        'webassets',
        'colorama',
        'colorlog',
    ],
    entry_points={
        'console_scripts': [
            'optimus-cli = optimus.cli.console_script:cli_frontend',
        ]
    },
    include_package_data=True,
    zip_safe=False
)