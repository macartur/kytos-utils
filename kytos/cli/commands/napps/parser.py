"""kytos - The kytos command line.

You are at the "napps" command.

Usage:
       kytos napps create
       kytos napps upload
       kytos napps list
       kytos napps install   <napp>...
       kytos napps uninstall <napp>...
       kytos napps enable    <napp>...
       kytos napps disable   <napp>...
       kytos napps search    <pattern>
       kytos napps -h | --help

Options:

  -h, --help    Show this screen.

Common napps subcommands:

  create        Create a bootstrap NApp structure for development.
  upload        Upload current NApp to Kytos repository.
  list          List all NApps installed into your system.
  install       Install a NApp into a controller.
  uninstall     Remove a NApp from your controller.
  enable        Enable a installed NApp.
  disable       Disable a NApp.
  search        Search for NApps in NApps Server.

"""
import sys

from docopt import docopt
from kytos.cli.commands.napps.api import NAppsAPI
from kytos.utils.exceptions import KytosException


def parse(argv):
    args = docopt(__doc__, argv=argv)
    try:
        call(sys.argv[2], args)
    except KytosException as e:
        print("Error parsing args: {}".format(e))
        exit()


def call(subcommand, args):
    args['<napp>'] = parse_napps(args['<napp>'])
    func = getattr(NAppsAPI, subcommand)
    func(args)


def parse_napps(napp_args):
    """Return a list of author and name from the napp list argument.

    The expected format of a NApp is napp_author/napp_name.

    Args:
        napp_args (list): NApps from the cli.

    Return:
        list: tuples (author_name, napp_name).

    Raises:
        KytosException: If a NApp has not the form _author/name_.
    """
    def parse_napp(arg):
        """Parse one argument."""
        napp = arg.split('/')
        if len(napp) != 2 or len(napp[0]) == 0 or len(napp[1]) == 0:
            msg = '"{}" NApp has not the form username/napp_name.'.format(arg)
            raise KytosException(msg)
        return tuple(napp)

    return [parse_napp(arg) for arg in napp_args]