# I have 10 files in my ../tickdata directory, each file contains past stocks trading data
# I have a python script called jc_trading_model.py that takes in the file path as argument and
# returns a csv file with the list of stocks to buy and sell
# For example, if I run python jc_trading_model.py ../tickdata/2018-01-01.csv output.csv, it will
# create a csv file called output.csv with the list of stocks to buy and sell in the current directory
# I have another python script called evaluation.py that takes in both the tickdata file and the output file
# and returns the profit of the trading strategy calculated to an double value
# For example, if I run python evaluation.py ../tickdata/2018-01-01.csv output.csv, it will return 10.5
# I have another model called jc_trading_model2.py that I want to compare with jc_trading_model.py
# Help me create a script test.sh that will run jc_trading_model.py and jc_trading_model2.py on all the files in
# ../tickdata and compare the profit of the two models and print the profit side by side for each file 
# For example, if I run ./test.sh, it will print out something like this:
# 2018-01-01.csv 10.5 10.0
# 2018-01-02.csv 10.5 -6.0
# 2018-01-03.csv 10.5 10.9

# start of script
for file in ../tickdata/*.csv
do
    # Get the filename without the directory path and extension
    filename=$(basename -- "$file")
    filename="${filename%.*}"
    
    # Run jc_trading_model.py on the file and save the output to a temporary file
    python jc_trading_model.py "$file" output1.csv
    
    # Run jc_trading_model2.py on the file and save the output to a temporary file
    python jc_trading_model2.py "$file" output2.csv
    
    # Get the profit for the first model
    profit1=$(python evaluation.py "$file" output1.csv)
    
    # Get the profit for the second model
    profit2=$(python evaluation.py "$file" output2.csv)

    # Output the filename and the profit for both model into a txt file called final_evaluation.txt
    # with a column indicating the filename and model of the column
    echo "$filename $profit1 $profit2" >> final_evaluation.txt    
done                                                                    