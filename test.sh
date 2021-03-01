# The -t flag simulates a sequence of input for a VM. The first value is the clock speed. All
# subsequent values represent a machine action. Any sequence of "0 x" represents the machine 
# receiving time x from another machine in its network queue. Any other value represents the 
# machine randomly drawing that action and putting it on the queue. 
python3 code/server.py -t ./tests/0.txt -id 2 -s 60 && python3 code/testeval.py -expected ./tests/0.txt
python3 code/server.py -t ./tests/1.txt -id 2 -s 60 && python3 code/testeval.py -expected ./tests/1.txt
python3 code/server.py -t ./tests/2.txt -id 2 -s 60 && python3 code/testeval.py -expected ./tests/2.txt
python3 code/server.py -t ./tests/3.txt -id 2 -s 60 && python3 code/testeval.py -expected ./tests/3.txt
python3 code/server.py -t ./tests/4.txt -id 2 -s 60 && python3 code/testeval.py -expected ./tests/4.txt
python3 code/server.py -t ./tests/5.txt -id 2 -s 60 && python3 code/testeval.py -expected ./tests/5.txt
python3 code/server.py -t ./tests/6.txt -id 2 -s 60 && python3 code/testeval.py -expected ./tests/6.txt
python3 code/server.py -t ./tests/7.txt -id 2 -s 60 && python3 code/testeval.py -expected ./tests/7.txt
python3 code/server.py -t ./tests/8.txt -id 2 -s 60 && python3 code/testeval.py -expected ./tests/8.txt
python3 code/server.py -t ./tests/9.txt -id 2 -s 60 && python3 code/testeval.py -expected ./tests/9.txt
rm 2test.txt