import json
from game_loop import Game
from argparse import ArgumentParser
from curses import wrapper

def main(_):
    parser = ArgumentParser(description="TODO: Add a description")
    parser.add_argument('--settings', default='settings.cfg', help="Location of the settings file to load")
    parser.add_argument('--show_fps', action='store_true', help="If enabled, the fps ticker will be shown by default")
    parser.add_argument('--max_fps', type=int, help="The maximum framerate of the game")
    parser.add_argument('--width', type=int, help="Width of the screen")
    parser.add_argument('--height', type=int, help="Height of the screen")
    parser.add_argument('--debug', action='store_true', help="If enabled, stdin will function as a full debug console")

    args = parser.parse_args()

    config_handle = open(args.settings, "r")
    config = json.load(config_handle)
    config_handle.close()

    if args.max_fps is not None:
        config['max_fps'] = args.max_fps
    if args.width is not None:
        config['width'] = args.width
    if args.height is not None:
        config['height'] = args.height
    if args.show_fps:
        config['show_fps'] = args.show_fps
    if args.debug:
        config['use_debug_console'] = args.debug

    game = Game(config)
    if config.get("use_debug_console", False):
        from debug_console import DebugConsole
        game = DebugConsole(game)

    while game.is_running:
        game.run_loop()

wrapper(main)
