WOLF
======

Last Version 0.2.4

What's new in last version
--------------------------

+ add option yesterday
+ was made optimization and refactoring
+ fix typos

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

**--order, -o:**
print list productivity file

**--yesterday, -y:**
filter tomorrow date

**--theme &lt;theme&gt;, -t &lt;theme&gt;:**
specify theme

**--log &lt;log&gt;, -l &lt;log&gt;:**
write message

**--version/--help:**
print version and help page accordingly