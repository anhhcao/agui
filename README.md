# Testing an Athena* GUI

Focussed on athena++, we show some examples of executing athena, and analyzing it's output using a GUI.
In theory could apply to any of the athena family (athena, athena++, athenak), but we are focussing on
athenak, since all the problems are compiled into one executable.


Related (inspired?) code is NEMO's **tkrun** and **run** frontends.


## Example (athenak) using Linear Wave

Using **athenak** is now preferred, as the executable has *all* problems compiled
into the executable. Some older comments on athena++ can be found below.

Again, an example how to compile and run the code

     git clone --recursive https://gitlab.com/theias/hpc/jmstone/athena-parthenon/athenak
     mkdir athenak/build
     cd athenak/build
     cmake ..
     make -j

or if you're lazy, use the Makefile in this agui directory:

     make build

this takes a bit longer, mostly because the kokkos library has to be compiled with).   The binary is
now in **athenak/build/src/athena**.

```text
build/src/athena -i inputs/tests/linear_wave_hydro.athinput -d run1
 -> LinWave.hydro_w.00000.tab

build/src/athena -i inputs/tests/advect_hyd.athinput        -d run2
 -> Advect.hydro_u.00000.tab
 
build/src/athena -i inputs/tests/advect_mhd.athinput        -d run3
  -> Advect.mhd_u.00000.tab

build/src/athena -i inputs/tests/hohlraum_1d.athinput       -d run4
  -> hohlraum_1d.rad_coord.00000.tab  

build/src/athena -i inputs/tests/rad_linwave.athinput       -d run5
 -> rad_linwave.hydro_w.*.tab
 -> rad_linwave.rad_coord.*.tab

build/src/athena -i inputs/hydro/sod.athinput               -d run6
 -> Sod.hydro_w.00000.tab
   base=run6/tab/Sod  xcol=3 ycol=4
   base=run6/tab/Sod  xcol=3 ycol=5
   base=run6/tab/Sod  xcol=3 ycol=6

build/src/athena -i inputs/hydro/shu_osher.athinput         -d run7
   ERROR

build/src/athena -i inputs/hydro/viscosity.athinput         -d run8
   ViscTest.hydro_w.00000.tab 
   base=run8/tab/ViscTest xcol=3 ycol=6
```


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

if **tkrun** is enabled, use

   tkrun ../../animate1 


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
