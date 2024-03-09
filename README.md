# CPS
## A Command Prompt Saver for Windows 10+

### Usage
*Info:*
- cps (--help | -h)     Display help text
- cps (--info | -i)     Display all the key infos
- cps a (--info | -i)   Display "a" key info

*Run:*
_"--clean" or "-c" excepts !first and !last to be executed_.
- cps                   Run !first, !default and !last
- cps .                 Run !first and !last
- cps a                 Run !first, "a" key and !last

*Binary operators*
_Dot (.) is used to delete in case of assign or pop in case of append or prepend_
- =     Set a string or another key
- +     Append a string or another key
- *     Prepend a command or another key
- |     Switch a key with another key
- ++    Append to the last command a string
- +*    Prepend to the last command a string
- *+    Append to the first command a string
- **    Prepend to the first command a string