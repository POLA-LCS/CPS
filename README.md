# CPS
## A Command Prompt Saver for Windows 10+

### Usage
```
Info:
- cps (--help | -h)     Display help text
- cps (--info | -i)     Display all the key infos
- cps a (--info | -i)   Display "a" key info

Run:
- cps                   Run !first, !default and !last
- cps a                 Run !first, "a" key and !last
- cps (--clean | -c)    Run !default
- cps a (--clean | -c)  Run "a" key

Set (prefixed by cps):
- a = 'b'    Set "a" key to 'b' command
- a = b      Set "a" key yo "b" key
- a + 'b'    Append 'b' command to the bottom of "a" key
- a + b      Append "b" key commands to the bottom of "a" key
- a * 'b'    Append 'b' command to the top of "a" key
- a * b      Append "b" key commands to the top of "a" key
- a = .      Delete "a" key
- a + .      Pop the last element of "a" key
- a * .      Pop the first element of "a" key
- a | b      Switche "a" key with "b" key
```