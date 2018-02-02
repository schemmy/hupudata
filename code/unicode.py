##################

# @Author: 			   Chenxin Ma
# @Email: 			   machx9@gmail.com
# @Date:               2018-02-01 17:37:31
# @Last Modified by:   Chenxin Ma
# @Last Modified time: 2018-02-01 17:41:20

##################


import csv,codecs 

f = codecs.open('temp.csv', 'w', 'utf_8_sig') 
writer = csv.writer(f)  
writer.writerow(['奥迪','爱迪生','方法'])  
f.close()

f = codecs.open('temp.csv', 'r', 'utf_8_sig') 
for i in f:
	print (i)

