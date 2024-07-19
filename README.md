# LNK File Packer

A payload generation script written in python. The script embeds a payload inside of an LNK file, and generates the powershell needed to extract the payload and invoke it with the users default program (May be subject to change to just use start-process instead, but for now I liked it being able to do arbitrary files). Writes a file to temp currently, which is a pretty massive IOC but this is just a POC and I am planning on expanding it later.

### Usage:
`python3 main.py -p .\payload.exe -f resume.pdf -t a.exe`
This will generate an lnk file with the filename resume.pdf.lnk ``(if the file name specified with -f is not an lnk file it will be automatically appended)`` and embed payload.exe inside of the shortcut file. Once a payload is generated the shortcut name cannot be changed due to currently having the filename hardcoded in the powershell.

```
usage: lnkPack.py [-h] -f FILENAME -p PAYLOAD [-t TEMP] [-e EXTRA]

Payload generator for self unpacking LNK files

options:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        The output lnk file name
  -p PAYLOAD, --payload PAYLOAD
                        The payload to embed
  -t TEMP, --temp TEMP  The temp file that is dropped to disk
  -e EXTRA, --extra EXTRA
                        Any powershell commands to run after the base payload
```
