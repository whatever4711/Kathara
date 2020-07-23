import argparse
import shutil
import sys

from .. import utils
from ..foundation.command.Command import Command
from ..manager.ManagerProxy import ManagerProxy
from ..setting.Setting import Setting
from ..strings import strings, wiki_description
from ..trdparty.libtmux.tmux import TMUX


class WipeCommand(Command):
    __slots__ = ['parser']

    def __init__(self):
        Command.__init__(self)

        parser = argparse.ArgumentParser(
            prog='kathara wipe',
            description=strings['wipe'],
            epilog=wiki_description,
            add_help=False
        )

        parser.add_argument(
            '-h', '--help',
            action='help',
            default=argparse.SUPPRESS,
            help='Show an help message and exit.'
        )

        parser.add_argument(
            '-f', '--force',
            required=False,
            action='store_true',
            help='Force the wipe.'
        )

        group = parser.add_mutually_exclusive_group(required=False)

        group.add_argument(
            '-s', '--settings',
            required=False,
            action='store_true',
            help='Wipe the stored settings of the current user.'
        )

        group.add_argument(
            '-a', '--all',
            required=False,
            action='store_true',
            help='Wipe all Kathara machines and links of all users. MUST BE ROOT FOR THIS OPTION.'
        )

        self.parser = parser

    def run(self, current_path, argv):
        args = self.parser.parse_args(argv)

        if not args.force:
            utils.confirmation_prompt("Are you sure to wipe Kathara?", lambda: None, sys.exit)

        if args.all and not utils.is_admin():
            raise Exception("You must be root in order to wipe all Kathara devices of all users.")

        if args.settings:
            Setting.wipe()

            sys.exit(0)
        else:
            ManagerProxy.get_instance().wipe(all_users=bool(args.all))

        vlab_dir = utils.get_vlab_temp_path(force_creation=False)
        shutil.rmtree(vlab_dir, ignore_errors=True)
