#!/bin/bash

SRCDIR=$PWD
SCRIPTDIR=$PWD/scripts
REPO=ietf/datatracker-environment
TAG=latest
WHO=$(whoami)
WHOUID=$(id -u $WHO)
WHOGID=$(id -g $WHO)

# exit when any command fails
set -e

# setup datatracker in home
echo "Setting up datatracker"
cd ~
PARENT=$PWD
MYSQLDIR=$PARENT/$CODEDIR/data/mysql
FILEDIR=$PARENT/$CODEDIR/data/
ln -s $SRCDIR/$CODEDIR $CODEDIR

cd $PARENT/$CODEDIR
mkdir $FILEDIR

# fetch latest docker image
echo "Fetching docker image '$REPO:$TAG'"
docker pull "$REPO:latest"

echo  $FILEDIR


# run datatracker docker instance and tests
cp "$SCRIPTDIR/init.sh" init.sh
docker run -ti --entrypoint $PARENT/$CODEDIR/init.sh \
    -v "$PARENT:/home/$WHO" -v "$MYSQLDIR:/var/lib/mysql" -e USER="$WHO" \
    -e DATADIR="$FILEDIR" -e CWD="$PARENT/$CODEDIR" \
    -e TAG="$TAG" -e FILEDIR="$FILEDIR" -e UID="$WHOUID" \
    -e GID="$WHOGID" "$REPO:$TAG"

echo "Finished running tests"
