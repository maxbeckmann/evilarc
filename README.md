# evilarc

Create `evil.zip` extracting a copy of `target.txt` to `..\..\..\..\..\..\..\..\Users\victim\target.txt` (on a Windows system):
```
python3 evilarc.py target.txt --path Users\victim
```

Create `poc.xlsx` from a template `base.xlsx` extracting a copy of `target.txt` to `../../../home/victim/target.txt` (on a unix-like system):
```
cp base.xlsx poc.xlsx && python3 evilarc.py target.txt --os unix --path /home/victim --out poc.xlsx -d 3
```

## Purpose
evilarc lets you create a zip file that contains files with directory traversal characters in their embedded path.  Most commercial zip program (winzip, etc) will prevent extraction of zip files whose embedded files contain paths with directory traversal characters.  However, many software development libraries do not include these same protection mechanisms (ex. Java, PHP, etc).  If a program and/or library does not prevent directory traversal characters then evilarc can be used to generate zip files that, once extracted, will place a file at an arbitrary location on the target system.
