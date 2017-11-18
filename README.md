The goal of this is to strip beer prices from The Beer Store website.

Status:
* Able to collect and store links to all unique beer pages
* Able to strip information about a given beer from webpage
* Able to populate an array with all the data the output sorted data to file in JSON format


Multithread update:
* Able to strip all of The Beer Store in <20 sec
* Executable on AWS Lambda(1)


(1)	NOTE:
	For execution on lambda if statement in def main() needs to be changed to check for equality with 'lambda_function' instead of '__main__'