Install acq4 with pip environment in mac OSX (this might mostly work for Linux as well)
=======================================================================================

(Python 3.78 and later only)

After you clone acq4-2019, change to the directory you cloned it into (e.g., something/acq4-2019)

Make sure the make_env script is executable (it should be by default, but check it). 
If it is not, then make it so:

    >> chmod +x make_env.sh

Next install everything needed and build the environment with:

    ./make_env.sh  

Then, still in the acq4-2019 directory:

    >> source acq4_venv/bin/activate
    >> python -m acq4

If you are using the .zshrc shell under MacOSX, you can make an alias in your .zshrc file:

    alias acq4="deactivate; cd ~/Desktop/acq4-2019; source acq4_venv/bin/activate; python -m acq4; deactivate;"  # load up and run acq4 in it's own env.

This will allow you to type "acq4" at the terminal, and it should start the program up. When you exit, it should deactivate the environment.
Don't worry if the first "deactivate" throws an error.

(9/18/2020 pbm)


