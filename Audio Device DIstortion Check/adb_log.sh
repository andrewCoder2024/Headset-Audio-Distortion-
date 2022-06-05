LS_DATE=$(date +%Y%m%d-%H:%M)
SAVE_PATH= $1
adb logcat -v time | grep ACCEPTED > $SAVE_PATH/ACCEPTED-$LS_DATE.log