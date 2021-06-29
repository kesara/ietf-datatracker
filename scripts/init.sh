#!/bin/bash

# This script is based on original docker/docker-init.sh from IETF datatracker
# Source: https://trac.ietf.org/trac/ietfdb/browser/trunk/docker/docker-init.sh
# License: https://trac.ietf.org/trac/ietfdb/browser/trunk/LICENSE
# Copyright (c) 2008,2018, The IETF Trust

echo "Running custom entry script!"

# A little bit of setup
export LANG=en_GB.UTF-8

if [ ! "$USER" ]; then
    echo "Environment variable USER is not set -- will set USER='django'."
    USER="django"
fi
if [ ! "$UID" ]; then
    echo "Environment variable UID is not set -- will set UID='1000'."
    UID="1000"
fi
if [ ! "$GID" ]; then
    echo "Environment variable GID is not set -- will set GID='1000'."
    GID="1000"
fi
if [ ! "$TAG" ]; then
    echo "Environment variable TAG is not set -- will set TAG='datatracker'."
    TAG="datatracker"
fi
echo "User $USER ($UID:$GID)"

if ! grep -q ":$GID:$" /etc/group ; then
    echo "Creating group entry for GID '$GID' ..."
    groupadd -g "$GID" "$USER"
fi
if ! id -u "$USER" &> /dev/null; then
    echo "Creating user '$USER' ..."
    useradd -s /bin/bash --groups staff,sudo --uid $UID --gid $GID $USER
    echo "$USER:$USER" | chpasswd
fi

VIRTDIR="/opt/home/$USER/$TAG"
echo "Checking that there's a virtual environment for $TAG ..."
if [ ! -f $VIRTDIR/bin/activate ]; then
    echo "Setting up python virtualenv at $VIRTDIR ..."
    mkdir -p $VIRTDIR
    python3.6 -m venv $VIRTDIR
    echo -e "
# This is from $VIRTDIR/bin/activate, to activate the
# datatracker virtual python environment on docker container entry:
" >> /etc/bash.bashrc
    cat $VIRTDIR/bin/activate >> /etc/bash.bashrc
    cat /usr/local/share/datatracker/setprompt >> /etc/bash.bashrc 
else
    echo "Using virtual environment at $VIRTDIR"
fi

echo "Activating the virtual python environment ..."
. $VIRTDIR/bin/activate


if ! $VIRTDIR/bin/python -c "import django"; then
    echo "Installing requirements ..."
    pip install --upgrade pip
    reqs=$CWD/requirements.txt
    if [ ! -f $reqs ]; then
        echo "   Using $reqs"
        pip install -r $reqs
    else
        echo "   Didn't find $reqs"
        echo "   Using /usr/local/share/datatracker/requirements.txt"
        pip install -r /usr/local/share/datatracker/requirements.txt
    fi
fi

if [ ! -f $CWD/ietf/settings_local.py ]; then
    echo "Setting up a default settings_local.py ..."
    cp $CWD/docker/settings_local.py $CWD/ietf/settings_local.py
fi

for sub in test/id/ test/staging/ test/archive/ test/rfc test/media test/media/photo test/wiki/ietf; do
    dir="$CWD/$sub"
    if [ ! -d "$dir"  ]; then
	echo "Creating dir $dir"
	mkdir -p "$dir";
    fi
done

for sub in					\
	nomcom_keys/public_keys			\
	developers/ietf-ftp			\
	developers/ietf-ftp/charter		\
	developers/ietf-ftp/conflict-reviews	\
	developers/ietf-ftp/internet-drafts	\
	developers/ietf-ftp/rfc			\
	developers/ietf-ftp/status-changes	\
	developers/ietf-ftp/yang/catalogmod	\
	developers/ietf-ftp/yang/draftmod	\
	developers/ietf-ftp/yang/ianamod	\
	developers/ietf-ftp/yang/invalmod	\
	developers/ietf-ftp/yang/rfcmod		\
	developers/www6s			\
	developers/www6s/staging		\
	developers/www6s/wg-descriptions	\
	developers/www6s/proceedings		\
	developers/www6/			\
	developers/www6/iesg			\
	developers/www6/iesg/evaluation		\
	; do
    dir="$CWD/data/$sub"
    if [ ! -d "$dir"  ]; then
	echo "Creating dir $dir"
	mkdir -p "$dir";
	chown "$USER" "$dir"
    fi
done

if [ ! -f "$CWD/test/data/draft-aliases" ]; then
    echo "Generating draft aliases ..."
    ietf/bin/generate-draft-aliases }
fi

if [ ! -f "$CWD/test/data/group-aliases" ]; then
    echo "Generating group aliases ..."
    ietf/bin/generate-wg-aliases }
fi

chown -R $USER /opt/home/$USER
chmod -R g+w   /usr/local/lib/		# so we can patch libs if needed

cd "$CWD"

echo "Running tests"
ietf/manage.py test --settings=settings_sqlitetest # does patching
ietf/manage.py test --settings=settings_sqlitetest --skip-coverage ietf.meeting.tests_views.MaterialsTests.test_upload_minutes_agenda

exit
