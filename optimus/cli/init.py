# -*- coding: utf-8 -*-
"""
Command line action to start a new project
"""
import datetime, os
from string import letters, digits

from argh import arg, CommandError

from optimus.logs import init_logging
from optimus.start_project import ProjectStarter

@arg('name', help="Project's name to use, must be a valid python module name")
@arg('-t', '--template', default="basic", help="A python path to a 'project template' module to use instead of the default one 'optimus.defaults.sample', there is also a sample with i18n at 'optimus.defaults.sample_i18n'.")
@arg('--dry-run', default=False, help="Dry run mode will perform all processus but will not create or modify anything")
@arg('-l', '--loglevel', default='info', choices=['debug','info','warning','error','critical'], help="The minimal verbosity level to limit logs output")
@arg('--logfile', default=None, help="A filepath that if setted, will be used to save logs output")
def init(args):
    """
    Create a new project from a project template
    """
    starttime = datetime.datetime.now()
    # Init, load and builds
    root_logger = init_logging(args.loglevel.upper(), logfile=args.logfile)
    
    # Valid that all characters from the name are : "_" character, letters, 
    # identifier ::=  (letter|"_") (letter | digit | "_")*
    # This is not fully safe, user can create a project name using an installed 
    # Python module that will override it and make some troubles in some case
    if args.name:
        if args.name[0] not in letters:
            root_logger.error("Project name must start with a letter")
            return
        for k in args.name[1:]:
            if k not in letters and k not in digits and k != "_":
                root_logger.error("Project name must only contains letters, digits or '_' character")
                return
    
    if args.dry_run:
        root_logger.warning("'Dry run' mode enabled")
    
    # TODO: optionnal command option to specify another path where the project will 
    #       be created
    project_directory = os.path.abspath(os.getcwd())

    loader = ProjectStarter(project_directory, args.name, dry_run=args.dry_run)
    loader.install(args.template)
    
    endtime = datetime.datetime.now()
    root_logger.info('Done in %s', str(endtime-starttime))
