# useless
Useless stuffs

# pyftpd.py
[pyftpdlib](https://github.com/giampaolo/pyftpdlib) based ftp server.

Customized for Xerox scanner.
When a xerox scanner sent a pdf file by ftp, it creates a directory and put file in it.
The filename seems randomly selected and has no information at all.

This script move the file to the degisnated directory and rename with the current data and time.
And delete the xerox created directory

The xerox created directory and filename stars with `img-`.


## How to use

copy and edit template.yaml to another(data.yaml for example)

    cp template.yaml data.yaml

    vi data.yaml

    ./pyftpd.py -c data.yaml
