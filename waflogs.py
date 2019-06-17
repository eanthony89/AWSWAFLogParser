# CLI based WAF logs parser
# Author: Eric Anthony
# Revision: 1


#!/usr/local/bin/python3.6
import argparse
import json
import pprint
from datetime import datetime, timezone

# define variables:
select = []
file = ""
count = 0

parser = argparse.ArgumentParser()

parser.add_argument('-filter', required=False , action='store', dest='select', default= None , type = str , help='Specify the search filter that you want to use to select specific requests . This can be be used to match any value in the logs like a IP address, country name , headers or Rule id. You can also join filters together using statements like cf.mywebsite.com/index.html,192.168.1.1,BLOCK   or  ApacheBench/2.3&BLOCK or  192.168.1.1,172.16.23.12,10.3.1.1 .')
parser.add_argument('-display', required=False , action='store_true', default=False, dest='display',help='Use this flag to print out all the requests that have matched the specified filter. Might generate a large output so it might be a good idea to CAT the output to file')
parser.add_argument('-file', required=True , action='store', dest='file' ,help='Specify the location of the log file')
parser.add_argument('-time', required=False , action='store', dest='timerange' , default= None , type = str , help='Specify the start and end datetime in format dd/mm/yyyy-hh:mm:ss separated by a "," eg 01/10/2018-01:10:20,01/10/2018-01:20:30')
parser.add_argument('-matchany', required=False , action='store_true', default=False, dest='matchany',help='Setting this flag finds requests that match any one or more filters.By default only requests that match all filters will be selected.')

results = parser.parse_args()


if results.select:
	try:
		if "," in results.select:
			select = results.select.split(",")
		elif results.select == None:
			select = []
		else:
			select.append(results.select)
	except AssertionError as e:
		print (e)
	except:
		msg = "Not a valid filter"
		raise argparse.ArgumentTypeError(msg)

if results.timerange:
	try:
		timerange = list(results.timerange.split(","))
		start_time = datetime.strptime(timerange[0], "%d/%m/%Y-%H:%M:%S").replace(tzinfo=timezone.utc)
		end_time = datetime.strptime(timerange[1], "%d/%m/%Y-%H:%M:%S").replace(tzinfo=timezone.utc)
		assert start_time <= end_time, "Start time cannot be ahead of end time"
	except ValueError:
		raise ValueError("Incorrect input data format, should be dd/mm/yyyy-hh:mm:ss,dd/mm/yyyy-hh:mm:ss ")
	except AssertionError as e:
		print (e)

#IF USER USES DISPLAY OPTION

if results.display == True:
	# USER ENTERS FILTER WITH MATCHALL , NO DATE
	if results.select != None and results.timerange == None and results.matchany == False:
		with open(results.file) as infile:
			for line in infile:
				if all(x in line for x in select):
					d = json.loads(line)
					d["timestamp"] = (datetime.fromtimestamp((int(d["timestamp"])/1000.0),timezone.utc)).strftime("%d/%m/%Y %H:%M:%S %Z")
					pprint.pprint(d)
					print ("==============================================================================\n")
					count +=1
	# USER ENTERS FILTER WITH MATCHANY , NO DATE
	elif results.select != None and results.timerange == None and results.matchany == True:
		with open(results.file) as infile:
			for line in infile:
				if any(x in line for x in select):
					d = json.loads(line)
					d["timestamp"] = (datetime.fromtimestamp((int(d["timestamp"])/1000.0),timezone.utc)).strftime("%d/%m/%Y %H:%M:%S %Z")
					pprint.pprint(d)
					print ("==============================================================================")
					count +=1
	# USER ENTERS DATE BUT NO FILTER
	elif results.select == None and results.timerange != None:
		with open(results.file) as infile:
			for line in infile:
				d = json.loads(line)
				d["timestamp"] = (datetime.fromtimestamp((int(d["timestamp"])/1000.0),timezone.utc))
				if d["timestamp"] >= start_time and d["timestamp"] <= end_time:
					d["timestamp"] = (d["timestamp"].replace(tzinfo=timezone.utc)).strftime("%d/%m/%Y %H:%M:%S %Z")
					pprint.pprint(d)
					print ("==============================================================================")
					count +=1
	# USER ENTERS DATE AND FILTER AND MATCHALL
	elif results.select != None and results.timerange != None and results.matchany== False:
		with open(results.file) as infile:
			for line in infile:
				if all(x in line for x in select):
					d = json.loads(line)
					d["timestamp"] = (datetime.fromtimestamp((int(d["timestamp"])/1000.0),timezone.utc))
					if d["timestamp"] >= start_time and d["timestamp"] <= end_time:
						d["timestamp"] = (d["timestamp"].replace(tzinfo=timezone.utc)).strftime("%d/%m/%Y %H:%M:%S %Z")
						pprint.pprint(d)
						print ("==============================================================================")
						count +=1
	# USER ENTERS DATE AND FILTER AND MATCHANY
	elif results.select != None and results.timerange != None and results.matchany == True:
		with open(results.file) as infile:
			for line in infile:
				if any(x in line for x in select):
					d = json.loads(line)
					d["timestamp"] = (datetime.fromtimestamp((int(d["timestamp"])/1000.0),timezone.utc))
					if d["timestamp"] >= start_time and d["timestamp"] <= end_time:
						d["timestamp"] = (d["timestamp"].replace(tzinfo=timezone.utc)).strftime("%d/%m/%Y %H:%M:%S %Z")
						pprint.pprint(d)
						print ("==============================================================================")
						count +=1
	# USER DOES NOT ENTER DATE AND FILTER
	else:
		with open(results.file) as infile:
			for line in infile:
				d = json.loads(line)
				d["timestamp"] = (datetime.fromtimestamp((int(d["timestamp"])/1000.0),timezone.utc)).strftime("%d/%m/%Y %H:%M:%S %Z")
				pprint.pprint(d)
				print ("==============================================================================")
				count +=1

	print ("Total number of hits matching this filter : " + str(count))



#IF USER NOT USES DISPLAY OPTION - ONLY COUNTER WILL BE SHOWN THAT MATCHED THE REQUESTS
else  :

	# USER ENTERS FILTER WITH MATCHALL , NO DATE
	if results.select != None and results.timerange == None and results.matchany == False:
		with open(results.file) as infile:
			for line in infile:
				if all(x in line for x in select):
					count +=1
	# USER ENTERS FILTER WITH MATCHANY , NO DATE
	elif results.select != None and results.timerange == None and results.matchany == True:
		with open(results.file) as infile:
			for line in infile:
				if any(x in line for x in select):
					count +=1
	# USER ENTERS DATE BUT NO FILTER
	elif results.select == None and results.timerange != None:
		with open(results.file) as infile:
			for line in infile:
				d = json.loads(line)
				d["timestamp"] = (datetime.fromtimestamp((int(d["timestamp"])/1000.0),timezone.utc))
				if d["timestamp"] >= start_time and d["timestamp"] <= end_time:
					count +=1
	# USER ENTERS DATE AND FILTER AND MATCHALL
	elif results.select != None and results.timerange != None and results.matchany == False:
		with open(results.file) as infile:
			for line in infile:
				if all(x in line for x in select):
					d = json.loads(line)
					d["timestamp"] = (datetime.fromtimestamp((int(d["timestamp"])/1000.0),timezone.utc))
					if d["timestamp"] >= start_time and d["timestamp"] <= end_time:
						count +=1
	#USER ENTERS DATE AND FILTER AND MATCHANY
	elif results.select != None and results.timerange != None and results.matchany == True:
		with open(results.file) as infile:
			for line in infile:
				if any(x in line for x in select):
					d = json.loads(line)
					d["timestamp"] = (datetime.fromtimestamp((int(d["timestamp"])/1000.0),timezone.utc))
					if d["timestamp"] >= start_time and d["timestamp"] <= end_time:
						count +=1
	# USER DOES NOT ENTER DATE AND FILTER
	else  :
		with open(results.file) as infile:
			for line in infile:
				count +=1

	print ("Total number of hits matching this filter : " + str(count))
