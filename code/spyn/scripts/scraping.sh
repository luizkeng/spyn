grep "TOTAL EN" "${1:-tmp/energyGA.log}" | while read -r line ; do
     i=$((i+1))
     echo "Conformer $i: $line"
done
