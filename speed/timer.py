import time
import logging
import os
import threading
import formatBig
from math import floor, ceil
from tkinter import *
import win32gui
import win32api
from win32api import GetSystemMetrics
import os


#per Priority?
#5+20 per game

global_incrementMs = 20*1000
global_bankMs = 5*60*1000

global_kill = False
global_arenaPath = "MTGA.lnk"
global_logPath = "C:\\Users\\Brennen\\AppData\\LocalLow\\Wizards Of The Coast\\MTGA\\Player.log"

global_timer7LastRead = -1
global_timer14LastRead = -1
global_player7Clock = 0
global_player14Clock = 0
global_lastSet7 = [0,0,0,0,0,0,0,]
global_lastSet14 = [0,0,0,0,0,0,0]

global_gameStartTime = -1
global_turnNumber = 0

global_lastKnowPriority = 1


global_gameCounter = 0
global_gameTimes = []

global_userSeat = -1
global_opponentSeat = -1



def tinker2():#this is taken from a github, I just threw it in and added the config line to the while loop


	global global_player14Clock
	global global_player14Clock
	global text
	global global_lastKnowPriority
	global global_kill
	global global_incrementMs
	global global_bankMs
	global global_gameTimes
	# WIDTH = 500
	# HEIGHT = 500

	WIDTH = GetSystemMetrics(0)
	HEIGHT = GetSystemMetrics(1)
	LINEWIDTH = 1
	TRANSCOLOUR = 'gray'
	title = 'Virtual whiteboard'
	global old
	old = ()
	global HWND_t
	HWND_t = 0

	tk = Tk()
	# tk.title(title)
	tk.lift()
	tk.wm_attributes("-topmost", True)
	tk.wm_attributes("-transparentcolor", TRANSCOLOUR)
	tk.attributes('-fullscreen', True)


	state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128

	canvas = Canvas(tk, width=WIDTH, height=HEIGHT, highlightthickness=0)
	canvas.pack()
	canvas.config(cursor='tcross')
	canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill=TRANSCOLOUR, outline=TRANSCOLOUR)
	userBox =canvas.create_text(int(floor(WIDTH/4)),int(floor(HEIGHT/2 +HEIGHT/16)),fill="white",font="Arial 20", text="TEXT GOES HERE")
	oppnentBox =canvas.create_text(int(floor(WIDTH/4)),int(floor(HEIGHT/2 -HEIGHT/16)),fill="white",font="Arial 20", text="TEXT GOES HERE")

	def putOnTop(event):
		event.widget.unbind('<Visibility>')
		event.widget.update()
		event.widget.lift()
		event.widget.bind('<Visibility>', putOnTop)
	def drawline(data):
		global old
		if old !=():
			canvas.create_line(old[0], old[1], data[0], data[1], width=LINEWIDTH)
		old = (data[0], data[1])

	def enumHandler(hwnd, lParam):
		global HWND_t
		if win32gui.IsWindowVisible(hwnd):
			if title in win32gui.GetWindowText(hwnd):
				HWND_t = hwnd

	win32gui.EnumWindows(enumHandler, None)

	tk.bind('<Visibility>', putOnTop)
	tk.focus()

	userClock = global_player7Clock
	userFunction = floor
	userIt = 0
	opponentClock = global_player14Clock
	oppFunction = ceil
	oppIt = 1
	if global_userSeat == 2:
		userClock = global_player14Clock
		userFunction = ceil
		userIt = 1
		opponentClock = global_player7Clock
		oppFunction = floor
		oppIt = 0


	running = 1
	i = 1
	while running == 1:
		#if global_kill == True:
			#print("Exiting Overlay " + str(seatNumber) )
			#break
		i += 1
		userClock = global_player7Clock
		opponentClock = global_player14Clock
		
		if int(global_userSeat) == 2:
			userClock = global_player14Clock
			opponentClock = global_player7Clock

		#Arena Clock
		userToSendSec = floor(60- (userClock/1000)%60)
		userToSendMin = floor(30-(userClock-(userClock/1000)%60)/1000 *(1/60))

		opponentToSendSec = floor(60- (opponentClock/1000)%60)
		opponentToSendMin = floor(30-(opponentClock-(opponentClock/1000)%60)/1000 *(1/60))

		#Fischer Clock


		
		userIncrementsPast = int(userFunction(global_turnNumber/2)-1)
		
		#Seconds elapased: 
		gameOffset = 0
		for i in range(len(global_gameTimes)):
			gameOffset += global_gameTimes[i][userIt]
		userFischerClock = userClock -(global_incrementMs*userIncrementsPast) - gameOffset
		
		#print(userFischerTotal)
		uFseconds = floor(60-(userFischerClock/1000)%60)
		uFminutes = floor(5-(userFischerClock-(userFischerClock/1000)%60)/1000*(1/60))






		
		opponentIncrementsPast = int(oppFunction(global_turnNumber/2)-1)
		
		#Seconds elapased: 

		gameOffset = 0
		for i in range(len(global_gameTimes)):
			gameOffset += global_gameTimes[i][oppIt]
		opponentFischerClock = opponentClock -(global_incrementMs*opponentIncrementsPast)- gameOffset
		
		#print(opponentFischerTotal)
		oFseconds = floor(60-(opponentFischerClock/1000)%60)
		oFminutes = floor(5-(opponentFischerClock-(opponentFischerClock/1000)%60)/1000*(1/60))






		


		userText = str(userToSendMin)+ ":"+str(userToSendSec) + " | " + str(uFminutes) +":"+str(uFseconds) + "   |PRESS FOR MOX| fucky:" + str(global_turnNumber)
		oppText = str(opponentToSendMin)+ ":"+str(opponentToSendSec)+ " | " + str(oFminutes) +":"+str(oFseconds)
		#print(userText)
		#print(oppText)
		if global_lastKnowPriority == global_userSeat:
			canvas.itemconfig(userBox, text = userText, fill='green',font="Arial 25")
			canvas.itemconfig(oppnentBox, text = oppText, fill='white',font="Arial 15")
		else:
			canvas.itemconfig(oppnentBox, text = oppText, fill='green',font="Arial 25")
			canvas.itemconfig(userBox, text = userText, fill='white',font="Arial 15")

		
		
		try:
			tk.update()
			time.sleep(0.1)
			if HWND_t != 0:
				windowborder = win32gui.GetWindowRect(HWND_t)
				cur_pos = win32api.GetCursorPos()
				state_left_new = win32api.GetKeyState(0x01)
				if state_left_new != state_left:
					if windowborder[0] < cur_pos[0] and windowborder[2] > cur_pos[0] and windowborder[1] < cur_pos[1] and windowborder[3] > cur_pos[1]:
						drawline((cur_pos[0] - windowborder[0] - 5, cur_pos[1] - windowborder[1] - 30))
				else:
					old = ()
		except Exception as e:
			running = 0
			print("error %r" % (e))







def readFile(i):
	def getMostRecentTimer(entries):
		
		index = 0
		for i in range(len(entries)):
			if int(entries[i][3]) > int(entries[index][3]):
				index = i

		return entries[index]
	def getMostRecentState(entries):
		
		index = 0
		for i in range(len(entries)):
			if int(entries[i][0]) > int(entries[index][0]):
				index = i

		return entries[index]

#----------------------------------------------------------------------------------------------

	
	

	demo = open("demoFile.csv", 'w')
	
	global global_lastKnowPriority
	
	global global_player7Clock
	global global_player14Clock
	global global_kill

	global global_turnNumber
	global global_gameStartTime

	file = open(global_logPath, "r")
	mostRecent7 = [0,0,0,0,0,0,0,0,0,0,0]
	mostRecent14 = [0,0,0,0,0,0,0,0,0,0,0]
	llR = ""
	old = [0,0,0,0]
	things7hasBeenSetToo = []
	things14hasBeenSetToo = []	
	selfMadeTimeStamp = -1
	#REQUIRES LOGIC TO ASSIGN SEAT NUMBER TO TIMER
	theNewAge = time.time()
	
	#ewThread2 = threading.Thread(target=tinker,args=(-1,2))
	#ewThread2.start()

	while True:
		#readNewestlines(file)
		lines = formatBig.blackBox(file)
		
		
		novelData = ""#will contain new lines
		if len(lines) != 0 and lines[0] == "BREAK": 
			#global_kill =True
			print("Game exit")
			#return 0
		selfMadeTimeStamp = time.time()*1000
		#print(selfMadeTimeStamp, "aaaa")
		if 0 < len(lines): #if there is new lines
			
			
			novelData = list(lines)#Array Format (Ithink): outie.write("State,globalTime,timerID,elapsedMs,phase,turnNumber,activePlayer,priorityPlayer, decisionPlayer, clockOwnership\n")
			#selfMadeTimeStamp = time.time()*1000
				
		
			#Sort the timer readings into 7 and 14
			#Find biggest state for each timer
			options7 = [0]
			options14 = [0]
			biggestState7index = 0
			biggestState14index = 0
			#Error likely in the finding of the timer
			
			zeSevens = []
			zeFourteens = []
			#print(things7hasBeen)
			#print(things14hasBeen)
			
			demo.write("-----------------------------------------------" + " \n")
			for i in range( len(novelData)):#This bit just sorts shit by timer
				#print(novelData[i])
				novelData[i] = [selfMadeTimeStamp] + novelData[i]

				#print(novelData[i])
				#demo.write(str(novelData[i]) + " \n")


				if '7' in novelData[i][2]:#Check for duplicates
					zeSevens.append(novelData[i])

				if '14' in novelData[i][2]:#Check for duplicates
					zeFourteens.append(novelData[i])

			
			if len(zeSevens) != 0: mostRecent7 = getMostRecentTimer(zeSevens)
			if len(zeFourteens) != 0: mostRecent14 = getMostRecentTimer(zeFourteens)
				#What happens if there is no 7 or no 14
				#[State,globalTime,timerID,elapsedMs,phase,turnNumber,activePlayer,priorityPlayer, decisionPlayer, clockOwnership]
			if mostRecent7[3] not in things7hasBeenSetToo: 
				things7hasBeenSetToo.append(mostRecent7[3])
				global_player7Clock = int(mostRecent7[3])
				



			if mostRecent14[3] not in things7hasBeenSetToo: 
				things14hasBeenSetToo.append(mostRecent14[3])
				global_player14Clock = int(mostRecent14[3])

			if global_gameStartTime == -1: #Single time sets reference for starting time
				#print(global_player14Clock, global_player7Clock)
				print("Timer Set")
				global_gameStartTime = int(1000*time.time()) - int(global_player14Clock) - int(global_player7Clock)
			#only reset if timer is bigger, smaller by a margin 
				#print(global_gameStartTime)
			
			#print(selfMadeTimeStamp, ",",(selfMadeTimeStamp- global_gameStartTime)/1000, (global_player14Clock + global_player7Clock)/1000)
			#print("from set ", selfMadeTimeStamp, ",",((selfMadeTimeStamp- global_gameStartTime)/1000)- (global_player14Clock + global_player7Clock)/1000)
			#Update Turn
			mRS = getMostRecentTimer(novelData)#getMostRecentState(novelData)	
			#print(mRS)
			global_lastKnowPriority = str(mRS[-2])
			if int(mRS[4]) > global_turnNumber: 
				global_turnNumber = int(mRS[4])
				print("New turn #", global_turnNumber)
			
			
			

		else: #If there are no new lines
			#print(global_lastKnowPriority, type(global_lastKnowPriority), global_lastKnowPriority == '1')
			if "1" in str(global_lastKnowPriority):
				#print("toggle")
				global_player7Clock += abs((time.time() - theNewAge))*1000 #Adjust timer by time since last adjustment
				theNewAge = time.time()
			else:
				#print("doggle")
				global_player14Clock += abs((time.time() - theNewAge))*1000#Adjust timer by time since last adjustment
				theNewAge = time.time()
			#selfMadeTimeStamp = abs(time.time() - theNewAge)*1000

		#Formats to minutes and seconds
		toSendSec7 = (global_player7Clock/1000)%60
		toSendMin7 = (global_player7Clock-toSendSec7)/1000 *(1/60)
		toSendSec14 = (global_player14Clock/1000)%60
		toSendMin14 = (global_player14Clock-toSendSec14)/1000 *(1/60)
			
		new = [floor(toSendMin7), floor(toSendSec7), floor(toSendMin14), floor(toSendSec14)]
		if new != old:#From when timer was getting frozen

			#print("7, ",floor(30-toSendMin7), ",",floor(60-toSendSec7),"   14, ",floor(30-toSendMin14), ",",floor(60-toSendSec14))
			#print(((1000*time.time()- global_gameStartTime)/1000)-((global_player14Clock + global_player7Clock)/1000))
			#print("passive ",selfMadeTimeStamp, ",",((selfMadeTimeStamp- global_gameStartTime)/1000)- (global_player14Clock + global_player7Clock)/1000)
			
			old = new
			#demo.write(str(selfMadeTimeStamp) +",7, " +str(global_player7Clock)+ "," + "   14, " +str(global_player14Clock) +", " + str(llR)+"\n")
				
		#time.sleep(.25)#Does ordering matter?
		

		
def overMethod():
	global global_userSeat
	global global_opponentSeat

	global global_gameStartTime
	global global_gameCounter
	global global_gameTimes
	#who is which player Match to CDE9150074F3C626


	#When does a match start ?? Connecting to matchId

	#who has which seat userId": "CDE9150074F3C626", "playerName": "IVertebrate#88688", "systemSeatId": 2, "teamId": 2,

	#When does a game start ??  "decision": "MulliganOption_AcceptHand"
	#WHen does a game end ?? "ResultType_WinLoss"
	#when does a match emd ?? "finalMatchResult"

	file = open(global_logPath, "r")
	userID = False
	#Search for user ID
	print("Searching for ID")
	while userID == False:
		for line in file:
			if "Match to " in line:
				#print(line)
				userID = line[line.index("Match to ")+len("Match to "):line.rindex(":")]
				print("ID found: " ,userID, "Waiting for match")
				break
	
	#Listen for Match
	
	matchRunning = False
	while matchRunning == False:
		for line in file:
			if "Connecting to matchId" in line:
				matchRunning =True
				break
	print("Match found, assinging seats")
	#Find Seats
	#Assign seat numbers
	while global_userSeat == -1:
		for line in file:
			if userID in line and "systemSeatId" in line:
				uIDindex = line.index(userID)+len(userID)
				seatIDindex = uIDindex + line[uIDindex:].index("systemSeatId")+len("systemSeatId")+3
				#print(uIDindex, seatIDindex)
				#print(line[uIDindex:seatIDindex], "<----------------")
				if "}" not in line[uIDindex:seatIDindex]:
					global_userSeat = line[int(seatIDindex)]
					#print(line , len(line))
					break
				else: print("whuho")
	print("Seats assigned-- user: ", global_userSeat)
	global_opponentSeat == 1
	if global_userSeat == 1: global_opponentSeat = 2

	




	print("waiting for game")
	global_gameCounter = 1
	totalLinesRead = 0
	leftOffat = -1
	#totalLinesRead > leftOffat and
	ewThread1 = threading.Thread(target=tinker2,args=())
	ewThread1.start()
	while True:
		#listen for game start
		
		
		gameRunning = False
		while gameRunning == False:
			for line in file:
				totalLinesRead += 1
				
				if "MulliganOption_AcceptHand" in line and gameRunning == False and len(line) < 500:
					
					gameRunning = True
					global_gameCounter += 1
					
					print("Game on, game # ", global_gameCounter)
					readFile(0)#Makes everything happen with clocks, Exits on game complete
					gameRunning = False
					global_gameTimes.append([global_player7Clock, global_player14Clock])
					leftOffat = totalLinesRead
					totalLinesRead = 0
				
			#time.sleep(3)
				if "finalMatchResult" in line:
					print("match complete")
					#return global_gameCounter
				
def main():
	referTime = time.time()

	i = 0
	
	global global_kill
	global global_arenaPath
	global global_logPath
	#try:
	#os.remove(global_logPath)
	#except:
		#print("Didnt find a log, lets see what happen")
	print("----")
	#print(os.listdir("\\"))
	#os.startfile(global_arenaPath)
	#time.sleep(10)
	#ewThread = threading.Thread(target=readFile,args=(0,))
	#ewThread.start()
	a =overMethod()
	'''
	timePrev = referTime
	timer = 0
	while i <10000:
		i+=1
		time.sleep(5)
		newTime = (time.time())
		elapsed = newTime-timePrev
		timer = timer + elapsed
		#print("Global timer " + str(timer))
		
		timePrev = newTime
		#if global_kill == True:
			#print("Exiting Main")
			#break
	'''
		
		
		
		


		
		

main()
