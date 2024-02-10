import argparse
from ebooklib import epub
from ebooklib.epub import EpubBook, EpubException
import re
import logging
import sys
import os.path


log = logging.getLogger(__name__)
parser = argparse.ArgumentParser(prog='RenameEPUB', description='program change name of file using metadata from epub')

parser.add_argument('-f', '--file')
parser.add_argument('-F', '--format', default="{creator} - {title}")
parser.add_argument('-d', '--directory', default=".")
parser.add_argument('-v', '--verbose', action="store_true", help="adds extra verbose")
parser.add_argument('-l', '--logging', choices=['DEBUG', 'INFO', 'WARNING', "ERROR", "CRITICAL"], default='DEBUG', help="do no print to std output")
parser.add_argument('-r', '--replace', action="store_true", help="should replace file instead of creating copy")
args = parser.parse_args()

def setup_logger():
    numeric_level = getattr(logging, args.logging.upper(), None)
    log.setLevel(numeric_level)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    log.addHandler(handler)
    

def get_metadata(book: EpubBook, name: str) -> str:
    log.debug(f"getting metadata: '{name}'")
    metadata = book.get_metadata('DC', name)
    if not metadata:
        log.warning(f"there is no metadata named: {name}")
        return ""
    return metadata[0][0]
    

def get_names_from_format() -> list[str]:
    return set(re.findall(r"{([^}]+)}", args.format))


def get_new_filename(old_filename: str) -> str:
    log.debug(f"processing file: '{old_filename}'")
    new_name = str(args.format)
    book = epub.read_epub(old_filename, {"ignore_ncx": True})
    for name in get_names_from_format():
        metadata = get_metadata(book, name)
        new_name = new_name.replace(f"{{{name}}}", metadata)
    new_name = f"{new_name}.epub"
    log.debug(f"new name: '{new_name}'")
    return new_name

def rename():
    pass

def main():
    setup_logger()

    if args.file and str(args.file).endswith(".epub"):
        try:
            get_new_filename(args.file)
        except Exception as ex:
            log.error(f"something went wrong when processing '{args.file}': {ex}")
            
    
        

if __name__ == '__main__':
    main()
