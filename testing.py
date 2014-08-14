import  pickle
from string import digits
import string
import math

discardList=["In-Reply-To:","Reply-To:","X-Newsreader:","-archive-name:","X-X-From:","X-Disclaimer:","X-Us-Mail:","X-Telephone:","X-Sequence:","X-UserAgent:","X-XXDate:","X-Cc:","X-To:","X-XXMessage-ID:","wrote","X-Received:","Version:","Mime-Version:","Last-update:","Last-modified:","Followup-To:","Expires:","Supersedes:","In article ","from article ","From article ","X-Mailer:","writes:","Xref:","Path:","Newsgroups:","From:","Nntp-Posting-Host:","Sender:"  ,"Organization:" ,"Lines:" , "References:" , "Article-I.D.:" , "Date:" ,"Approved:", "Message-ID:"];
#words to remove :
# Adding words to remove list
fname = "english-stop-words.txt"
fhand = open(fname)
wordsToRemove = ();
for line in fhand:
    wordsToRemove = line.split(',')


#get classifying lists
pkl_file = open('list.pkl', 'rb')
list = pickle.load(pkl_file)
pkl_file.close()

#get categories list
pkl_file2 = open('categories.pkl', 'rb')
cat = pickle.load(pkl_file2)
pkl_file2.close()

hashlist=dict();
fname = "test"
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
            if ((len(word) < 15) ) and ( "'" not in word ) and ( "." not in word ) and (word not in wordsToRemove):
                if word not in hashlist:
                    hashlist[word] = 1
                else:
                    hashlist[word] += 1
hashlist = sorted(hashlist.items(), key=lambda x: x[1], reverse=True)

classifyList =[0]*20;
hashlist =dict(hashlist)
counter = 0 ;
print hashlist;
for l in list:
    l = dict(l)
    for item in hashlist:
        if item in l:
            classifyList[counter]+= hashlist[item]*abs(math.log(l[item],10));   
    #classifyList[counter]+= abs(math.log(cat[counter][1]*1.0/cat[-1][1]))
    counter+=1;
   
maximum =  max(classifyList)
max_index = classifyList.index(maximum)
print maximum
print classifyList
print "category is : ",cat[max_index][0]