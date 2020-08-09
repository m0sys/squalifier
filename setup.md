# Setup

-----

## 1. Checkout the repo.

```shell
git clone https://github.com/mhd53/squalifier.git
cd squalifier
```

## 2. Setup the python environment

### If on GCP AI Platform Notebooks instance

Simply run ```pip install -r requirements.txt -r requirements-dev.txt```.

### If on own machine

Run `conda env create` to create an environment called `squalifier`, as defined in `environment.yml`.
This environment will provide us with the right Python version as well as the CUDA and CUDNN libraries.
We will install Python libraries using `pip-sync`, however, which will let us do three nice things:

1. Separate out dev from production dependencies (`requirements-dev.in` vs `requirements.in`).
2. Have a lockfile of exact versions for all dependencies (the auto-generated `requirements-dev.txt` and `requirements.txt`).
3. Allow us to easily deploy to targets that may not support the `conda` environment.

So, after running `conda env create`, activate the new environment and install the requirements:

```sh
conda activate squalifier
pip-sync requirements.txt requirements-dev.txt
```

If you add, remove, or need to update versions of some requirements, edit the `.in` files, then run

```
pip-compile requirements.in && pip-compile requirements-dev.in
```

Now, every time you work in this directory, make sure to start your session with `conda activate squalifier`.

### In both cases run the following!

Also, run ```export PYTHONPATH=.``` before executing any commands later on, or you will get errors like `ModuleNotFoundError: No module named 'squat_recognizer'`.

In order to not have to set `PYTHONPATH` in every terminal you open, just add that line as the last line of the `~/.bashrc` file using a text editor of your choice (e.g. `vim ~/.bashrc`)