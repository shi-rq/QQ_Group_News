# QQ_Group_News
Using machine learning to filter messages in a QQ group that is most likely to be news.  
A test set of QQ group messages is needed, with individual message in such format:  
>Nickname(1234567890)  19:06:25  
>要来了要来了

## 1. Nearest_Neighbour
In this version, 4 features are collected from each training sample:  
* Feature 1: Message length
* Feature 2: The ASCII code of the first character
* Feature 3: Heat, namely the number of messages in the next 5 minutes
* Feature 4: Discussion, namely the number of users in the next 5 minutes, +1 once the speaker changes
