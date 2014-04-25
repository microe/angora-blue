#!/bin/sh

OUTPUT=7376_03.zip

# Remove any previous archive of the project.
rm -f "$OUTPUT"

# Blank out the email login information.
sed -i '.bak' -e "s/fromAddr = '.*'/fromAddr = 'username@gmail.com'/g" AngoraBlue.py
sed -i '' -e "s/toAddrList = \['.*'\]/toAddrList = \['username@gmail.com'\]/g" AngoraBlue.py
sed -i '' -e "s/login = '.*'/login = 'username'/g" AngoraBlue.py
sed -i '' -e "s/password = '.*'/password = 'password'/g" AngoraBlue.py

# Archive the project, excluding hidden and generated files.
zip -r --exclude='*/.*' "$OUTPUT" \
        *.py *.sh build.bat AngoraBlue.spec mac win \
        cascade_training/describe.py cascade_training/*.sh cascade_training/train.bat \
        cascades/haarcascade_frontalcatface.xml cascades/haarcascade_frontalface_alt.xml

# Restore the email login information.
mv -f AngoraBlue.py.bak AngoraBlue.py