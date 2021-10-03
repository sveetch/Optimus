"""
Manifest for basic template project
"""
# Directory structure to create
DIRECTORY_STRUCTURE = [
    # list(dir_name[, children_dir_list])
    [
        'project',
        [
            [
                'sources',
                [
                    ['js'],
                    ['css'],
                    ['scss'],
                    ['images'],
                    ['templates'],
                ],
            ],
        ]
    ],
]

# The directory name that contains 'sources' (assets, templates, images, etc..)
# in the template project
SOURCES_FROM = 'sources'

# The directory name that will contains 'sources' in the new created projects
SOURCES_TO = "project/sources"

# Default sources files or directory to copy within the new project
# sources directory
# The sync task is performed before the script writing task
FILES_TO_SYNC = (
    # (SOURCE, DESTINATION)
    ('js', 'js'),
    ('css', 'css'),
    ('scss', 'scss'),
    ('templates', 'templates'),
)

# Script template files
SCRIPT_FILES = [
    ['README.rst', 'README.rst'],
    # Default scripts
    ['scripts/Makefile.tpl', 'Makefile'],
    ['scripts/requirements.txt.tpl', 'requirements.txt'],
    ['scripts/gitignore.tpl', '.gitignore'],
    ['scripts/settings.json.tpl', 'settings.json'],
    ['scripts/__init__.py.tpl', 'project/__init__.py'],
    ['scripts/settings__init__.py.tpl', 'project/settings/__init__.py'],
    ['scripts/pages.py.tpl', 'project/pages.py'],
    ['scripts/settings.py.tpl', 'project/settings/base.py'],
    ['scripts/prod_settings.py.tpl', 'project/settings/production.py'],
]
