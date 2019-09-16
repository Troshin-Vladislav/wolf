WOLF
======

Last Version 0.2.1

What's new in last version
--------------------------

+ add option tomorrow
+ was made optimization and refactoring

Program create report a productivity and output it on display


INSTALL:
--------

1) move executable file python to /usr/local/bin 
2) create file with name ".productivity.ord" in home user directory
(program work for each user)


	$ mv wolf.py /usr/local/bin

	$ touch ~/.productivity.ord
 

USE:
----

	$ wolf [options] 

OPTIONS:
--------

**-o, --order:**
print list productivity file

**--tomorrow, -r:**
filter tomorrow date

**--theme &lt;theme&gt;, -t &lt;theme&gt;:**
specify theme

**--log &lt;log&gt;, -l &lt;log&gt;:**
write message

**--version/--help:**
print version and help page accordingly