ENVNAME="acq4_venv"
python3 -m venv $ENVNAME
source $ENVNAME/bin/activate
pip install --upgrade pip  # be sure pip is up to date in the new env.
pip install wheel  # seems to be missing (note singular)
pip install cython
pip install requests

# now get the dependencies
pip install -r requirements.txt
source $ENVNAME/bin/activate

# build the mechanisms
# this may equire a separate install of the standard NEURON package
# with the same version as we have provided
# nrnivmodl cnmodel/mechanisms

python setup.py develop
source $ENVNAME/bin/activate
