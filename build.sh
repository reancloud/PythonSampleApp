#!/bin/sh -x
#Copy the terraform files in the dist/bin folder
rm -rf dist
mkdir dist
#Create the wheel file and copy in dist/bin folder
cd reantest-cli
python setup.py bdist_wheel
cd ../
cp reantest-cli/dist/reantest-0.1-py3-none-any.whl dist/reantest-0.1-py3-none-any.whl

#Copy the install.sh file in the dist folder
cp install.sh dist/install.sh

#cp HOWTO.md dist/HOWTO.md
#Create a tar.gz of the dist folder, which is ready to be shipped.
tar -zcvf reantest.tar.gz dist

