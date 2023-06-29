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

but the default output from that **athinput** file is the **vtk** data format, which for this demo will
be too complex to parse. TBD. For now we switch to the ascii table format, viz.

     bin/athena  -i inputs/hydro/athinput.linear_wave1d  -d run2 output2/file_type=tab

### Animations

First example is NEMO biased, effectively quickly plotting all **tab** files using tabplot. Noting that the second row
in each table shows the columns names:


```text
  # Athena++ data at time=0.000000e+00  cycle=0  variables=prim 
  # i       x1v         rho          press          vel1         vel2         vel3     
```

```bash
for f in LinWave*.tab; do
   tabplot $f xcol=2 ycol=5
done
```

or using our sample script
```bash
   ../../animate1 xcol=2 ycol=5
```


### Statistics

The history (hst) keeps track of a number of variables of which we can obtain the statistics (agui/show_stats)

```text
#        [1]=time     [2]=dt      [3]=mass [4]=1-mom    [5]=2-mom [6]=3-mom [7]=1-KE    [8]=2-KE [9]=3-KE [10]=tot-E [11]=max-v2
npt:     501          501         501      501          501       501       501         501      501      501        501
min:     0            1.31217e-05 1        -3.14329e-22 0         0         2.49497e-13 0        0        0.9        0
max:     5            0.003125    1        3.19912e-22  0         0         2.5e-13     0        0        0.9        0
sum:     1253.43      1.56251     501      -1.56725e-20 0         0         1.25127e-10 0        0        450.9      0
mean:    2.50186      0.00311879  1        -3.12825e-23 0         0         2.49754e-13 0        0        0.9        0
disp:    1.44625      0.00013889  0        8.61373e-23  0         0         1.46346e-16 0        0        0          0
skew:    -4.15046e-05 -22.316     0        0.0211432    0         0         -0.0439997  0        0        0          0
kurt:    -1.20002     496.002     0        0.579502     0         0         -1.23003    0        0        0          0
min/sig: -1.72989     -22.3607    -nan     -3.28599     -nan      -nan      -1.75681    -nan     -nan     inf        -nan
max/sig: 1.72732      0.0447214   -nan     4.07715      -nan      -nan      1.68025     -nan     -nan     inf        -nan
median:  2.50312      0.003125    1        -3.21566e-23 0         0         2.49757e-13 0        0        0.9        0
```
>>>>>>> 442032f1ed1844ebf85a161ed8a84b898f4a8778
