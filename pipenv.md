Install acq4 with pip environment
=================================

(Python 3.3 and later only)

pip install --upgrade pip
pip install --user virtualenv

Now, make a virtual environment::

    python -m venv env

Activate it::

    source env/bin/activate
    pip install --upgrade pip
    pip install requests

Install what is needed::

    pip install matplotlib numpy scipy pyparsing==2.0.3 pyserial pyqt5 lmfit h5py six pillow

Run::

    python -m acq4




