import numpy as np
import pickle
from optparse import OptionParser
import os.path

NB_ALGO = 4
NB_MIX = 3
PROPERTIES = ["qualite", "defauts"]


def to_float(a):
	try:
		return float(a)
	except:
		return -1

def acqu(sujet):
	rep = []
	print()
	print("________ ACQUIRE SUBJECT", sujet)
	print()
	for algo in range(NB_ALGO):
		print("____ ALGO", algo + 1)
		print()
		rep.append({})
		for mix in range(NB_MIX):
			print("___ MIX", mix + 1)

			for pro in PROPERTIES:
				if pro not in rep[algo]:
					rep[algo][pro] = []
				print(pro + ": ", end="")
				temp = to_float(input(""))
				while (temp < -5 or temp > 5):
					print("Incorect input, please try again.")
					temp = to_float(input(""))
				rep[algo][pro].append(temp)
		print()

	for algo in range(NB_ALGO):
		for pro in PROPERTIES:
			rep[algo][pro] = np.mean(rep[algo][pro])
						
	print()

	return rep


class Data():
	def __init__(self):
		self.results = {}

	def load(self, name):
		if os.path.isfile(name):
			self.results =  pickle.load(open(name, "rb"))  
		else:
			print("This database does not exist, we start from a new one.")

	def save(self, name):
		pickle.dump(self.results, open(name, "wb"))  

	def acquire(self, subject):
		rep = "y"
		if subject in self.results:
			print("This subject is already enrolled into the database, would you like to replace it? y/N")
			rep = str(input())[0:1]
			while (rep not in ["y", "N", "n", ""]):
				print(rep)
				print("Incorect input, please try again.")
				rep = str(input())[0]
		if rep == "y":
			print("Erasing previous data.")
			self.results[subject] = acqu(subject)
		else:
			print("We skip subject", subject)

	def getRes(self, subject):
		if subject in self.results:
			return self.results[subject]
		else:
			print("Subject", subject, "is not enreolled in the database.")

	def print(self):
		for subject in self.results:
			print("______ Subject", subject)
			print()
			k = 1
			for algo in self.getRes(subject):
				print("___ ALGO", k)
				for item in algo:
					print(item + ": " + str(algo[item]))
				print()
				k += 1

	def automaticFill(self, n):
		for subject in range(n):
			rep = []
			for algo in range(NB_ALGO):
				rep.append({})
				for pro in PROPERTIES:
					rep[algo][pro] = np.random.normal(5)
			self.results[subject] = rep

	def analyse(self):
		algos = {}
		for subject in self.results:
			k = 1
			for algo in self.getRes(subject):
				if k not in algos:
					algos[k] = []

				## A revoir
				score = (algo["qualite"] + (10 - algo["defauts"]))/2

				algos[k].append(score)

				k += 1

		for algo in algos:
			print("___ Algo", algo)
			mean = np.mean(algos[algo])
			standart_deviation = np.std(algos[algo])
			algos[algo] = (mean, standart_deviation)
			print("mean:", mean)
			print("standart deviation:", standart_deviation)
		return algos

if __name__ == "__main__":

	usage = "usage: %prog [options] <subject to fill>"
	parser = OptionParser(usage)

	parser.add_option("-d", "--name", type="string",
					  help="Name of the database.",
					  dest="name", default="DATA_ANECHOIC.sm")

	parser.add_option("-p", "--print", type="string",
					  help="1 if you want to print the data.",
					  dest="pprint", default="0")

	options, arguments = parser.parse_args()

	D = Data()
	D.load(options.name)

	if options.pprint == "1":
		D.print()

	if len(arguments) == 1:
		try:
			D.acquire(int(arguments[0]))
			D.save(options.name)
		except ValueError:
			print("The subject you passed is not valid, must be int.")

	else:
		parser.error("You have to specify the subject you want to fill.")

