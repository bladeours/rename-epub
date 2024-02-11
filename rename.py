import argparse
import shutil
from ebooklib import epub
from ebooklib.epub import EpubBook
import re
import logging
import sys
import os
import shutil
from pathlib import Path
from pathvalidate import sanitize_filename


log = logging.getLogger(__name__)
name_dict = {}
parser = argparse.ArgumentParser(prog="rename", description="program change name of file using metadata from epub")

parser.add_argument("-f", "--file")
parser.add_argument(
    "-F", "--format", default="{creator} - {title}", help="format of name, default is '{creator} - {title}'"
)
parser.add_argument("-d", "--directory", help="default is '.'")
parser.add_argument(
    "-l", "--logging", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default="WARNING", help="logging level"
)
parser.add_argument("-r", "--replace", action="store_true", help="should replace file instead of creating copy")
parser.add_argument("-o", "--output", help="output folder to copy file with new name")
args = parser.parse_args()


def exit_and_log(exit_code: int):
    log.debug(f"exit with code: {exit_code}")
    sys.exit(exit_code)


def validate_args():
    if args.file and args.directory:
        log.error("you can not set file and directory at the same time")
        exit_and_log(1)
    if not args.file and not args.directory:
        log.debug("setting directory to '.'")
        args.directory = "."
    if args.replace and args.output:
        log.error("you can not set output and replace at the same time")
        exit_and_log(1)


def setup_logger():
    numeric_level = getattr(logging, args.logging.upper(), None)
    log.setLevel(numeric_level)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    log.addHandler(handler)


def get_metadata(book: EpubBook, name: str) -> str:
    log.debug(f"getting metadata: '{name}'")
    metadata = book.get_metadata("DC", name)
    if not metadata:
        log.warning(f"there is no metadata named: {name}")
        return ""
    return metadata[0][0]


def get_names_from_format() -> list[str]:
    return set(re.findall(r"{([^}]+)}", args.format))


def get_new_filename(old_filename: str) -> str:
    formatted_name = reformat_name(old_filename)
    if args.output:
        dirname = args.output
        Path(dirname).mkdir(parents=True, exist_ok=True)
    else:
        dirname = os.path.dirname(old_filename)
    new_filename = os.path.join(dirname, sanitize_filename(formatted_name))
    new_filename = add_suffix_if_needed(new_filename)
    log.info(f"new filename: '{new_filename}'")
    return new_filename

def add_suffix_if_needed(new_filename):
    while os.path.isfile(new_filename):
        log.debug(f"file {new_filename} already exists, adding suffix...")
        file_name, file_extension = os.path.splitext(new_filename)
        match = re.search(r"\((\d)\)$", file_name)
        if match:
            index = int(match.group(1))
            file_name = file_name.removesuffix(f" ({index})")
            new_filename = new_filename = f"{file_name} ({index + 1}){file_extension}"
            log.debug(f"new suffix:' ({index + 1})'")
        else:
            new_filename = f"{file_name} (0){file_extension}"
            log.debug(f"new suffix:' (0)'")
    return new_filename

def reformat_name(old_filename):
    log.debug(f"processing file: '{old_filename}'")
    formatted_name = str(args.format)
    book = epub.read_epub(old_filename, {"ignore_ncx": True})
    for name in get_names_from_format():
        metadata = get_metadata(book, name)
        formatted_name = formatted_name.replace(f"{{{name}}}", metadata)
    formatted_name = f"{formatted_name}.epub"
    log.debug(f"new name: '{formatted_name}'")
    return formatted_name


def handle_change_file(old_filename: str) -> int:
    if not str(old_filename).endswith(".epub"):
        log.error("file extension has to be '.epub'!")
        return 1
    try:
        new_filename = get_new_filename(old_filename)
        if args.replace:
            log.debug("changing file name")
            os.rename(old_filename, new_filename)
        else:
            log.debug("copy file with new name")
            shutil.copy(old_filename, new_filename)
        return 0
    except Exception as ex:
        log.error(f"something went wrong when processing '{old_filename}': {ex}")
        return 1


def main():
    setup_logger()
    validate_args()
    old_filename = args.file
    if old_filename:
        exit_code = handle_change_file(old_filename)
        exit_and_log(exit_code)
    directory = args.directory
    for file in os.listdir(directory):
        file_and_path = os.path.join(directory, file)
        if os.path.isfile(file_and_path) and file_and_path.endswith(".epub"):
            handle_change_file(file_and_path)


if __name__ == "__main__":
    main()