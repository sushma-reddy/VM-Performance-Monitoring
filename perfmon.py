import time

import libvirt



cl = libvirt.open("qemu:///system")





def getAllStats(array):

	cArr = []

	mArr = []



	for item in array:

		dom = cl.lookupByID(item)

		cstats = dom.getCPUStats(True)

		mstats = dom.memoryStats()

		cArr.append(cstats[0]['cpu_time'])

		mArr.append(mstats['available'] - mstats['unused'])



	return [cArr, mArr]





def getPercentUsage(arr1, arr2):

	out = []

	

	for i in range(len(arr1)):

		temp = (arr2[i] - arr1[i]) * 100 / arr1[i]

		out.append(temp)



	return out





def printOut(array, sortedTuples):

	for i in range(len(array)):

		print "Domain: ", cl.lookupByID(array[sortedTuples[i][0]]).name(), "Usage: ", str(sortedTuples[i][1])





def main():

	print "Enter 1 for CPU usage. 2 for Memory stats"

	input1 = raw_input()

	print "Enter threshold percentage"

	input2 = raw_input()

	fh = open("alerts.txt","w")
	fh.write("Below are the CPU usage alerts\n") 

	array = cl.listDomainsID()

	t1 = getAllStats(array)

	time.sleep(1)

	t2 = getAllStats(array)



	cpu = getPercentUsage(t1[0], t2[0])



	if int(input1) == 1:

		sortedCPU = sorted(enumerate(cpu), key = lambda x:x[1])

		printOut(array, sortedCPU)



	elif int(input1) == 2:

		mem = getPercentUsage(t1[1], t2[1])	

		sortedMEM = sorted(enumerate(mem), key = lambda x:x[1])

		printOut(array, sortedMEM)



	else:

		print "Program terminated. Enter 1 for CPU usage. 2 for Memory stats"

		exit(0)



	if 0 <= int(input2) <= 100:

		for i, c in enumerate(cpu):

			if c >= int(input2):

				temp = cl.lookupByID(array[i]).name() + ' ' + str(c) + ' ' +  str(time.ctime())  + '\n'
				print temp
				fh.write(temp)

	else:

		print "Program terminated. Percentages lie between 0 and 100"

		exit(0)





if __name__== "__main__":

	main()
