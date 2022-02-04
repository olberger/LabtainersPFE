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
Check the [vm](https://github.com/IlyesBenighil/LabtainersPFE/tree/vm) branch. It will give you a virtual machine image that you can use with virtuel box.

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

# Contents of this repo

The repo contains several other git repos as submodules :

- 'Labtainers/' : https://github.com/olberger/Labtainers

# History

Initially, work reused from other repos had been pushed on different
branches :

 - 'master' as a modified version of the distribution of
   https://github.com/mfthomps/Labtainers (distribution made with
   mkdist.sh ?)
