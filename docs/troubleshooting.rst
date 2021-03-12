Troubleshooting
===============

Problems during the installation were observed on a python 3.7 environment with these two packages:

* psycopg2
* graphiz

on the following system:

* Operating System:
* Kernel: Linux 5.4.0-66-generic
* Architecture: x86-64

Running a simulation may error out. In this case the two packages must be installed
in an alternative way, for instance using conda:

::

   conda install -c anaconda psycopg2
   conda install -c anaconda graphviz
