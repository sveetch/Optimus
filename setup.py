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
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Text Processing :: Markup',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'docutils >= 0.9.1',
        'Jinja2 >= 2.6',
        'webassets==0.8',
        'argh==0.24.1',
        'pathtools==0.1.2',
        'watchdog==0.8.3',
        'Babel==1.3.0',
        'yuicompressor >= 2.4.8',
    ],
    entry_points={
        'console_scripts': [
            'optimus-cli = optimus.cli.console_script:main',
        ]
    },
    include_package_data=True,
    zip_safe=False
)