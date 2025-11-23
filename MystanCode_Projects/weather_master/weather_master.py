"""
File: weather_master.py
Name:
-----------------------
This program should implement a console program
that asks weather data from user to compute the
average, highest, lowest, cold days among the inputs.
Output format should match what is shown in the sample
run in the Assignment 2 Handout.

"""

EXIT = -100  #sentinel value

def main():
	"""
	Pre-condition: input integer temperatures
	Post-condition: print highest, lowest, average temperature and the number of cold days (temperature<16)
	"""
	print ("stanCode \"Weather Master 4.0\"!")
	temp = int(input('Next Temperature: (or -100 to quit)? '))


	while True:
		if temp == EXIT:
			print('No temperature were entered.')
			break
		else:
			max_temp=temp
			min_temp=temp
			total=temp
			count=1
			cold_days=0
			if temp < 16:
				cold_days+=1


			while True:
				temp = int(input('Next Temperature: (or -100 to quit)? '))
				if temp == EXIT:
					break
				else:
					total+=temp
					count+=1
					avg=total/count
					if temp < 16:
						cold_days+=1
					if temp > max_temp:
						max_temp = temp
					if temp < min_temp:
						min_temp = temp

		print("Highest temperature = " + str(max_temp))
		print("Lowest temperature = " + str(min_temp))
		print("Average = " + str(avg))
		print(str(cold_days) + " cold day(s)")






# DO NOT EDIT CODE BELOW THIS LINE #

if __name__ == "__main__":
	main()
