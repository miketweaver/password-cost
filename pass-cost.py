#!/usr/bin/env python
from appJar import gui
import getpass
import argparse

# Flags/Arguments
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--show-pass', action="store_true",help='prints the typed password')
parser.add_argument('--hash', help='set the hash type. SHA1, MD5, or BCRYPT  (default: %(default)s)', type=str, default="SHA1")
parser.add_argument('--gui', action="store_true",help='use GUI interface')
args = parser.parse_args()

### Variables ###
google = .7
amazon = .9

### Speed variables ###
#SHA1 in MH/s
gtx1070SHA1		= 6401.6
gtx970SHA1		= 3830.8
dadSHA1			= 1856.4
cloudSHA1		= 1979.0375

#MD5 in MH/s
gtx1070MD5		= 17907.6
gtx970MD5		= 9526.5
dadMD5			= 1
cloudMD5		= 4580.40625

#BCRYPT in MH/s
gtx1070BCRYPT		= .009676
gtx970BCRYPT		= .006301
dadBCRYPT		= 1
cloudBCRYPT		= .002121

units = 1000000 #MH/s

# Humanize Function
def humanize_time(secs):
    mins, secs = divmod(secs, 60)
    hours, mins = divmod(mins, 60)
    return '%02d hr %02d min %02d sec' % (hours, mins, secs)

def get_charset(string):
	count = 0
	if any(c.islower() for c in string):
	 count += 26
	if any(c.isupper() for c in string):
	 count += 26
	if any(c.isdigit() for c in string):
	 count += 10
	if any(c == "#" or c == "!" or c == "@" or c == "$" for c in string):
	 count += 4
	return count

def get_hashcount(count,length):
	return pow(count,length)

def get_time2crack(hashes,speed):
	return hashes/(speed*units)

def get_cost(time,price):
	return (time/60/60)*price

def get_speed(device,type):
	if device == "GTX970":
		switcher = {
		'SHA1': gtx970SHA1,
		'MD5': gtx970MD5,
		'BCRYPT': gtx970BCRYPT
		}
	if device == "GTX1070":
		switcher = {
		'SHA1': gtx1070SHA1,
		'MD5': gtx1070MD5,
		'BCRYPT': gtx1070BCRYPT
		}
	if device == "DAD":
		switcher = {
		'SHA1': dadSHA1,
		'MD5': dadMD5,
		'BCRYPT': dadBCRYPT
		}
	if device == "CLOUD":
		switcher = {
		'SHA1': cloudSHA1,
		'MD5': cloudMD5,
		'BCRYPT': cloudBCRYPT
		}
	return switcher.get(type, 0)

################ GUI ################
if args.gui:
	# function called by pressing the buttons
	def press(btn):
		if btn=="Quit":
			app.stop()
		elif app.getEntry('pass') is '':
			app.errorBox("Empty Pass", "Please enter a password.")
		else:
			var = app.getEntry('pass')
			hashtype = app.getOptionBox("HashType")
			length = len(var)
			charcount = get_charset(var)
			hashes = get_hashcount(charcount,length)
			cloudtime= get_time2crack(hashes,get_speed("CLOUD",hashtype))

			text =	"# of Chars: " + str(length)
			text +=	"\n# of Charset: " + str(charcount)
			text +=	"\n# of Hashes: " + str(hashes)
			text +=	"\n# of Hashes: " + str(hashes)
			text +=	"\nHash Type: " + hashtype
			text +=	"\nTime to solve (dad): " + humanize_time(get_time2crack(hashes,get_speed("DAD",hashtype)))
			text +=	"\nTime to solve (gtx 970): " + humanize_time(get_time2crack(hashes,get_speed("GTX970",hashtype)))
			text +=	"\nTime to solve (gtx 1070): " + humanize_time(get_time2crack(hashes,get_speed("GTX1070",hashtype)))
			text +=	"\nCost, Amazon: ${:,.2f}".format(get_cost(cloudtime,amazon))
			text += "\nCost, Google: ${:,.2f}".format(get_cost(cloudtime,google))
			app.clearTextArea("Results")
			app.setTextArea("Results", text)

	app = gui()
	app=gui("PassCalc", "400x325")

	app.addLabel("title", "Calculate your password", 0, 0, 2)  # Row 0,Column 0,Span 2
	app.addLabel("by", "by Mike Weaver", 2, 0, 2)  # Row 0,Column 0,Span 2
	app.addLabel("pass", "Password:", 3, 0)              # Row 2,Column 0
	app.addSecretEntry("pass", 3, 1)                     # Row 2,Column 1
	app.addLabel("hashText", "Hash Type:", 4, 0)  # Row 0,Column 0,Span 2
	app.addOptionBox("HashType", ["SHA1", "MD5", "BCRYPT"], 4, 1)
	app.addHorizontalSeparator(5,0,2)
	app.addTextArea("Results", 6,0,2)
	app.addHorizontalSeparator(7,0,2)
	app.addButtons(["Caluclate", "Quit"], press, 8, 0, 2) # Row 3,Column 0,Span 2

	app.setEntryFocus("pass")

	app.go()

############## CMD Line ##############
else:
	var = getpass.getpass()

	if args.show_pass:
	 print "Your password is:", var 

	length = len(var)
	charcount = get_charset(var)
	hashes = get_hashcount(charcount,length)
	cloudtime= get_time2crack(hashes,get_speed("CLOUD",args.hash))

	print "# of Chars:", length
	print "# of Charset:", charcount
	print "# of Hashes:", hashes
	print "Hash Type:", args.hash
	print "Time to solve (dad):", humanize_time(get_time2crack(hashes,get_speed("DAD",args.hash)))
	print "Time to solve (gtx 970):", humanize_time(get_time2crack(hashes,get_speed("GTX970",args.hash)))
	print "Time to solve (gtx 1070):", humanize_time(get_time2crack(hashes,get_speed("GTX1070",args.hash)))
	print "Cost, Amazon: ${:,.2f}".format(get_cost(cloudtime,amazon))
	print "Cost, Google: ${:,.2f}".format(get_cost(cloudtime,google))
