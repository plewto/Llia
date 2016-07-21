### lliascript load command

load(filename, sync=True)

Read and execute Python file.



**ARGS**

-    filename - String
-    sync - optional flag, if True synchronize the client and host after
     code execution.  You may want to set sync to False if several files
     are being loaded in sequence and then enable it before the last file
     is loaded.


**WARNING**  Load executes arbitrary Python code and may be a security
  risk.  Only use with trusted code.



