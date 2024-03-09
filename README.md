# CPS - Command Prompt Saver
This is software designed for those who are accustomed to the command console to minimize command repetition or at least make it more dynamic. The program comes integrated with basic functions such as creating aliases for code blocks, quick ways to modify these blocks, and more specific ones like typing character by character in a command. It can call itself and can become very powerful if used skillfully. I'm open to proposals for the software as it will be open-source.
## Just available in Windows 10+
It uses batch commands and it is created with Python "subprocess", "os" and "sys" so maybe it isn't compatible with Linux or other OS. 

## Usage
- Set a directory for it.
- Execute without parameters (this might create the `cps.json` file and fill it with default values).
- Type `cps --info` to make sure it works.
- Enjoy...
- - -
### This is the view when you type `cps --help` or `cps -h`
```
Info:
    cps (--help | -h)     Display help text
    cps (--info | -i)     Display all the key infos
    cps a (--info | -i)   Display "a" key info

Run:
  (--clean | -c) excepts !first and !last to be executed.
    cps                   Run !first, !default and !last
    cps .                 Run !first and !last
    cps a                 Run !first, "a" key and !last

Binary operators:
  Dot (.) is used to delete in case of assign or pop in case of append or prepend.
    =     Set a string or another key
    +     Append a string or another key
    *     Prepend a command or another key
    |     Switch a key with another key
    ++    Append to the last command a string
    +*    Prepend to the last command a string
    *+    Append to the first command a string
    **    Prepend to the first command a string
```