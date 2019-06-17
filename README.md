I have created this dirty script that parses through WAF logs . It currently supports the following: 1) Searching requests that fall within a starttime and endtime. 2) Searching requests that match one or more strings in the logs. You can enter multiple search strings together and use a "matchall" or "matchany". 3) Choose to view all the requests that matched the search (in indented JSON format) or just see the number of requests that matched the search.



The script:
==========

-Uses python3.
-Loads each request one at a time into memory instead of loading the whole Log file. This might come handy in parsing through large files.

Usage:
=====


ubuntu@ip-10-10-2-207:~$ python3 waflogs.py -h
usage: waflogs.py [-h] [-filter SELECT] [-display] -file FILE
                  [-time TIMERANGE] [-matchany]

optional arguments:
  -h, --help       show this help message and exit
  -filter SELECT   Specify the search filter that you want to use to select
                   specific requests . This can be be used to match any value
                   in the logs like a IP address, country name , headers or
                   Rule id. You can also join filters together using
                   statements like
                   cf.mywebsite.com/index.html,192.168.1.1,BLOCK or
                   ApacheBench/2.3&BLOCK or 192.168.1.1,172.16.23.12,10.3.1.1
                   .
  -display         Use this flag to print out all the requests that have
                   matched the specified filter. Might generate a large output
                   so it might be a good idea to CAT the output to file
  -file FILE       Specify the location of the log file
  -time TIMERANGE  Specify the start and end datetime in format dd/mm/yyyy-
                   hh:mm:ss separated by a "," eg
                   01/10/2018-01:10:20,01/10/2018-01:20:30
  -matchany        Setting this flag finds requests that match any one or more
                   filters.By default only requests that match all filters
                   will be selected.

Examples :

*To count the number of requests that were blocked and contain "341414dfsfr4re0fddf/test.html"
python3 waflogs.py -file waflog.txt -filter BLOCK,341414dfsfr4re0fddf/test.html

*To count  and show the number of requests that were blocked and contain "341414dfsfr4re0fddf/test.html"
python3 waflogs.py -file waflog.txt -filter BLOCK,341414dfsfr4re0fddf/test.html

*To count and show the number of requests that were allowed and fall within 01/10/2018-01:10:10 and 01/10/2018-01:20:30 UTC.
python3 waflogs.py -file waflog.txt -filter ALLOW -time 01/10/2018-01:10:10,01/10/2018-01:20:30 -display

*To count and show the number of requests that were allowed and fall within 01/10/2018-01:10:10 and 01/10/2018-01:20:30 UTC.
python3 waflogs.py -file waflog.txt -filter ALLOW -time 01/10/2018-01:10:10,01/10/2018-01:20:30 -filter BLOCK,341414dfsfr4re0fddf/test.html -display

python3 waflogs.py -file waflog.txt -filter ALLOW -time 01/10/2018-01:10:10,01/10/2018-01:20:30 -filter 1.2.3.4,10.4.5.2,3.5.6.7 -display -matchany
