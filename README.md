cp2dd
=====

Why?
----
This script was created for the following case:
- You had an external HD you were copying files from, and these files failed occasionally.
- You don't want to ddrescue the entire disk, because: a) you might have enough space to do it, or b) you won't be able to tell which files were sitting around the bad blocks from the ones that are healthy.
- I created this script because I needed it (the exact above scenario).

How?
----
1) After you run your cp -R, you will get a list of files that failed to copy. Please save this list as input.txt. E.g.:

```
cp: /Volumes/SAMSUNG/D/Backup/Alisson/Desktop/Organizar/FOTOS/DSC00329.JPG: Input/output error
cp: /Volumes/SAMSUNG/D/Backup/Alisson/Desktop/ultimas/DSC03950.JPG: Input/output error
```

2) Install dd (probably built-in) and ddrescue. You might want to use homebrew for that (http://brew.sh/).

3) Install Python3 (script wasn't tested on earlier versions).

4) Run cp2dd.py using the following parameters:

```
#use dd to copy
./cp2dd.py -i input.txt -o output.sh -f /prefix/path/from/ -t "/prefix path/to/"
```

```
#use ddrescue to copy
./cp2dd.py -i input.txt -o output.sh -f /prefix/path/from/ -t "/prefix path/to/" -udr
```

```
#sample help output
$ ./cp2dd.py -h
usage: cp2dd.py [-h] -i INPUT [-o OUTPUT] [-f FROM_DIR] [-t TO_DIR] [-la]
                [-lf] [-ld] [-udr]

Quickie to transform cp -R errors in dd commands for further desperate
attempts of recovery.Please use double quotes to enclosure paths with spaces.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input file name
  -o OUTPUT, --output OUTPUT
                        Output file name
  -f FROM_DIR, --from_dir FROM_DIR
                        From prefix path
  -t TO_DIR, --to_dir TO_DIR
                        To prefix path
  -la, --listall        List all files and directories after processing. Will
                        not write to output.
  -lf, --listfiles      List all files after processing. Will not write to
                        output.
  -ld, --listdirectories
                        List all directories after processing. Will not write
                        to output.
  -udr, --useddrescue   Use ddrescue instead of dd.
```

4) run the resulting output.sh, this will attempt to copy the failed files again one by one, and try to recover data (when using ddrescue).

Features:
---------
- Utilises the recommended conv=noerror,sync for dd copy.
- When using ddrescue, tries to read 6 times form the source (3 forwards and 3 reverse).
- When using ddrescue, utilises a logfile to save data already copied accross 3 runs as to save time.
- Allows you to list folders and filers (-la, -lf or -ld). When listing no attempt to copy is made.
- This script does not attempt to copy folders accross, only files. It tries to detect files by the extension (e.g.: .bmp is considred a file). I do not try to read file information to do so in an attempt to touch the origin disk the less as possible.

Disclaimer:
-----------
I recommend you to read the code and understand what the generated bash script does. Recovering data is hard and I cannot say this script is gonna help every time. If your data is important, do not attempt to rescue directly as you might damage the drive even futher.
