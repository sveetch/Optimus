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
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Text Processing :: Markup',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'docutils==0.9.1',
        'Jinja2>=2.6',
        'webassets==0.8',
        'argparse==1.2.1',
        'argh==0.16.0',
        'pathtools==0.1.2',
        'watchdog==0.6.0',
        'rstview==0.1.2',
        'Babel==1.3.0',
    ],
    scripts=['bin/optimus-cli'],
    include_package_data=True,
    zip_safe=False
)