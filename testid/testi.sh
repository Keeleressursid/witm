#!/bin/sh
cd ../witm
for i in 1
do
cat ../testid/"$i".tekst |grep -v '^#' | python3 witolge.py > /tmp/vastus."$i".tekst
diff ../testid/vastus."$i".tekst /tmp/vastus."$i".tekst
done
