#  Some thoughts on a dynamic GUI for athena


##  example of an athinput file with GUI hints

<time>
correct_err = false     # correct midpoint assumption in analytic solution        #> RADIO true,false
cfl_number  = 0.4       # The Courant, Friedrichs, & Lewy (CFL) Number            #> SCALE 0:2:0.01
tlim       = 5.0        # time limit                                              #> SCALE 1:100:1
integrator = rk2        # time integration algorithm                              #> RADIO rk2,vl2
evolution  = dynamic    # dynamic/kinematic/static                                #> RADIO dynamic,kinematic,static



<name>
key = value     # help text     #> WIDGET [wpars]


## Command Line Interface

### Athena++
Usage: /home/teuben/Athena/agui/athena/bin/athena [options] [block/par=value ...]

Options:
  -i <file>       specify input file [athinput]
  -r <file>       restart with this file
  -d <directory>  specify run dir [current dir]
  -n              parse input file and quit
  -c              show configuration and quit
  -m <nproc>      output mesh structure and quit
  -t hh:mm:ss     wall time limit for final output
  -h              this help

### Athenak

Athena v0.1
Usage: athenak/build/src/athena [options] [block/par=value ...]
Options:
  -i <file>       specify input file [athinput]
  -r <file>       restart with this file
  -d <directory>  specify run dir [current dir]
  -n              parse input file and quit
  -c              show configuration and quit
  -m              output mesh structure and quit
  -h              this help
This Athena++ executable is configured with:
  Problem generator:          built_in_pgens
  Floating-point precision:   double
  MPI parallelism:            OFF
  OpenMP parallelism:         OFF

## Proposed workflow.

0. Terminal command: (a separate GUI can do that too, looking for athinput files
   and then "executing" them via our new gui). 

   Examples :

   agui.py [options] athena/inputs/hydro/athinput.linear_wave1d
   agui.py [options] athenak/inputs/tests/linear_wave_hydro.athinput
 
   [options]

   Should it be able to deal with athena++ as well as athenak ?

1. parse the athinput file and sort by "<name/key=val> help [GUI]"
   [block/par=value ...]
   athena:     no magic marker?
   athenak:    '# AthenaXXX'       has new <meshblock> ?

   Decide which (or all) that have GUI markup ?

   These [GUI] directives will be displayed via this new dynamics
   GUI on screen, and builds up a command 

   Idea: allow mathematical transformation? For example a gridsize of 16,32,64,128,256,....
   could be written as 2**N with N=4,5,6,7,8,...
   #>  SCALE 16:256:*2
   #>  SCALE 4:8:1;%1**2
   The alternative is a radio button with enumerated values

3. EXE -i ATHINPUT -d RUNDIR PARS...

   where PARS... will be provided by the GUI

4. Analyze the 1D-output -   do we need an athoutput file?

   - animate a selected X vs. Y plot in time (from the *tab files)
     # Athena++ data at time=1.940622e+00  cycle=621  variables=prim 
     # i       x1v         rho          press          vel1         vel2         vel3
     
   - look at history of variable (in .hst file) as function of time
     # [1]=time     [2]=dt       [3]=mass     [4]=1-mom    [5]=2-mom    [6]=3-mom    [7]=1-KE     [8]=2-KE     [9]=3-KE     [10]=tot-E   [11]=max-v2
     
   - look at the errors.dat file
     # Nx1  Nx2  Nx3  Ncycle  RMS-L1-Error  d_L1  M1_L1  M2_L1  M3_L1  E_L1   Largest-Max/L1  d_max  M1_max  M2_max  M3_max  E_max

5. TBD - what to do for 2D-output 


## What's currently working:

1. A parser of athinput for tkrun is working, but you can't run anything, just displays the GUI

     ./arun1.py athinput.linear_wave1d > test1.sh
     tkrun test1.sh

     ./arun1.py linear_wave_hydro.athinput > test2.sh
     tkrun test2.sh

## Other ideas

1. For 1D cases it's nice to have a GUI that can plot two variables from the *.tab files
   (or two columns from the hst file), in addition a slider to stop the animation and step
   through the tab files.
