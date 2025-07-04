from menu_mate.bridged_ui import show_bridged_ui
from sims4.commands import Command, CommandType
from uuid import UUID

@Command("menu_mate.show", command_type=CommandType.Live)
def command_show_bridged_ui(_connection=None):
    show_bridged_ui()