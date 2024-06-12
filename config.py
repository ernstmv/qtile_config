from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
import os
import subprocess

# KEYS
mod = "mod4"
keys = [

    Key([mod], "f", lazy.spawn("chromium"), desc="Firefox"),

    Key([mod], "w", lazy.spawn("whatsapp-for-linux"), desc="whatsapp"),

    Key([mod], "s", lazy.spawn("spotify"), desc="spotify"),

    Key([mod], "a", lazy.spawn("arduino"), desc="arduino"),

    Key([mod], "return", lazy.spawn("terminator"), desc="Terminator"),

    Key([mod], "i", lazy.window.toggle_floating(), desc="Floating"),

    Key([mod], "backspace", lazy.window.kill(), desc="Kill focused window"),

    Key([mod], "space", lazy.next_layout(), desc="Full screen"),

    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    Key([mod], "left", lazy.screen.prev_group(), desc="Mov prev desktop"),
    Key([mod], "right", lazy.screen.next_group(), desc="Mov next desktop"),

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
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

# GROUPS
groups = [
        Group("1", label=" "),
        Group("2", label=" "),
        Group("3", label=" "),
        Group("4", label="󰱯 "),
        Group("5", label="󰈹 "),
        ]

for i in groups:
    keys.extend(
        [
            Key([mod], i.name, lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name)),
            Key([mod, "shift"], i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name)),
        ]
    )

# LAYOUTS
layouts = [
    layout.Columns(
                   border_width=2,
                   margin=6,
                   border_normal="#000000",
                   border_focus="#F2A413",
                   border_on_single=True,
                   num_columns=3,
                   margin_on_single=20),
    layout.Max(
        border_focus="#F2A413",
        border_width=2,
        margin=20,
        ),
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

# COLORS
colo = ["#000000",  # BACKGROUND
        "#F2A413",  # FONTS
        "#FFFFFF",
        "#F2F2F2",
        "#0D0D0D",
        "#F2F2F2",
        "#0D0D0D"]


# SCREENS
widget_defaults = dict(
    font="Terminess Nerd Font Mono Bold",
    fontsize=20,
    padding=3,
    background=colo[0]
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        wallpaper="~/.config/qtile/wpp.jpg",
        wallpaper_mode="fill",
        top=bar.Bar(
            [
                widget.Clock(
                    format="%Y.%m.%d || %I:%M",
                    foreground=colo[1],
                ),
                widget.Spacer(),

                widget.GroupBox(
                    highlight_method="text",
                    highlight_color=colo[1],
                    this_current_screen_border=colo[1],
                ),
                widget.Spacer(),

                widget.Battery(
                    charge_char="charging:",
                    foreground=colo[1],
                    discharge_char="discharging",
                    format="{char}",
                    background=colo[0]
                    ),
                widget.Battery(
                    foreground=colo[2],
                    format="{percent:2.0%}  ",
                    background=colo[0]
                    ),
                widget.Wlan(
                    interface="wlp0s20f3",
                    format='{essid} ',
                    foreground=colo[1],
                    backgroud=colo[0]),
                widget.Backlight(
                    format="󰛨 {percent:2.0%}",
                    backlight_name="intel_backlight",
                    foreground=colo[2],
                    background=colo[0]
                ),
                widget.TextBox(
                    text="󱄠",
                    foreground=colo[2],
                    background=colo[0]
                ),
                widget.Volume(  # Requires alsa-utils
                    format="{percent}",
                    foreground=colo[2],
                    background=None
                ),
            ],
            26,
        ),
    ),
]


# AUTOSTART
@hook.subscribe.startup
def autostart():
    home = os.path.expanduser("~")
    # Don't forget to 'chmod +x' this file
    subprocess.call([home + "/.config/qtile/autostart.sh"])


# ETC
# To be honest, I have no idea what this does.
dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
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
