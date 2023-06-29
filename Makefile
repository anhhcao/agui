# See the INSTALL.md notes on how to use this Makefile

#
SHELL = /bin/bash

#
TIME = /usr/bin/time

# use python3 or anaconda3
PYTHON = anaconda3


# git directories we should have here

GIT_DIRS = athena athenak

# URLs that we'll need

URL1  = https://github.com/PrincetonUniversity/athena
URL2  = https://gitlab.com/theias/hpc/jmstone/athena-parthenon/athenak
URL3  = https://github.com/teuben/nemo

.PHONY:  help install build


install:
	@echo "The installation has a few manual steps:"

help:
## help:      This Help
help : Makefile
	@sed -n 's/^##//p' $<


## git:       Get all git repos for this install
git:  $(GIT_DIRS)
	@echo Last git: `date` >> git.log

## pull:      Update all git repos
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


athena:
	git clone $(URL1)

athenak:
	git clone --recursive $(URL2)

nemo:
	git clone $(URL3)

## build:     build athenak
build:	athenak
	(mkdir -p athenak/build; cd athenak/build; cmake ..; make -j)

build_nemo:	nemo
	(cd nemo; ./configure ; make build check bench5)
