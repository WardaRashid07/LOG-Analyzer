import re
import logging
from datetime import datetime
import csv
from pattern import PATTERN

logging.basicConfig(level = "INFO" ,format =" '%(asctime)s ' | ' %(levelname)s' | '%(message)s'   "  , datefmt="%H::%M::%S")
logger = logging.getLogger("Log Analyzer : Project #03  ")
errorss=[]
t=[]
m=[]
l=[]
c=[]
crupts=[]
crupt=0
frequency={}
path = r"C:\Users\warda\Downloads\application.log"
with open(path,newline='')as file , open('log_summmary.csv', 'w',newline='') as output:
    info=0
    warn=0
    debug=0
    error=0
    csv_writer = csv.writer(output)
    csv_writer.writerow(['Timestamp', 'level', 'Component', 'Message'])
    for i,line in enumerate(file):

        a = re.search(PATTERN,line)

        if a is not None:
               # if i <=5 and a is not None:
               #     print(f"line {i} = {a.group()}")
               #     print(a.group(1) ,  " : " , a.group(2) , " :  " ,a.group(3) , "  :  " , a.group(4))
               #     print(f"line ")
               #     # print(f"{lines}")
               t.append(datetime.strptime(a.group(1),'%Y-%m-%d %H:%M:%S'))
               l.append(a.group(2))
               c.append(a.group(3))
               m.append(a.group(4))
               if a.group(2) == 'INFO':
                   info += 1
               elif a.group(2) == 'DEBUG':
                   debug += 1
               elif a.group(2) == 'WARN':
                   warn += 1
               elif a.group(2) == 'ERROR':
                   error += 1
               csv_writer.writerow([a.group(1), a.group(2), a.group(3), a.group(4)])


        else:
            crupt+=1
            crupts.append(line)
            logger.warning("warning: log did not matched ")

    freq = {}
    for times in t:
        freq[times.hour] = freq.get(times.hour, 0) + 1

    print( " number of levels = ", len(set(l)))
    print(freq)
    frequency['Info'] = info
    frequency['Warning'] = warn
    frequency['Error'] = error
    frequency['Debug'] = debug
    print( "total lines processed  = " , i)
    print( f" total valid lines = {(i - crupt)} and  total invalid lines = {crupt}")
    print(" count per log level :")
    print(f" num if INFO logs = {frequency['Info']} ,   num of warning logs  = {frequency['Warning']} , number of Error logs = {frequency['Error']}, number of Debug logs = {frequency['Debug']}")



with open('errors.log' ,'w') as errors_file:
      errors_file.writelines(crupts)






