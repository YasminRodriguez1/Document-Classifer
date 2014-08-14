import os
import string 
from string import digits
import math
import pylab


N=200
hashlist_sum = 0 ;

discardList=["In-Reply-To:","Reply-To:","X-Newsreader:","-archive-name:","X-X-From:","X-Disclaimer:","X-Us-Mail:","X-Telephone:","X-Sequence:","X-UserAgent:","X-XXDate:","X-Cc:","X-To:","X-XXMessage-ID:","wrote","X-Received:","Version:","Mime-Version:","Last-update:","Last-modified:","Followup-To:","Expires:","Supersedes:","In article ","from article ","From article ","X-Mailer:","writes:","Xref:","Path:","Newsgroups:","From:","Nntp-Posting-Host:","Sender:"  ,"Organization:" ,"Lines:" , "References:" , "Article-I.D.:" , "Date:" ,"Approved:", "Message-ID:"];


def testfile(fname,list):
    hashlisttest=dict();
    fhand = open(fname)
    for line in fhand:
        discardline = 0;
        for item in discardList:
            if item in line: 
                discardline=1;
                break;
        if discardline == 0 :  
            line =line.translate(None, digits)
            string.punctuation=string.punctuation.replace(".","")
            string.punctuation=string.punctuation.replace("'","")

            line = line.translate(None, string.punctuation)    # New Code
            line = line.lower()                                # New Code
            words = line.split()
            for word in words:
                if word.endswith("."):
                    word=word[:-1]
              
                if ((len(word) < 15) ) and ( "'" not in word )and ((len(word) > 0)) and ( "." not in word ) and (word not in wordsToRemove):
                    if word not in hashlisttest:
                        hashlisttest[word] = 1
                    else:
                        hashlisttest[word] += 1
    hashlisttest = sorted(hashlisttest.items(), key=lambda x: x[1], reverse=True)

    classifyList =[0]*20;
    hashlist =dict(hashlisttest)
    counter = 0 ;
    for l in list:
        l = dict(l)
        for item in hashlist:
            if item in l:
                classifyList[counter]+= hashlist[item]*abs(math.log(l[item],10));    
            else:
                classifyList[counter]+= hashlist[item]*abs(math.log((1.0/(1+hashlist_sum)),10));    

        counter+=1;
    
    maximum =  max(classifyList)
    max_index = classifyList.index(maximum)
    return max_index

#end
# Adding words to remove list
fname = "english-stop-words.txt"
fhand = open(fname)
wordsToRemove = ();
for line in fhand:
    wordsToRemove = line.split(',')
    
def trainAndTestWithN(N):
    list = [];
    cat = [];
    sum_of_files = 0 ;
    ctr=0; #counter for trainning , max = 800
    #going through directories
    for root, dirs ,files in os.walk("20_newsgroups"):
        for dir in dirs: 
            #keda ana gowa el directory
            x= os.path.join(root,dir)
            hashlist=dict();
            for root1,dir2,files1 in os.walk(x):
                sum_of_files +=len(files1);
                cat.append((dir,len(files1)));
                for file in files1:
                    ctr +=1;
                    if ctr > 800 :
                        break;
                    #keda ma3aya file file
                    fname = os.path.join(root,dir,file)
                    fhand = open(fname)
                    for line in fhand:
                        discardline = 0;
                        for item in discardList:
                            if item in line: 
                                discardline=1;
                                break;
                        if discardline == 0 :  
                            line =line.translate(None, digits)
                            string.punctuation=string.punctuation.replace(".","")
                            string.punctuation=string.punctuation.replace("'","")
    
                            line = line.translate(None, string.punctuation)    # New Code
                            line = line.lower()                                # New Code
                            words = line.split()
                            for word in words:
                                if word.endswith("."):
                                    word=word[:-1]
                                if ((len(word) < 15) ) and ((len(word) > 0))and ( "'" not in word ) and ( "." not in word ) and (word not in wordsToRemove):
                                    if (word not in hashlist):
                                        hashlist[word] = 1
                                    else:
                                        hashlist[word] += 1
                ctr=0;
            hashlist.update((x, (y+1)) for x, y in hashlist.items())
            hashlist = sorted(hashlist.items(), key=lambda x: x[1], reverse=True)

            hashlist=hashlist[:N]
            hashlist=dict(hashlist)
            hashlist_sum = sum(hashlist.values());
            hashlist.update((x, y*1.0/hashlist_sum) for x, y in hashlist.items())
            hashlist = sorted(hashlist.items(), key=lambda x: x[1], reverse=True)
            list.append(hashlist);
    cat.append(("sum",sum_of_files));
    
    
    #end of training
    
    #testing from 801 to end.
    ctr=0;
    dirctr = 0;
    c =[(0,0)]*20; #counter
    for root, dirs ,files in os.walk("20_newsgroups"):
        for dir in dirs:
            
            #keda ana gowa el directory
            x= os.path.join(root,dir)
            for root1,dir2,files1 in os.walk(x):
                for file in files1:
                    if ctr < 801 :
                        ctr+=1;
                    else:
                        ctr+=1
                        fname = os.path.join(root,dir,file)
                        classify = testfile(fname,list);
                        if dirctr == classify:
                            c[dirctr]=((c[dirctr][0]+1),(c[dirctr][1]))
                        else:
                            c[dirctr]=((c[dirctr][0]),(c[dirctr][1]+1))
                ctr=0
            dirctr+=1;
    accuracy = 0
    for x in c:
        accuracy += x[0]*1.0/(x[0]+x[1]);
    accuracy = accuracy*1.0/20    

    return (N,accuracy)
    
x =[];
y=[];
for i in xrange(100,9000,100):
  result = trainAndTestWithN(i)
  print result
  x.append(result[0])
  y.append(result[1])


pylab.plot(x,y)
pylab.show()
