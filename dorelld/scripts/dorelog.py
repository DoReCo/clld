# To log different operations

from datetime import datetime
import os

def dorelog(text,f="",d="",mode="w",typ=""):
    """To create a log of all operations.
    ARGUMENTS:
    - 'text'        :   the text to log"""
    
    if not text:
        return ""
        # Append
    if mode == "a":
        if os.path.isfile(f):
            with open(f,'a',encoding="utf-8") as file:
                file.write(text)
            return f
        else:
            return ""
        # Create
        ## folder
    log_d = os.path.join(os.path.abspath(os.path.dirname(__file__)),"log")
    #print('***********************', log_d)
    cre = str(datetime.today().strftime('%d.%m.%Y'))
    if typ:
        cre = typ+"_"+cre
    if d:
        log_d = d
    if not os.path.isdir(log_d):
        os.mkdir(log_d)
        ## file
    log_f = os.path.join(log_d,cre)
    incr = 1; temp = log_f
    while os.path.isfile(temp):
        temp = log_f+"_"+str(incr); incr += 1
    log_f = temp
        ## text
    with open(log_f,'w',encoding="utf-8") as file:
        file.write(text)
    return log_f
