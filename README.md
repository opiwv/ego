# ego
 social network map

map_and_metrics.PNG represents a social network or "ego" map that was genereated using kumu.io 

link to my kumu project if you would like to test some of the metrics and network cloud customization:
https://kumu.io/opiwv/opiwv-ego

# explanation
the value represented in the table to the left of the map is the number of times the host accoount (my own) retweets the target account
my own account shows a value of 315 because comments on my own posts are counted as retweets, so the first table entrie is faulty

each table entry below that is a user and number of times i have retweeted them. these are graphically represented on the network map 
by the size of the user icon, and a node that represents what the value is for that user or users. 

in order to generate this map, I had to retrieve twitter developer access for my account and get access to specific keys which where then used in 
SFM as I seeded a project that did a one time retrieval of all tweets on my own timeline and returned every pertinent metric in a JSON file. 

the JSON files were then handled in python to retrieve only desired columns and return them to CSV which were then used in Kumu. 
Kumu is a web-based program (SaaS) that allows you to conduct in depth analysis and cloud graphing once you have registered an account. 

this personal project was an integration of big data principles in the retrieval of all metadata from my persona social media account, 
coding through python and data handling, and the use of a distributed application / software as a service on the kumu website. 

documentation included below, as well as coding-relevant documentation in the header of the python file.

# documentation
building network vizualizations tutorial - https://gwu-libraries.github.io/sfm-ui/posts/2017-09-08-sna
social feed manager - http://sfm1.cs.vt.edu:8084/ui/
code template for big data extraction - https://nbviewer.jupyter.org/github/gwu-libraries/notebooks/blob/master/20170720-building-social-network-graphs-JSON.ipynb
kumu - https://kumu.io
kumu data handling - http://slob.coplacdigital.org/course/2017/02/21/social-network-mapping-part-iii-importing-data-to-kumu/

