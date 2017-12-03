# useless
Useless stuffs

# pyftpd.py
pyftpdlib based ftp library.

Customized for Xerox scanner.
When a xerox scanner sent a pdf file by ftp, it creates a directory and put file in it.
The filename seems randomly selected and has no information at all.

This script move the file to the degisnated directory and rename with the current data and time.
And delete the xerox created directory

The xerox created directory and filename stars with `img-`.

