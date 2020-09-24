ENVNAME="acq4_venv"
echo "Removing previous environment: $ENVNAME"
rm -r $ENVNAME
python3.7 -m venv $ENVNAME
source $ENVNAME/bin/activate
pip3 install --upgrade pip  # be sure pip is up to date in the new env.
pip3 install wheel  # seems to be missing (note singular)
pip3 install cython
pip3 install requests

# now get the dependencies
pip3 install -r requirements.txt
source $ENVNAME/bin/activate

# build the mechanisms
# this may equire a separate install of the standard NEURON package
# with the same version as we have provided
# nrnivmodl cnmodel/mechanisms
python --version
python tools/rebuildUI.py pyqt5 -d acq4
python tools/rebuildUI.py pyqt5 -d acq4/pyqtgraph -v -f
python setup.py develop
source $ENVNAME/bin/activate
