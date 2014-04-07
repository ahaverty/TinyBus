#!/usr/bin/python
#
# OLED 4x20 Test Script for
# Raspberry Pi
#
# Author : Alan Haverty
# Site   : http://www.ahaverty.com
# 
# Date   : 25/02/2014
#

# The wiring for the LCD is as follows:
# 1 : GND
# 2 : 5V
# 3 : 				- GROUND THIS PIN/NOT USED
# 4 : RS (Register Select)
# 5 : R/W (Read Write)       	- GROUND THIS PIN
# 6 : Enable or Strobe
# 7 : Data Bit 0             	- NOT USED
# 8 : Data Bit 1             	- NOT USED
# 9 : Data Bit 2             	- NOT USED
# 10: Data Bit 3             	- NOT USED
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: 				- NOT USED
# 16: 				- NOT USED

#import
import RPi.GPIO as GPIO
import time
from datetime import datetime
import lxml.html as lh
import nltk
from urllib import urlopen

# Define GPIO to LCD mapping

LCD_RS = 8
LCD_E  = 10
LCD_D4 = 18
LCD_D5 = 22
LCD_D6 = 24
LCD_D7 = 26

# Define some device constants
LCD_WIDTH = 20    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 128   # 00 LCD RAM address for the 1st line
LCD_LINE_2 = 192   # 40 LCD RAM address for the 2nd line
LCD_LINE_3 = 148   # 14 LCD RAM address for the 3rd line
LCD_LINE_4 = 212   # 54 LCD RAM address for the 4th line

# Timing constants
MAX_EXEC = 0.0006

E_PULSE = 0.00005   #0.0001
E_DELAY = 0.00005   #0.00005

# Setting modes

GPIO.setmode(GPIO.BOARD)     # Use BOARD numbers
GPIO.setup(LCD_E, GPIO.OUT)  # E
GPIO.setup(LCD_RS, GPIO.OUT) # RS
GPIO.setup(LCD_D4, GPIO.OUT) # DB4
GPIO.setup(LCD_D5, GPIO.OUT) # DB5
GPIO.setup(LCD_D6, GPIO.OUT) # DB6
GPIO.setup(LCD_D7, GPIO.OUT) # DB7


# Initialise display


def main():

	lcd_init()

	# Keep loop open and auto update information
	while(True):
		bus_program()

	lcd_byte(0x08,LCD_CMD) # Turn off display
	time.sleep(MAX_EXEC)

def scraper():

	# Test bus page for after midnight
	page = "http://www.ahaverty.com/tiny/bus15.htm"

	# Live bus page
	#page = "http://www.dublinbus.ie/en/RTPI/Sources-of-Real-Time-Information/?searchtype=view&searchquery=4339"


	html = urlopen(page).read()
	doc = lh.fromstring(html)
	val = []

	i=0
	j=0

	for tr in doc.cssselect('#rtpi-results td:nth-child(-n+1)'):
		if(i<3):
			val.append(nltk.clean_html(tr.text_content()))
			i+=1

		# Skip col of images and move to new row
		else:
			i=0
			j+=1

	for k in range(0,j*3):
		val[k] = val[k][:8] + (val[k][8:] and '..')    # Shorten bus description and add trail if over 8 chars long

	print val[k] # Test output onscreen

	return(val)

def bus_program():
# Main program for bus info output

	bus = scraper()

	busMes = []

	maxBus = len(bus)
	maxRow = maxBus/3


	# Test for onscreen output
	print("Bus ")
	print(maxBus)
	print("Row ")
	print(maxRow)


	j=0
	i=0

	# Creates the messages for output
	while(j<maxRow):

		# If bus isn't 'Due', format time for calculation
		if(bus[i+2]!='Due'):
			s1=bus[i+2]
			localtime = time.localtime()
			s2=time.strftime("%H:%M", localtime)

			FMT = '%H:%M'

			tdelta = datetime.strptime(s1,FMT) - datetime.strptime(s2,FMT)

			timeleft = str(tdelta)
			timeleftfrm = timeleft[2:4]+"min"

		# Else format Due for output
		else:
			timeleftfrm = "Due".rjust(5)

		# Formatting for the final message thats outputted on the TinyBus
		busMes.append(bus[i].ljust(3)+" "+bus[i+1]+" "+timeleftfrm)

		j+=1
		i+=3

	i=0
	cycle=0
	# Outputs the messages onto the TinyBus
	while(cycle<maxRow):

		# Display if bus data is available
		if(bus[0]):
			clrscrn()

			lcd_byte(LCD_LINE_1, LCD_CMD)
			lcd_string(busMes[i])

			time.sleep(MAX_EXEC)

			# If there is a second bus to display,
			# then print its message and increment
			if(i+1<maxRow-1):
				lcd_byte(LCD_LINE_3, LCD_CMD)
				lcd_string(busMes[i+1])
				i+=2

			# Or if the second bus is the last bus in this set
			# then print it but reset the increment for new data
			elif(i+1==maxRow-1):
				lcd_byte(LCD_LINE_3, LCD_CMD)
				lcd_string(busMes[i+1])
				i=0

			# If none of the above occured (ie there was a first line but no second line)
			# then print the current date and time and reset the count to zero for new data
			else:
				dateTimeStamp = "  "+time.strftime("%d/%m/%Y")+" "+time.strftime("%H:%M")
				print ("TESTING DATETIMESTAMP>>")

				lcd_byte(LCD_LINE_3, LCD_CMD)
				lcd_string(dateTimeStamp)
				i=0

		# Print unavailable message if no data available
		else:
			lcd_byte(LCD_LINE_1, LCD_CMD)
			lcd_string("   No Realtime")
			lcd_byte(LCD_LINE_3, LCD_CMD)
			lcd_string("   Info Available.")

		time.sleep(7)
		cycle+=1


def clrscrn():
# Function to clear the screen
	lcd_byte(0x00,LCD_CMD)
	time.sleep(MAX_EXEC)

	lcd_byte(0x01,LCD_CMD)
	time.sleep(MAX_EXEC)



def lcd_init():
	
	print("Starting Init...")
	time.sleep(0.002) # Wait for power stabilisation
	
	print("Configuring bit-modes...")
	lcd_byte(0x02,LCD_CMD) # Set to 4Bit Mode
	time.sleep(MAX_EXEC)
	lcd_byte(0x02,LCD_CMD) # Return to home
	time.sleep(MAX_EXEC)
	lcd_byte(0x08,LCD_CMD) # Sets font to '00' english
	time.sleep(MAX_EXEC)
	
	lcd_byte(0x00,LCD_CMD) #  
	time.sleep(MAX_EXEC)
	lcd_byte(0x08,LCD_CMD) #  
	time.sleep(MAX_EXEC)

	lcd_byte(0x00,LCD_CMD) #  
	time.sleep(MAX_EXEC)
	lcd_byte(0x01,LCD_CMD) #  
	time.sleep(MAX_EXEC)

	lcd_byte(0x00,LCD_CMD) #  
	time.sleep(MAX_EXEC)
	lcd_byte(0x06,LCD_CMD) # Sets write mode 
	time.sleep(MAX_EXEC)

	lcd_byte(0x00,LCD_CMD) #  
	time.sleep(MAX_EXEC)
	lcd_byte(0x02,LCD_CMD) #  
	time.sleep(MAX_EXEC)

	lcd_byte(0x00,LCD_CMD) #  
	time.sleep(MAX_EXEC)
	lcd_byte(0x0F,LCD_CMD) #  
	time.sleep(MAX_EXEC)

	#End Initialization
	print("Ending Init...")

def lcd_string(message):
	
	# Send string to display
	message = message.ljust(LCD_WIDTH," ")  

	for i in range(LCD_WIDTH):
		lcd_byte(ord(message[i]),LCD_CHR)

def lcd_byte(bits, mode):
	# Send byte to data pins
	# bits = data
	# mode = True  for character
	#        False for command

	GPIO.output(LCD_RS, mode) # RS

	# High bits
	GPIO.output(LCD_D4, False)
	GPIO.output(LCD_D5, False)
	GPIO.output(LCD_D6, False)
	GPIO.output(LCD_D7, False)
	if bits&0x10==0x10:
		GPIO.output(LCD_D4, True)
	if bits&0x20==0x20:
		GPIO.output(LCD_D5, True)
	if bits&0x40==0x40:
		GPIO.output(LCD_D6, True)
	if bits&0x80==0x80:
		GPIO.output(LCD_D7, True)

	# Toggle 'Enable' pin
	time.sleep(E_DELAY)    
	GPIO.output(LCD_E, True)  
	time.sleep(E_PULSE)
	GPIO.output(LCD_E, False)  
	time.sleep(E_DELAY)      

	# Low bits
	GPIO.output(LCD_D4, False)
	GPIO.output(LCD_D5, False)
	GPIO.output(LCD_D6, False)
	GPIO.output(LCD_D7, False)
	if bits&0x01==0x01:
		GPIO.output(LCD_D4, True)
	if bits&0x02==0x02:
		GPIO.output(LCD_D5, True)
	if bits&0x04==0x04:
		GPIO.output(LCD_D6, True)
	if bits&0x08==0x08:
		GPIO.output(LCD_D7, True)

	# Toggle 'Enable' pin
	time.sleep(E_DELAY)    
	GPIO.output(LCD_E, True)  
	time.sleep(E_PULSE)
	GPIO.output(LCD_E, False)  
	time.sleep(E_DELAY)   

if __name__ == '__main__':
	main()
