#
# update-add.sh Migrate most update function here so that changes to this this file are updated
# before the script is sourced from the update-labtainer.sh script.
#
if [ -z "$LABTAINER_DIR" ] || [ ! -d "$LABTAINER_DIR" ]; then
    export LABTAINER_DIR=/home/student/labtainer/trunk
fi
hascommit=$(grep "^Commit:" labtainer/trunk/README.md)
hasgit=$(grep "github.*releases" labtainer/update-labtainer.sh)
if [ -z "$hascommit" ] || [ -z "$hasgit" ]; then
    cd labtainer
    wget --quiet https://github.com/IlyesBenighil/LabtainersPFE/releases/latest/download/LabtainersPFE.zip -O labtainer.zip
    sync
    cd ..
    # tar xf labtainer/labtainer.tar --keep-newer-files --warning=none
    unzip -n -q labtainer/labtainer.zip
fi
$LABTAINER_DIR/setup_scripts/pull-all.py $test_flag 
here=`pwd`
rm -fr labtainer/trunk/setup-scripts
cd labtainer/trunk/scripts/labtainer-student/bin
if [ ! -L update-designer.sh ]; then
    ln -s ../../../setup_scripts/update-designer.sh
fi
if [[ "$TEST_REGISTRY" != TRUE ]]; then
    mkdir -p $LABTAINER_DIR/MakepackUI/bin
    wget --quiet https://github.com/mfthomps/Labtainers/releases/latest/download/makepackui.jar -O $LABTAINER_DIR/MakepackUI/bin/makepackui.jar
fi
target=~/.bashrc
grep "lab-completion.bash" $target >>/dev/null
result=$?
if [[ result -ne 0 ]];then
   echo 'source $LABTAINER_DIR/setup_scripts/lab-completion.bash' >> $target
fi
source $LABTAINER_DIR/setup_scripts/lab-completion.bash
cd $here

# echo the last readme.md  
# grep "^Distribution created:" labtainer/trunk/README.md | awk '{print "Updated to release of: ", $3, $4}'
# grep "^Branch:" labtainer/trunk/README.md | awk '{print "branch: ", $2}'
# grep "^Revision:" labtainer/trunk/README.md | awk '{print "Revision: ", $2}'
# grep "^Commit:" labtainer/trunk/README.md | awk '{print "Commit: ", $2}'
