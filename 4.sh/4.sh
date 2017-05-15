#!/bin/bash

hargajual=$(curl -s http://www.bankmandiri.co.id/resource/kurs.asp?row=2 | grep "beli"|sed -e 's/<[^>]*>//g' |$ echo $hargajual
echo $hargajual >> "hargajual.txt"

