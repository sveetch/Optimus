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

# The directory name that contains 'sources' (assets, templates, images, etc..)
# in the template project
SOURCES_FROM = 'sources'

# The directory name that will contains 'sources' in the new created projects
SOURCES_TO = SOURCES_FROM

# Default sources files or directory to synchronize within the new project
# sources directory
# The sync task is performed before the writing task
FILES_TO_SYNC = (
    # (SOURCE, DESTINATION)
    ('js', 'js'),
    ('css', 'css'),
    ('scss', 'scss'),
    ('templates', 'templates'),
)

# Directory that contain message catalog file structure to copy to the project
LOCALE_DIR = "locale"

# Script template files
SCRIPT_FILES = [
    ['README.rst', 'README.rst'],
    # Default scripts
    ['scripts/Makefile.tpl', 'Makefile'],
    ['scripts/requirements.txt.tpl', 'requirements.txt'],
    ['scripts/babel.cfg.tpl', 'babel.cfg'],
    ['scripts/settings.json.tpl', 'settings.json'],
    ['scripts/gitignore.tpl', '.gitignore'],
    ['scripts/__init__.py.tpl', '__init__.py'],
    ['scripts/settings.py.tpl', 'settings.py'],
    ['scripts/prod_settings.py.tpl', 'prod_settings.py'],
    ['scripts/pages.py.tpl', 'pages.py'],
]
