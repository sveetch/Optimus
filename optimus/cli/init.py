# -*- coding: utf-8 -*-
"""
Command line action to start a new project
"""
import datetime, os

from argh import arg, CommandError

from optimus.logs import init_logging
from optimus.start_project import ProjectStarter

@arg('name', help="Project's name to use, must be a valid python module name")
@arg('-l', '--loglevel', default='info', choices=['debug','info','warning','error','critical'], help="The minimal verbosity level to limit logs output")
@arg('--logfile', default=None, help="A filepath that if setted, will be used to save logs output")
@arg('-t', '--template', default="basic", help="A python path to a 'project template' module to use instead of the default one 'optimus.defaults.sample', there is also a sample with i18n at 'optimus.defaults.sample_i18n'.")
@arg('--dry-run', default=False, help="Dry run mode will perform all processus but will not create or modify anything")
def init(args):
    """
    Create a new project from a project template
    """
    starttime = datetime.datetime.now()
    # Init, load and builds
    root_logger = init_logging(args.loglevel.upper(), logfile=args.logfile)
    
    # DEPRECATED
    #if not args.name:
        #root_logger.error("'--name' argument is required")
        #return
    # TODO: Check that the given project name is a valid python module name
    # identifier ::=  (letter|"_") (letter | digit | "_")*
    # So valid that all characters from the name are : "_" character, letters, 
    # digits and does not starts with digits
    
    if args.dry_run:
        root_logger.warning("'Dry run' mode enabled")
    
    # TODO: optionnal command option to specify another path where the project will 
    #       be created
    project_directory = os.path.abspath(os.getcwd())

    loader = ProjectStarter(project_directory, args.name, dry_run=args.dry_run)
    loader.install(args.template)
    
    endtime = datetime.datetime.now()
    root_logger.info('Done in %s', str(endtime-starttime))
