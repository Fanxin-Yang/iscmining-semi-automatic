# backend

The back end is implemented with Flask

## Dependencies
Create a virtual environment first.
```sh
python3 -m venv venv
. venv/bin/activate
pip3 install -r requirements.txt
```
To end the virtual environment.

```sh
deactivate
```
Make sure to set the correct path, where JDK is installed.

```sh
export JAVA_HOME="/Library/Java/JavaVirtualMachines/jdk-17.0.5.jdk/Contents/Home"
```
### Run

```sh
. venv/bin/activate
python3 -m flask run
```

### Note
Make sure to export the right path for JVM before running.
```sh
export JAVA_HOME="/Library/Java/JavaVirtualMachines/jdk-17.0.5.jdk/Contents/Home"
```