import argparse
from datetime import date
from pathlib import Path


EXTENSIONS = (
    '.mkv',
    '.m4v',
    '.mp4',
    '.mpg',
    '.avi',
)

EXCLUDE_PATHS = (
    '.Trash-1000',
    '.awake',
    'lost+found',
    'Downloads',
)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-dt", "--dest-tv", required=True, help="Path to save the tv show list to")
    parser.add_argument("-dm", "--dest-movie", required=True, help="Path to save the movie list to")
    parser.add_argument("-m", "--movie-path", required=False, help="Path to the Movies")
    parser.add_argument("-t", "--tv-path", required=False, help="Path to the TV shows")
    return parser.parse_args()


def process_shows(parent_path: Path):
    show_list = []
    path = Path(parent_path)
    for p in path.iterdir():
        dir_name = p.parts[-1]
        if dir_name in EXCLUDE_PATHS:
            continue
        if p.is_dir():
            shows = process_shows(p)
            if shows:
                show_list.extend(shows)
        else:
            filename = p.parts[-1]
            if p.suffix in EXTENSIONS:
                show_list.append(filename)
    return show_list


def write_list(show_list: list, destination: str):
    with open(destination, "w") as fp:
        for show in show_list:
            fp.writelines(f"{show}\n")


def main():
    args = parse_args()
    today = date.today()
    if args.tv_path:
        write_list(process_shows(args.tv_path), f"{args.dest_tv}-{today}.txt")
    if args.movie_path:
        write_list(process_shows(args.movie_path), f"{args.dest_movie}-{today}.txt")


if __name__ == "__main__":
    main()
