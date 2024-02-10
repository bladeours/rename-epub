import argparse
from ebooklib import epub

parser = argparse.ArgumentParser(
    prog='RenameEPUB',
    description='program change name of file using metadata from epub')

parser.add_argument('-f', '--file')
parser.add_argument('-F', '--format', default="{author} - {title}")
parser.add_argument('-d', '--directory', default=".")
parser.add_argument('-v', '--verbose', help="adds extra verbose")
parser.add_argument('-r', '--replace', action="store_true", help="should replace file instead of creating copy")
args = parser.parse_args()


def get_new_filename(old_filename: str) -> str:
    book = epub.read_epub(old_filename, {"ignore_ncx": True})
    author = book.get_metadata('DC', 'creator')[0][0]
    title = book.get_metadata('DC', 'title')[0][0]
    return args.format.format(author=author, title=title)


def main():
    if args.file:
        print(get_new_filename(args.file))


if __name__ == '__main__':
    main()
