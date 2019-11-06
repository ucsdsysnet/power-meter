# power-meter
Python scripts used for managing reading data from the power meters connected to SysNet servers

## Setting up virtual environment
In order to better manage packaging in python, this project uses **pipenv** for version and dependency management.

To install pipenv on your machine, run:

`$ pip install --user pipenv`

*Note:
This does a user installation to prevent breaking any system-wide packages. If pipenv isn’t available in your shell after installation, you’ll need to add the user base’s binary directory to your PATH.*

On Linux and macOS you can find the user base binary directory by running `python -m site --user-base` and adding `bin` to the end. For example, this will typically print `~/.local` (with ~ expanded to the absolute path to your home directory) so you’ll need to add `~/.local/bin` to your `PATH`. You can set your `PATH` permanently by modifying `~/.profile`.

On Windows you can find the user base binary directory by running `python -m site --user-site` and replacing site-packages with Scripts. For example, this could return `C:\Users\Username\AppData\Roaming\Python36\site-packages` so you would need to set your PATH to include `C:\Users\Username\AppData\Roaming\Python36\Scripts`. You can set your user `PATH` permanently in the Control Panel. You may need to log out for the `PATH` changes to take effect.

After installing pipenv, cd into the source directory and run:

`$ pipenv shell`

to create the virtual environment.

`$ pipenv install`

installs all dependencies in the Pipfile.

`$ pipenv run python read_power.py`

runs read_power script, or you can activate shell and run directly (without pipenv run) there.

## Troubleshooting

In order to access the power meters, you must be connected to UCSD-PROTECTED. If you are having trouble with dependencies, (runtime errors with import statements) run `pipenv --rm` to nuke virtual environment, and re-create it with `pipenv shell`. You should not be using pip as your package manager when working in this environment. If you want to add a new package during development, use `pipenv install <package>`. This will ensure it is added as a dependency so that it is reproducible across environments.
