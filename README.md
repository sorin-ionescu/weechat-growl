# WeeChat Growl Script

This is a [Growl](http://growl.info) script for [WeeChat](http://weechat.org) Internet Relay Chat client.

For an [Irssi](http://irssi.org/) Growl script, see [Irssi Growl](https://github.com/sorin-ionescu/irssi-growl).

## Installation

Make sure that the Growl Network Transport Protocol ([GNTP](https://github.com/kfdm/gntp)) Python bindings are installed.

    pip install gntp

Move *growl.py* to *~/.weechat/python/autoload/growl.py* and an *icon.png* to *~/.weechat/icon.png*.

The network settings **DO NOT** need to be populated for local Growl notifications.

## Settings

### Notification Settings

`show_public_message`

Notify on public message. (on/off)

`show_private_message`

Notify on private message. (on/off)

`show_public_action_message`

Notify on public action message. (on/off)

`show_private_action_message`

Notify on private action message. (on/off)

`show_notice_message`

Notify on notice message. (on/off)

`show_invite_message`

Notify on channel invitation message. (on/off)

`show_highlighted_message`

Notify on nick highlight. (on/off)

`show_server`

Notify on server connect and disconnect. (on/off)

`show_channel_topic`

Notify on channel topic change. (on/off)

`show_dcc`

Notify on DCC chat/file transfer messages. (on/off)

`show_upgrade_ended`

Notify on WeeChat upgrade completion. (on/off)

### Sticky Settings

`sticky`

Set sticky notifications. (on/off)

`sticky_away`

Set sticky notifications only when away. (on/off)

### Network Settings

`hostname`

Set the Growl server host.

`password`

Set the Growl server password.

### Icon Settings

`icon`

Set the Growl notification icon path relative to _~/.weechat_.

