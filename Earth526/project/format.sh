
python file1.py
awk '{print $1"d0", $2"d0"}' dc_values.txt > dc_model2.txt
rm dc_values.txt
