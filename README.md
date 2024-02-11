# Rename Epub

Script for renaming epub files with custom format.

## Installation

Use `requirements.txt` to install necessary modules.

```bash
pip install -r requirements.txt
```

## Help

```bash
usage: rename [-h] [-f FILE] [-F FORMAT] [-d DIRECTORY] [-v] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-r] [-o OUTPUT]

program change name of file using metadata from epub

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE
  -F FORMAT, --format FORMAT
                        format of name, default is '{creator} - {title}'
  -d DIRECTORY, --directory DIRECTORY
                        default is '.'
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        logging level
  -r, --replace         should replace file instead of creating copy
  -o OUTPUT, --output OUTPUT
                        output folder to copy file with new name
```

- `-f/--file "filename"` rename/copy only one specific file
- `-F/--format "format"` use matadata names in curly braces from [epub specification](https://www.w3.org/TR/epub-33/#sec-pkg-metadata) to build output filename. Default is `{creator} - {title}` so sample filename will be `James Clear - Atomic Habits Tiny Changes, Remarkable Results.epub`. `creator` is standard metadata name for author.
- `-d/--directory "directory"` specifies directory where script should look for files to rename. It's not recursive. Can not be used with `-f`. Default is `.`.
- `-l/-logging "level"` set logging level
- `-r/--replace` set flag if file should be renamed. If is not set then by default script copies file with new name.
- `-o/--output` specifies the output folder where script should copy files with new name. Can not be used with `-r`. It automatically creates folder if needed.

Script automatically removes illegal characters from filename like: `<`,`>`,`:`,`"`,`/`,`\`.`|`,`?`,`*`.

## Usage

```bash
# makes copy of each file with new name `{creator} - {title}.epub`
python3 rename.py

# makes copy of file atomic.epub with new name in folder ./epub
python3 rename.py -f atomic.epub -o epub

# rename file atomic.epub to {title}+{creator}+{language}.epub 
# example name: Atomic Habits Tiny Changes, Remarkable Results+James Clear+en-US.epub
python3 rename.py --file atomic.epub -r --format '{title}+{creator}+{language}'
```
