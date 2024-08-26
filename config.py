from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
import os
import subprocess




# KEYS
mod = "mod4"
keys = [

    Key([mod], "p", lazy.spawn("firefox"), desc="Firefox"),

    Key([mod], "o", lazy.spawn("whatsapp-for-linux"), desc="Whatsapp"),

    Key([mod], "i", lazy.spawn("spotify-launcher"), desc="Spotify"),

    Key([mod], "e", lazy.spawn("dolphin"), desc="File explorer"),

    Key([mod], "u", lazy.spawn("arduino-ide"), desc="Arduino"),

    Key([mod], "m", lazy.spawn("rofi -show drun"), desc="App launcher"),

    Key([mod], "return", lazy.spawn("alacritty"), desc="Terminal"),

    Key([mod], "n", lazy.window.toggle_floating(), desc="Floating"),

    Key([mod], "backspace", lazy.window.kill(), desc="Kill focus window"),

    Key([mod], "space", lazy.next_layout(), desc="Full screen"),


    Key([mod], "left", lazy.screen.prev_group(), desc="Mov prev desktop"),
    Key([mod], "right", lazy.screen.next_group(), desc="Mov next desktop"),
    Key([], "Print", lazy.spawn("scrot")),
    # Volume
    Key(
        [], "XF86AudioRaiseVolume",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%")),
    Key(
        [], "XF86AudioLowerVolume",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5% ")),
    Key(
        [], "XF86AudioMute",
        lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),

    # Brightness
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set 10%+")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),

    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),

    # Move windows between columns
    Key(
        [mod, "shift"], "h",
        lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key(
        [mod, "shift"], "l",
        lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key(
        [mod, "shift"], "j",
        lazy.layout.shuffle_down(), desc="Move window down"),
    Key(
        [mod, "shift"], "k",
        lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows
    Key(
        [mod, "control"], "h",
        lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l",
        lazy.layout.grow_right(), desc="Grow window to the right"),
    Key(
        [mod, "control"], "j",
        lazy.layout.grow_down(), desc="Grow window down"),
    Key(
        [mod, "control"], "k",
        lazy.layout.grow_up(), desc="Grow window up"),

    # Other basic actions
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Log out"),
]

# MOUSE
mouse = [
    Drag(
        [mod], "Button1",
        lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag(
        [mod], "Button3",
        lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click(
        [mod], "Button2", lazy.window.bring_to_front()),
]

# GROUPS
groups = [
        Group("1", label="󰇴 "),
        Group("2", label=" "),
        Group("3", label=" "),
        Group("4", label=" "),
        Group("5", label=" "),
        ]

for i in groups:
    keys.extend(
        [
            Key([mod], i.name, lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name)),
            Key([mod, "shift"], i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}"),
        ]
    )

# COLORS
colo = ["#000000",  # BLACK
        "#FFFFFF",  # WHITE
        "#2D2D2D",  # BACKGROUNDS
        "#F2F2F2"]  # FONTS

# LAYOUTS
layouts = [
    layout.Columns(
                   border_width=1,
                   margin=3,
                   border_normal=colo[0],
                   border_focus=colo[0],
                   border_on_single=True,
                   num_columns=3,
                   margin_on_single=3),
    layout.Max(
        border_focus=colo[0],
        border_width=1,
        margin=10,
        ),
]


# SCREENS
widget_defaults = dict(
    font="Hurmit Nerd Font",
    fontsize=15,
    padding=3,
    background=colo[2]
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        wallpaper="~/.config/qtile/wpp.png",
        wallpaper_mode="fill",
        top=bar.Bar(
            [
                widget.Clock(
                    format="%I:%M at %d.%m.%Y",
                    foreground=colo[3],
                ),
                widget.Spacer(),

                widget.GroupBox(
                    highlight_method="text",
                    active="#000000",
                    foreground='#FFFFFF',
                    fontsize=20,
                ),

                widget.Spacer(),

                widget.Wlan(
                    interface="wlp0s20f3",
                    disconnected_message="",
                    use_ethernet=True,
                    ethernet_interface='enp46s0',
                    ethernet_message="󰈀 Wired",
                    format=' {essid}',
                    foreground=colo[3],
                ),
                widget.Battery(
                    discharge_char="󰁹",
                    charge_char="󰚥",
                    foreground=colo[3],
                    update_interval=1,
                    format="{char} {percent:2.0%}  ",
                ),
                widget.TextBox(
                    text=" ",
                    foreground=colo[3],
                ),
                widget.Volume(  # Requires alsa-utils
                    format="{percent}",
                    foreground=colo[3]
                ),
                widget.TextBox(
                    text="   ",
                    foreground='#FF0000',
                    mouse_callbacks={
                        'Button1': lazy.spawn('sudo shutdown now')
                        }
                )
            ],
            30,
            border_color=colo[3],
            border_width=[0, 0, 0, 0],
            margin=[10, 100, 2, 100],
        ),
    ),
]


# AUTOSTART
@hook.subscribe.startup_once
def autostart():
    subprocess.Popen(
            ['picom', '--config',
                '/home/user/.config/picom/picom.conf', '--daemon'])
    home = os.path.expanduser("~")
    subprocess.call([home + "/.config/qtile/autostart.sh"])


@hook.subscribe.client_new
def float_to_front(window):
    if isinstance(window.window.get_wm_class()[1], str):
        if window.window.get_wm_class()[1] == 'Alacritty':
            window.floating = True
            window.bring_to_front()


# To be honest, I have no idea what this does.
dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    border_width=0,
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)

focus_on_window_activation = "smart"
reconfigure_screens = True
wl_input_rules = None
wmname = "Qtile"
