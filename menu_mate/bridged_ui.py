from typing import Optional
from uuid import UUID

_bridged_ui = None
_bridged_ui_uuid = UUID('f5dba3a8-0896-4cd7-bb24-ffa3989fa8ce')

def _handle_bridged_ui_announcement(announcement):
    pass

def _handle_bridged_ui_destroyed(_):
    global _bridged_ui
    _bridged_ui = None

def _initialize_bridged_ui(bridged_ui):
    global _bridged_ui
    _bridged_ui = bridged_ui
    _bridged_ui.announcement.add_listener(_handle_bridged_ui_announcement)
    _bridged_ui.destroyed.add_listener(_handle_bridged_ui_destroyed)

def show_bridged_ui():
    global _bridged_ui
    if _bridged_ui:
        _bridged_ui.focus()
        return
    try:
        from plumbbuddy_proxy.asynchronous import await_for
        from plumbbuddy_proxy.api import gateway, PlumbBuddyNotConnectedError, PlayerDeniedRequestError, BridgedUiNotFoundError
        @await_for(gateway.look_up_bridged_ui(_bridged_ui_uuid))
        def look_up_bridged_ui_continuation(bridged_ui, fault):
            if bridged_ui:
                _initialize_bridged_ui(bridged_ui)
                bridged_ui.focus()
                return
            if isinstance(fault, PlumbBuddyNotConnectedError):
                # TODO: show notification to get player to relaunch PB
                return
            if not isinstance(fault, BridgedUiNotFoundError):
                # TODO: show notification for unexpected error
                return
            @await_for(gateway.request_bridged_ui(None, 'http://localhost:3000', _bridged_ui_uuid, 'Menu Mate', 'To give you a better experience when using any crafting picker.', 'Menu Mate', 'tab-icon.png'))
            #@await_for(gateway.request_bridged_ui(__file__, 'ui', _bridged_ui_uuid, 'Menu Mate', 'To give you a better experience when using any crafting picker.', 'Menu Mate', 'tab-icon.png'))
            def request_bridged_ui_continuation(bridged_ui, fault):
                if bridged_ui:
                    _initialize_bridged_ui(bridged_ui)
                    return
                if isinstance(fault, PlumbBuddyNotConnectedError):
                    # TODO: show notification to get player to relaunch PB
                    return
                if isinstance(fault, PlayerDeniedRequestError):
                    # TODO: show notification to advise player to uninstall the mod? I dunno...
                    return
                # TODO: show notification for unexpected error
    except ModuleNotFoundError:
        # TODO: show notification to advise player to install PB or turn on RMI
        return

def close_bridged_ui():
    if not _bridged_ui:
        return
    _bridged_ui.close()