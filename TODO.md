# List of issues and todo's

- option to integrate with a running athena.
  test12:   pyqt version
  test13:   pysq version


# Features

Stating perhaps the obvious, the different GUIs all have their own issues. Here is the current GUI list

                           click_+/-  scroll_+/-    step<1      run?     comments
     tkrun   (test1)       ok         not           ok		 -
     qtrun   (test5)       ok         ok  
     gooey   (test7)       ok         ok            ?            ?
     pyqt    (test1        ok         ok            ok           ok
     pysg-tk (test13)      ok         not           weird        not     step < 1 not working?
     pysg-qt (test13)      ok         ok            ok           not
 

# Things to consider

- athenak vs. minik  (a version for only athena_minik)
- python vs. python3


# Python versions

The latest nuisance is the label_props= and radio_props= arguments to matplotlib.widgets.RadioButtons()
but also with a missing module pyparsing. Here's a summary of older versions of python that gave us
trouble:


                                       python -c 'import matplotlib; print(matplotlib.__version__)'

     distro:                python:    mpl:     comments
     -------------------    -------    -----    --------
     ubuntu 22.04           3.10.12    3.7.2    ok
     anaconda3 2023.07-2    3.11.4              ok
     anaconda3 2023.03-1    3.10.12             No module named 'pyparsing'
     ?                      3.10.9     3.7.2    ok
     anaconda3 2022.10      3.9.13              unexpected keyword argument 'label_props'
