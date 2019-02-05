import datetime
from optparse import OptionParser

def getTime(n, K, k2, k3, k4, k5=0):
	return n*(4*k2 +  8*k4 + 4*k3 + 16 * K) + (n-1)*k5

if __name__ == "__main__":

	usage = "usage: %prog [options] <path to database>"
	parser = OptionParser(usage)

	parser.add_option("-n", "--mixtures", type="int",
					  help="Number of mixture to pass on.",
					  dest="n")

	parser.add_option("-k", "--length", type="float",
					  help="Duration of the musical extract.", 
					  dest="k")

	parser.add_option("-a", "--k1", type="float",
					  help="Pause between the mix and the extracted sources.", 
					  dest="k1")

	parser.add_option("-b", "--k2", type="float",
					  help="Pause between two algorithm results.", 
					  dest="k2")

	parser.add_option("-c", "--k3", type="float",
						  help="Pause between two source listening.", 
						  dest="k3")

	parser.add_option("-d", "--k4", type="float",
						  help="Pause between two mixtures.", 
						  dest="k4")

	options, arguments = parser.parse_args()



	if options.n is not None and options.k is not None and options.k1 is not None and \
		 options.k2 is not None and options.k3 is not None and options.k4 is not None:
		print(str(datetime.timedelta(seconds=getTime(options.n, options.k, options.k1, options.k2, options.k3, options.k4))))

	elif options.n is not None and options.k is not None and options.k1 is not None and \
		 options.k2 is not None and options.k3 is not None:     

		if options.n > 1:
			parser.error("You must provide a pause value between two mixtures.")
		else:
			print(str(datetime.timedelta(seconds=getTime(options.n, options.k, options.k1, options.k2, options.k3))))

	else:
		parser.error("You have to specify at least the first 5 options.")
