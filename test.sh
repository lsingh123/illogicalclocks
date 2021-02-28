# The -t flag simulates a sequence of input for a VM. The first value is the clock speed. All
# subsequent values represent a machine action. Any sequence of "0 x" represents the machine 
# receiving time x from another machine in its network queue. Any other value represents the 
# machine randomly drawing that action and putting it on the queue. 
python3 code/server.py -t ./tests/0.txt -id 2 -s 60 && python3 code/testeval.py -expected ./tests/0.txt
python3 code/server.py -t ./tests/1.txt -id 2 -s 60 && python3 code/testeval.py -expected ./tests/1.txt
rm 2test.txt