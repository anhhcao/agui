#  Some thoughts on a dynamic GUI for athena


##  example of an athinput file with GUI hints

<time>
correct_err = false     # correct midpoint assumption in analytic solution        #> RADIO true,false
cfl_number  = 0.4       # The Courant, Friedrichs, & Lewy (CFL) Number            #> SCALE 0:2:0.01
tlim       = 5.0        # time limit                                              #> SCALE 1:100:1
integrator = rk2        # time integration algorithm                              #> RADIO rk2,vl2
evolution  = dynamic    # dynamic/kinematic/static                                #> RADIO dynamic,kinematic,static



<name>
key = value     # help text     #> WIDGET wpars



## Proposed workflow.

0. Terminal command: (a separate GUI can do that too, looking for athinput files
   and then "executing" them via our new gui). 

   Examples :

   agui.py [options] athena/inputs/hydro/athinput.linear_wave1d
   agui.py [options] athenak/inputs/tests/linear_wave_hydro.athinput
 
   [options]

   Should it be able to deal with athena++ as well as athenak ?

1. parse the athinput file and sort by "<name/key=val> help [GUI]"
   
   athena:     no magic marker?
   athenak:    '# AthenaXXX'       has new <meshblock> ?

   Decide which (or all) that have GUI markup ?

   These [GUI] directives will be displayed via this new dynamics
   GUI on screen, and builds up a command 

   

3. EXE -i ATHINPUT -d RUNDIR PARS...

   where PARS... will be provided by the GUI

4. Analyze the 1D-output
   - animate a selected X vs. Y plot in time (from the *tab files)
     # Athena++ data at time=1.940622e+00  cycle=621  variables=prim 
     # i       x1v         rho          press          vel1         vel2         vel3     
   - look at history of variable (in .hst file) as function of time
     # [1]=time     [2]=dt       [3]=mass     [4]=1-mom    [5]=2-mom    [6]=3-mom    [7]=1-KE     [8]=2-KE     [9]=3-KE     [10]=tot-E   [11]=max-v2  
   - look at the errors.dat file
     # Nx1  Nx2  Nx3  Ncycle  RMS-L1-Error  d_L1  M1_L1  M2_L1  M3_L1  E_L1   Largest-Max/L1  d_max  M1_max  M2_max  M3_max  E_max

5. TBD - what to do for 2D-output 

