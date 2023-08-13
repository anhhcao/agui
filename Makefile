# See the README.md notes on how to use this Makefile

#
SHELL = /bin/bash

#
TIME = /usr/bin/time

# use python3 or anaconda3
PYTHON = anaconda3

# git directories we should have here

GIT_DIRS = athena athenak

# URLs that we'll need

URL0  = https://github.com/teuben/Athena-Cversion
URL1  = https://github.com/PrincetonUniversity/athena
URL2  = https://gitlab.com/theias/hpc/jmstone/athena-parthenon/athenak
URL3  = https://github.com/teuben/nemo
URL4  = https://github.com/teuben/tkrun
URL5a = https://github.com/teuben/agui
URL5b = https://github.com/anhhcao/agui
URL5c = https://github.com/KylieGong/agui

# the ATHENA executable (from athena or athenak)
# ATHENA = athena/bin/athena
ATHENA = athenak/build/src/athena

.PHONY:  help install build


install: help
	@echo "These are some make targets we advertise. See Makefile for details"

help:
## help:          This Help
help : Makefile
	@sed -n 's/^##//p' $<


## git:           Get all git repos for this install
git:  $(GIT_DIRS)
	@echo Last git: `date` >> git.log

## pull:          Update all git repos
pull:
	@echo -n "lmtoy: "; git pull
	-@for dir in $(GIT_DIRS); do\
	(echo -n "$$dir: " ;cd $$dir; git pull); done
	@echo Last pull: `date` >> git.log

status:
	@echo -n "lmtoy: "; git status -uno
	-@for dir in $(GIT_DIRS); do\
	(echo -n "$$dir: " ;cd $$dir; git status -uno); done

branch:
	@echo -n "lmtoy: "; git branch --show-current
	-@for dir in $(GIT_DIRS); do\
	(echo -n "$$dir: " ;cd $$dir; git branch --show-current); done

athenac:
	git clone $(URL0) -b teuben1 athenac
	$(MAKE) build_athenac

athena:
	git clone $(URL1)
	$(MAKE) build_athena

athenak:
	git clone --recursive $(URL2)

nemo:
	git clone $(URL3)

tkrun:
	git clone $(URL4)

## build:         build athenak
build:	athenak
	(mkdir -p athenak/build; cd athenak/build; cmake ..; make -j 4)

## build_athena   build athena++ for the linear_wave problem
build_athena: athena
	(cd athena; ./configure.py --prob linear_wave; make clean; make -j)

## build_athenac  build AthenaC for the linear_wave problem
build_athenac: athenac
	(cd athenac; autoconf;  ./configure; make all)

## build_nemo:    build nemo - will build tkrun
build_nemo:	nemo
	(cd nemo; ./configure ; make build check bench5)

# a few sample runs

## run1:          example linear_wave_hydro
run1:
	$(ATHENA) -i athenak/inputs/tests/linear_wave_hydro.athinput -d run1
	@echo ./animate1 base=run1/tab/LinWave xcol=x1v ycol=velx
	# -> LinWave.hydro_w.00000.tab

## run1:          example advect_hyd
run2:
	$(ATHENA) -i athenak/inputs/tests/advect_hyd.athinput        -d run2
	@echo ./animate1 base=run2/tab/Advect xcol=x1v ycol=dens
	# -> Advect.hydro_u.00000.tab

run3:
	$(ATHENA) -i athenak/inputs/tests/advect_mhd.athinput        -d run3
	#  -> Advect.mhd_u.00000.tab

run4:
	$(ATHENA) -i athenak/inputs/tests/hohlraum_1d.athinput       -d run4
	#  -> hohlraum_1d.rad_coord.00000.tab  

run5:
	$(ATHENA) -i athenak/inputs/tests/rad_linwave.athinput       -d run5
	# -> rad_linwave.hydro_w.*.tab
	# -> rad_linwave.rad_coord.*.tab

run6:
	$(ATHENA) -i athenak/inputs/hydro/sod.athinput               -d run6
	# -> Sod.hydro_w.00000.tab
	#   base=run6/tab/Sod  xcol=3 ycol=4
	#   base=run6/tab/Sod  xcol=3 ycol=5
	#   base=run6/tab/Sod  xcol=3 ycol=6

run7:
	$(ATHENA) -i athenak/inputs/hydro/shu_osher.athinput         -d run7
	#   THIS IS A KNOWN ERROR

run8:
	$(ATHENA) -i athenak/inputs/hydro/viscosity.athinput         -d run8
	#   ViscTest.hydro_w.00000.tab 
	#   base=run8/tab/ViscTest xcol=3 ycol=6


#  We use past tense for old versions of athena :-)
#  ran1 and ran2 are made by ATHENA++
#  ran3 by good old AthenaC
ran1: athena
	(cd athena; bin/athena  -i inputs/hydro/athinput.linear_wave1d  -d ../ran1)
	@echo Results in ran1

## ran2:          example athena++ linear_wave1d needed by some tests - will also build athena++
ran2: athena
	(cd athena; bin/athena  -i inputs/hydro/athinput.linear_wave1d  -d ../ran2 output2/file_type=tab)
	@echo Results in ran2

## ran3:          example AthenaC linear_wave1d needed by some tests - will also build athenac
ran3: athenac
	athenac/bin/athena  -i athenac/tst/1D-hydro/athinput.linear_wave1d  -d ran3

test0:
	./z1.sh

test1:
	./arun1.py athinput.linear_wave1d > test1.sh
	tkrun test1.sh

test2:
	./arun1.py linear_wave_hydro.athinput > test2.sh
	tkrun test2.sh

test3:
	pyuic5 -x test3.ui  -o test3.py
	python test3.py

test4:
	python pysimplegui.py

test5:
	python pyqt.py testfile

test6:
	python pyqt.py testfile2

test7:
	./gooey_run2.py linear_wave_hydro.athinput

# will try Qt first, else fall back to tkinter
test8:
	./pysg_run.py linear_wave_hydro.athinput

test9: 	ran2
	./plot1d.py -d ran2

test10:
	./pysg_run.py test.athinput

test11:
	./pyqt_run.py test.athinput

# will run the plot when run is clicked
test12:
	./pyqt_run.py athinput.linear_wave1d -r

test13: athena_problems.json
	./pysg_menu.py -r

athena_problems.json:
	./write_problems.py

# collaborations
agui_t:
	git clone $(URL5a) agui_t

agui_a:
	git clone $(URL5b) agui_a

agui_k:
	git clone $(URL5c) agui_k