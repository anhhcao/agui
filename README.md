# Testing an Athena* GUI

Focussed on athena++, we show some examples of executing athena, and analyzing it's output using a GUI.
In theory could apply to any of the athena family (athena, athena++, athenak).

Related (inspired?) code is NEMO's **tkrun** and **run** frontends.


## Example (athena++) using Linear Wave

First we grab and compile the code for the linear wave problem

     https://github.com/PrincetonUniversity/athena
     cd athena
     ./configure.py --prob linear_wave
     make clean
     make -j

after which we can run it

     bin/athena   -i inputs/hydro/athinput.linear_wave1d  -d run1




### Statistics

Each output has a number of columns

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
