Install acq4 with pip environment in mac OSX (this might mostly work for Linux as well)
=======================================================================================

(Python 3.78 and later only)
Check to make sure you have good version of Python 3 installed by typing "python3"

    >>python3
    Python 3.7.3 (default, Aug  4 2020, 19:30:55)
    [Clang 11.0.3 (clang-1103.0.32.62)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>>

The version should be in the 3.7 range. I have not tested it with 3.8 yet.

Next, change to the directory where you want acq4 to live (I have directory called "Python"
that holds most of my python code).

Then, clone acq4-2019 from the lab git repository and set the working brance to the python3 version:

    git clone https://github.com/pbmanis/acq4-2019.git
    git checkout py3pbm
    
After you clone acq4-2019, change to the directory you cloned it into (e.g., something/acq4-2019)

Make sure the make_env script is executable (it should be by default, but check it). 
If it is not, then make it so:

    >> chmod +x make_env.sh

Next install everything needed and build the environment with:

    >> ./make_env.sh  

Then, still in the acq4-2019 directory:

    >> source acq4_venv/bin/activate

If this is the first time you have installed acq4 here, you might need to 
compile some of the graphic templates first (you should only rarely need to do this):

    >> python  tools/rebuildui.py  pyqt5 -d acq4

Now, it should run:
    
    >> python -m acq4

There may be some warnings about a deprecated "h5py.highlevel". Ignore these for now.

You can make an alias in your .zshrc or .bash_profile file:

    alias acq4="deactivate; cd ~/Desktop/acq4-2019; source acq4_venv/bin/activate; python -m acq4; deactivate;"  # load up and run acq4 in it's own env.

This will allow you to type "acq4" at the terminal, and it should start the program up. When you exit, it should deactivate the environment.
Don't worry if the first "deactivate" throws an error.

(9/18/2020 pbm)


