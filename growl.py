# -*- coding: utf-8 -*-
#
# growl.py 
# Copyright (c) 2011 Sorin Ionescu <sorin.ionescu@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


SCRIPT_NAME    = "growl"
SCRIPT_AUTHOR  = "Sorin Ionescu <sorin.ionescu@gmail.com>"
SCRIPT_VERSION = "1.0.0"
SCRIPT_LICENSE = "GPLv3"
SCRIPT_DESC    = "Sends Growl notifications upon events."


# -----------------------------------------------------------------------------
# Settings
# -----------------------------------------------------------------------------
SETTINGS = {
    "irc_server_connecting"   : "on",
    "irc_server_connected"    : "on",
    "irc_server_disconnected" : "on",
    "irc_ctcp"                : "on",
    "irc_dcc"                 : "on",
    "irc_pv"                  : "on",
    "weechat_highlight"       : "on",
    "weechat_pv"              : "on",
    "upgrade_ended"           : "on",
    "sticky"                  : "off",
    "sticky_away"             : "on",
    "icon"                    : "%h/.weechat/icon.png",
}


# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
try:
    import re
    import weechat
    import Growl
    IMPORT_OK = True
except ImportError as error:
    IMPORT_OK = False
    if str(error) == "No module named weechat":
        print("This script must be run under WeeChat.")
        print("Get WeeChat at http://www.weechat.org.")
    if str(error) == "No module named Growl":
        weechat.prnt("", "Growl: Python bindings are not installed.")


# -----------------------------------------------------------------------------
# Utility
# -----------------------------------------------------------------------------
def growl_notify(notification_type, title, description, priority=None):
    """Returns whether Growl notifications should be sticky."""
    is_sticky = False
    if weechat.config_get_plugin("sticky") == "on":
        is_sticky = True
    if weechat.config_get_plugin("sticky_away") == "on" and is_away:
        is_sticky = True
    GROWL.notify(notification_type, title, description, "", is_sticky, priority)


# -----------------------------------------------------------------------------
# Hook Handlers
# -----------------------------------------------------------------------------
def signal_irc_server_connecting(data, signal, signal_data):
    """Notify when connecting to IRC server."""
    if weechat.config_get_plugin("irc_server_connecting") == "on":
        growl_notify(
            "Server",
            "Server Connecting",
            "Connecting to network {0}.".format(signal_data))
    return weechat.WEECHAT_RC_OK

def signal_irc_server_connected(data, signal, signal_data):
    """Notify when connected to IRC server."""
    if weechat.config_get_plugin("irc_server_connected") == "on":
        growl_notify(
            "Server",
            "Server Connected",
            "Connected to network {0}.".format(signal_data))
    return weechat.WEECHAT_RC_OK

def signal_irc_server_disconnected(data, signal, signal_data):
    """Notify when disconnected to IRC server."""
    if weechat.config_get_plugin("irc_server_disconnected") == "on":
        growl_notify(
            "Server",
            "Server Disconnected",
            "Disconnected from network {0}.".format(signal_data))
    return weechat.WEECHAT_RC_OK

def signal_irc_ctcp(data, signal, signal_data):
    """Notify on CTCP Action request."""
    if weechat.config_get_plugin("irc_ctcp") != "on":
        return weechat.WEECHAT_RC_OK
    regex = re.compile(
        r"^:([^!]+)![^\s]+\s+PRIVMSG\s+([^\s]+).+ACTION\s+(.+)$",
        re.UNICODE)
    match = regex.match(signal_data)
    if not match:
        return weechat.WEECHAT_RC_OK
    nick = match.group(1)
    channel = match.group(2)
    message = match.group(3)
    description = "On {0}, {1}:\n{2}".format(channel, nick, message)
    growl_notify("Action", "Action Message", description, 1)
    return weechat.WEECHAT_RC_OK

def signal_irc_dcc(data, signal, signal_data):
    """Notify on CTCP request."""
    if weechat.config_get_plugin("irc_dcc") != "on":
        return weechat.WEECHAT_RC_OK
    regex = re.compile(
        r"^:([^!]+)![^\s]+\s+PRIVMSG\s+[^\s]+\s+.+DCC\s+(CHAT|SEND).*$",
        re.UNICODE)
    match = regex.match(signal_data)
    if not match:
        return weechat.WEECHAT_RC_OK
    nick = match.group(1)
    dcc_type = match.group(2)
    if dcc_type == u"CHAT":
        title = "DCC Chat Request"
        message = "{0} wants to chat directly.".format(nick)
    if dcc_type == u"SEND":
        title = "DCC File Transfer"
        message = "{0} wants to send you a file.".format(nick)
    growl_notify("DCC", title, message)
    return weechat.WEECHAT_RC_OK

def signal_weechat_highlight(data, signal, signal_data):
    """Notify on highlited message."""
    if weechat.config_get_plugin("weechat_pv") != "on":
        return weechat.WEECHAT_RC_OK
    regex = re.compile(r'^(\w+).+?\b(.+)', re.UNICODE)
    match = regex.match(signal_data)
    if not match:
        return weechat.WEECHAT_RC_OK
    nick = match.group(1)
    message = match.group(2)
    growl_notify(
        "Highlight",
        "Highlighted Message",
        "{0}: {1}".format(nick, message), 1)
    return weechat.WEECHAT_RC_OK

def signal_weechat_pv(data, signal, signal_data):
    """Notify on private message."""
    if weechat.config_get_plugin("weechat_pv") != "on":
        return weechat.WEECHAT_RC_OK
    notice_regex = re.compile(r'^--.+?\b(\w+):\s\b(.+)$', re.UNICODE)
    notice_match = notice_regex.match(signal_data)
    message_regex = re.compile(r'^(\w+).+?\b(.+)', re.UNICODE)
    message_match = message_regex.match(signal_data)
    if notice_match:
        nick = notice_match.group(1)
        message = notice_match.group(2)
        title = "Notice Message"
    elif message_match:
        nick = message_match.group(1)
        message = message_match.group(2)
        title = "Private Message"
    else:
        return weechat.WEECHAT_RC_OK
    growl_notify(
        "Private", title, "{0}: {1}".format(nick, message))
    return weechat.WEECHAT_RC_OK

def signal_upgrade_ended(data, signal, signal_data):
    """Notify on private message."""
    if weechat.config_get_plugin("upgrade_ended") == "on":
        growl_notify(
            "WeeChat", "WeeChat Upgraded", "WeeChat has been upgraded.")
    return weechat.WEECHAT_RC_OK

def process_message(
    data, buffer, date, tags,
    displayed, highlight, prefix, message
):
    global is_away
    if weechat.buffer_get_string(buffer, 'localvar_away'):
        is_away = True
    else:
        is_away = False
    return weechat.WEECHAT_RC_OK

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
if __name__ == "__main__" and IMPORT_OK and weechat.register(
    SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION,
    SCRIPT_LICENSE, SCRIPT_DESC, "", ""
):
    global is_away
    is_away = False

    # Initialize options.
    for option, value in SETTINGS.items():
        if not weechat.config_is_set_plugin(option):
            weechat.config_set_plugin(option, value)

    # Initialize Growl.
    global GROWL
    GROWL = Growl.GrowlNotifier(
        applicationName='WeeChat',
        notifications=[
            "Public", "Private", "Action", "Notice", "Invite",
            "Highlight", "Server", "Channel", "DCC", "WeeChat"],
        applicationIcon=Growl.Image.imageFromPath(
            weechat.config_get_plugin("icon")))
    GROWL.register()

    # Register hooks.
    weechat.hook_signal(
        "irc_server_connecting", "signal_irc_server_connecting", "")
    weechat.hook_signal(
        "irc_server_connected", "signal_irc_server_connected", "")
    weechat.hook_signal(
        "irc_server_disconnected", "signal_irc_server_disconnected", "")
    weechat.hook_signal("irc_ctcp", "signal_irc_ctcp", "")
    weechat.hook_signal("irc_dcc", "signal_irc_dcc", "")
    weechat.hook_signal("weechat_highlight", "signal_weechat_highlight", "")
    weechat.hook_signal("weechat_pv", "signal_weechat_pv", "")
    weechat.hook_signal("upgrade_ended", "signal_upgrade_ended", "")
    weechat.hook_print("", "", "", 1, "process_message", "")

