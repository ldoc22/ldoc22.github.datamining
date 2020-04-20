import py_stringmatching as sm
import csv
import tokenize
import pandas as pd


gj = sm.GeneralizedJaccard()

indice1 = list()
indice2 = list()
titles1 = list()
titles2 = list()
authors1 = list()
authors2 = list()
year1 = list()
year2 = list()
matches = 0;
count = 0;
def Append(row1, idx1, row2, idx2):
    indice1.append(idx1);
    indice2.append(idx2);
    titles1.append(row1[1]);
    titles2.append(row2[1]);
    authors1.append(row1[2]);
    authors2.append(row2[2]);
    year1.append(row1[3]);
    year2.append(row2[3]);



with open('MatchingTableA.csv', encoding='utf8') as file1:
    csv_reader1 = csv.reader(file1)    
    for row1 in csv_reader1:
        count+=1;
        secondCount = 0
        if(count == 1):
            continue;
        i = str(row1[1]).split(' ')
        with open('MatchingTableB.csv', encoding='utf8') as file2:
            csv_reader2 = csv.reader(file2)
            for row2 in csv_reader2:
                secondCount+=1
                if(secondCount == 1):
                    continue;
                j = str(row2[1]).split(' ')
                x = gj.get_raw_score(i, j)
                if(x >= .95):
                    matches+=1
                   
                    Append(row1,count, row2, secondCount)
            print(str(count)+' -> Matches: ' + str(matches))            
book = pd.DataFrame(
    {
        'ltable_ID':indice1,
        'rtable_ID':indice2,
        'ltable_Title':titles1,
        'ltable_Authors': authors1,
        'ltable_Year': year1,
        'rtable_Title':titles2,   
        'rtable_Authors': authors2,
        'rtable_Year':year2
    })
book.to_csv('TableC_97.csv')

print("Complete")
        
           
