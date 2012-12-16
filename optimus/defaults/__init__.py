"""
Default template project to use to create a new project
"""
# Directory structure to create
DIRECTORY_STRUCTURE = [
    # list(dir_name[, children_dir_list])
    [
        'sources',
        [
            ['js'],
            ['css'],
            ['scss'],
            ['images'],
            ['templates'],
        ]
    ]
]

# Script template files
# NOTE: Files are rendered with the ``String.format()`` method, so remember to double 
#       all your '{' and '}', else they will be interpreted as format variable, and 
#       probably raise a Key error
SCRIPT_FILES = [
    ['requirements.txt', 'requirements.txt'],
    ['README.rst', 'README.rst'],
    # Default scripts
    ['scripts/init.py', '__init__.py'],
    ['scripts/settings.py', 'settings.py'],
    ['scripts/pages.py', 'pages.py'],
    # Default sources
    ['sources/templates/base.html', 'sources/templates/base.html'],
    ['sources/templates/index.html', 'sources/templates/index.html'],
    ['sources/templates/readme.html', 'sources/templates/readme.html'],
    ['sources/css/screen.css', 'sources/css/screen.css'],
]
