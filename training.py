import os
import string
from string import digits

import pickle

discardList=["In-Reply-To:","Reply-To:","X-Newsreader:","-archive-name:","X-X-From:","X-Disclaimer:","X-Us-Mail:","X-Telephone:","X-Sequence:","X-UserAgent:","X-XXDate:","X-Cc:","X-To:","X-XXMessage-ID:","wrote","X-Received:","Version:","Mime-Version:","Last-update:","Last-modified:","Followup-To:","Expires:","Supersedes:","In article ","from article ","From article ","X-Mailer:","writes:","Xref:","Path:","Newsgroups:","From:","Nntp-Posting-Host:","Sender:"  ,"Organization:" ,"Lines:" , "References:" , "Article-I.D.:" , "Date:" ,"Approved:", "Message-ID:"];

N=200
# Adding words to remove list
fname = "english-stop-words.txt"
fhand = open(fname)
wordsToRemove = ();
for line in fhand:
    wordsToRemove = line.split(',')

list = [];
cat = [];
sum_of_files = 0 ;
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
                            if ((len(word) < 15) ) and ( "'" not in word ) and ( "." not in word ) and (word not in wordsToRemove):
                                if word not in hashlist:
                                    hashlist[word] = 1
                                else:
                                    hashlist[word] += 1
        hashlist.update((x, (y+1)) for x, y in hashlist.items())
        hashlist_sum = sum(hashlist.values());
        hashlist.update((x, y*1.0/hashlist_sum) for x, y in hashlist.items())

        hashlist = sorted(hashlist.items(), key=lambda x: x[1], reverse=True)
        list.append(hashlist[:N]);
cat.append(("sum",sum_of_files));
output = open('list.pkl', 'wb')
pickle.dump(list, output)
output.close()

output = open('categories.pkl', 'wb')
pickle.dump(cat, output)
output.close()