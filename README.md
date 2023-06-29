# Testing an Athena* GUI

Focussed on athena++, we show some examples of executing athena, and analyzing it's output using a GUI.
In theory could apply to any of the athena family (athena, athena++, athenak).

Related (inspired?) code is NEMO's **tkrun** and **run** frontends.


## Example (athena++) using Linear Wave

First we grab and compile the code for the linear wave problem

     git clone https://github.com/PrincetonUniversity/athena
     cd athena
     ./configure.py --prob linear_wave
     make clean
     make -j

Compiling the code takes the most time, but on a typical laptop well under 30 seconds.

After this we can run it

     bin/athena  -i inputs/hydro/athinput.linear_wave1d  -d run1

but the default output from that athinput file is the **vtk** data format, which for this demo will
be too complex to parse.

     bin/athena  -i inputs/hydro/athinput.linear_wave1d  -d run2 output2/file_type=tab
