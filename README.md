# LabtainersPFE

LabtainersPFE is an adapted version of [Labtainers](https://github.com/mfthomps/Labtainers) to our school Telecom SudParis. 
It aims to do labs without worrying about the environment problem so teachers can gain a lot of time at the begenning of a lab.

Also it gives the possibility of self-assessment for labs. 
## Content
[Installation](#installation)

[Usage for students](#usage-for-students)

[Useful links](#useful-links)


## Installation 
### For Ubuntu users
Download the LabtainersPFE.zip file from the [last release](https://github.com/IlyesBenighil/LabtainersPFE/releases/latest).
Then unzip it and execute the following command line in the labtainer root directory.

```bash
#execute the install-labtainer.sh
./intall-labtainer.sh
```
### For VM users
Check the contents of the `packer-ubuntu-20.04/` subdir (formerly on the [vm](https://github.com/IlyesBenighil/LabtainersPFE/tree/vm) branch). It will give you a virtual machine image that you can use with virtuel box.

## Usage for students

To get a lab:
```bash
./get-lab.sh lab-name
```
To start a lab:
```bash
#go to the labtainer-student directory
cd ./labtainer-student
#start the lab
labtainer lab-name
```
To stop a lab:
```bash
stoplab lab-name
```
To look at your progress:
```bash
checkwork lab-name
```
To submit your work to Moodle:
```bash
python3 ./upload_file.py
```

## Useful links
[Our Lab repository](https://github.com/Ironem/LabsPFE) 

[The initial Labtainers repository](https://github.com/mfthomps/Labtainers)

# Submodules of this repo

The repo contains several other git repos as submodules :

- 'Labtainers/' : https://github.com/olberger/Labtainers in sync with the base revision used at the project start (67e075b06cb40d3cf810de956ee021bcdc03f6f2) on 2021/11/24.

- 'packer-ubuntu-20.04/' : https://github.com/olberger/packer-ubuntu-20.04

# Todo

- merge back the changes in the main directory and in trunk/ (mainly setup_scripts/) into the main Labtainers trunk.

# History

Initially, work reused from other repos had been pushed on different
branches :

 - 'master' as a modified version of the contents of Labtainer's distribution (based off https://github.com/mfthomps/Labtainers as made with mkdist.sh ?)

 - 'vm' as a modified version of https://github.com/heizo/packer-ubuntu-20.04
