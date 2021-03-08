#!/bin/bash

# Make sure that .gitignore has all the files to be ignored.
#====================================
# $ sudo nano .gitignore # create one if it does not exist # echo  >>
# $ sudo nano .gitignore # just this to create and edit it

# # Ignore some files # no empty space above
# # Sam Macharia
# *.csv # ignore all .csv files
# *.txt
# !notes.txt # do not ignore this particular file
# !param_set.txt
# *.mp4
# *.avi
# *.png
# *.html
# *.vtk
# *.svg
# *.pdf
# *.ipynb_checkpoints
#====================================
# Make this file executable: $ sudo chmod -x git_add.sh
# Run this file: $ source git_add.sh
# Then: $ git status
# Then: $ git commit -m 'some comment'
# Then: $ git push -u origin master

git add .
git commit -m 'new changes'
git rm -rf --cached .
# git rm -rf --cached Analysis/ContactStates/*/
git add .

# git add .
# git reset -- Analysis/ContactStates/data4
# git reset -- Analysis/ContactStates/data5
# git reset -- Analysis/ContactStates/fig019
# git reset -- Analysis/ContactStates/figInAc004less
# git reset -- Analysis/ContactStates/figR05DefAgg
# git reset -- Analysis/ContactStates/fig019
# git reset -- Analysis/ContactStates/dataM5pN
# git reset -- Analysis/ContactStates/figR05DefAgg_geq198
# git reset -- Analysis/ContactStates/figR06DefAgg_geq054
# git reset -- Analysis/ContactStates/figR07DefAgg_above019
# git reset -- Analysis/ContactStates/figR07DefAgg_equal019
# git reset -- Analysis/ContactStates/figR07DefAgg_geq019
# git reset -- Analysis/ContactStates/figR08DefAgg_geq004
# git reset -- Analysis/ContactStates/figR09DefAgg_geq001
# git reset -- Analysis/BindingMotors/data2
git status
echo "do:"
echo "git commit -m 'some comment' "
echo "git push -u origin master"
echo "Regards, Sam Macharia"

#===============================
# chmod -x git_add.sh
# source git_add.sh
# git commit -m "some comment"
# git push -u origin master
# Regards, Sam Macharia
#===============================