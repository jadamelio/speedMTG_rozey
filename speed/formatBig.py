import time
def blackBox(f):
  class TurnInfo:
    def __init__ (self, phase, step, turnNumber, activePlayer):
      self.phase = phase
      self.step = step
      self.turnNumber = turnNumber
      self.activePlayer = activePlayer

  class GameState:
    def __init__ (self, id, turnInfo):
      self.id = id
      self.turnInfo = turnInfo
  def getThing(lineFull,i0,iN, str, wall):
    

    line = lineFull[i0:iN]
    if str in line: xx = line[line.index(str)+len(str)+2:]
    else:
     #print("Couldn't find: ", str, " in ", line)
     #time.sleep(1)
     xx = getThing(lineFull, i0 - 90, iN + 90,str ,wall )

    a = xx[:xx.index(wall)]
   # print(type(a))

    if " " in a : b = a.replace(" ", "")#remove white space
    else: b = a
   # print(type(b))
    if "'" in b :c = b.replace("'", "")#remove apostrophe
    else: c = b
   # print(type(c))

    if "\"" in c :   d = c.replace("\"","")#remove qoutes
    else: d = c
    #print(type(d))

    return d
   


  #print("STARTOMG")
  gameStates = []
  #input = open("PlayerJackvArcher.log", "r")
  input = f
  #outie = open("archervsivertebrate.csv", 'w')
  #outie.write("State,globalTime,timerID,elapsedMs,phase,turnNumber,activePlayer,priorityPlayer, decisionPlayer, clockOwnership\n")
  lines = 0
  linesWithPrevious = 0
  indices = []
  gameStateId = "prevGameStateId"
  counter = 0
  toWrite = []
  aT = True
  bT = True
  cT = True
  dT= True
  eT = True
  fT = True
  escape = ""
  for line in input:
     #if len(toWrite) > 3: break 
    counter +=1
    timerSet1 =0
    '''
    lplpl = ''
    if "Match to " in line and aT:
     print(line)
     print(line[line.index("o"): line.index(":")])
     lplpl = line[line.index("o"): line.index(":")]
     aT = False

    
    if "Connecting to matchId" in line and bT: 
      print(line)
      bT=False

    if "systemSeatId" in line and "teamId" in line and fT:
      print(line.replace("{", "\n"))
      fT = False
    if "MulliganOption_AcceptHand" in line and cT: 
      print(line)
      cT=False
    if "ResultType_WinLoss" in line and dT:
     print(line)
     dT = False

    if "finalMatchResult" in line and eT:
      print(line)
      eT= False
    '''
    try:
     startString1 = line[line.index("teamId"):]
     #print("  VV" +startString1)
     timerSet1 = getThing(startString1,"timerIds\": ): ", ",")
    except:
     xlx = 0

      #print("Meee  ", timerSet1)
     if "ResultType_WinLoss" in line: 
      #print("MATCH EXIT FOUND")
      #print(line[:100])
      escape = "BREAK"
     
     # break
     gameStates = []
     if "gameStateId" in line:
     # print("-----------")
     # print(line,"AAA")
      for i in range(len(line)):
        sli = line[i:i+len("gameStateId")]
        shift = 0
        if sli == "gameStateId":
          aaa = line[i+len("gameStateId")+3:i+len("gameStateId")+10]
         # print(aaa)
          try:
            bbb = aaa[:aaa.index(",")]#ID
          except:
            try:
             bbb = aaa[:aaa.index("}")]#ID#turn ID
            except:
             try:
              bbb = aaa#ID#turn 
             except:
              print(aaa[:30], "wwww")
          #print(line, "line")
          #print (aaa, "AA")
          #print(bbb, "BB")
          bbb = bbb.replace(" ", "").replace("}","")
          if int(bbb) == 5 or int(bbb)== 6or int(bbb)== 7:break

          
          ccc = line[i+shift:i+len("\"gameStateId")+shift+35]
          if "turnInfo" in ccc:
            #print("NEW OBJECT", bbb)
            #print("FILE LINE: " + str(counter))
            newState = GameState(int(bbb),[])
            
            #print(line[i:i+len("gameStateId")+40]+"\n")
            ddd = line[i:]
            eee = ddd
            #print("### "+eee)
            repeat = False
            for k in range(len(gameStates)):
              if gameStates[k].id == newState.id:
                repeat = True
                #print("   Repeated")

            if repeat is False: 
              newState.turnInfo = [eee]
              gameStates.append(newState)
       
        xxx = 0


     if "\"type\": \"TimerType_MatchClock\"" in line:
       if gameStateId in line:
         #print(line, "\n")
         #print("FILE LINE: " + str(counter))
         for i in range(len(line)):
          sli = line[i:i+len("TimerType_MatchClock")]
          
          if sli == "TimerType_MatchClock": 
            #print(sli)
            #print("\n        " +line[i:i+len("TimerType_MatchClock")+190])
            aaa = line[i:i+len("TimerType_MatchClock")+290]#TIMER STUFF
            for j in range(i):
              sli2 = line[i-len("\"gameStateId")-j:i-j]
              if sli2 == "\"gameStateId": 
               #print("\n        " +sli2)
               bbb = line[i-len("gameStateId")-j:i-j+10]
               try:
                iDD = int(bbb[13:bbb.index(",")])
               except:
                iDD = int(bbb[13:bbb.index("}")])


               found = False
               for k in range(len(gameStates)):
                if gameStates[k].id == iDD: 
                  found = True

                  #print("      Timer found for state:         " + str(iDD) +" || " + aaa[:80])
                  #print("         FOUND ---  " + str(gameStates[k].turnInfo))

                  
                  #print(getThing(str(gameStates[k].turnInfo[0]), "decisionPlayer", ","))
                  toWrite.append(str(iDD) +"," + 
                    getThing(line,i-40,i, "timerId", ",")+","   + getThing(line,i,i+len("TimerType_MatchClock")+290, "elapsedMs", "}")+","  
                     
                       + getThing(str(gameStates[k].turnInfo[0]),0,len(str(gameStates[k].turnInfo[0]))-1,"turnNumber", ",") + ","   
                       + getThing(str(gameStates[k].turnInfo[0]),0,len(str(gameStates[k].turnInfo[0]))-1,"activePlayer", ",")  + ","  
                        + getThing(str(gameStates[k].turnInfo[0]),0, len(str(gameStates[k].turnInfo[0]))-1,"priorityPlayer", ",") +","
                        +"]")
                  break
               #if found == False: print("         xNo State Found")
              #break
               
         prevIndex = line.index(gameStateId) + 18
         id = ""
         while (line[prevIndex] != ","):
           
           prevIndex += 1
           #print(line[prevIndex])
         # Check if there's a GameState object that's created already with the correct id.
         # Maybe index the TurnInfo objects by the game state id instead of creating a GameState
         # object that contains TurnInfo.
         indices.append(id)
         linesWithPrevious += 1
       lines += 1

  #print(indices)
  #print(linesWithPrevious)
  #print(lines)
  #print(len(gameStates))
  toPrint = []
  for i in range(len(toWrite)-1):
    l = toWrite[i]
    #print(l)
    #print(toWrite[i+1])
    #print("-----------------")
   
    toSearch =toWrite[i+1:]
    foundDupe = False
    for j in range(len(toPrint)):
      if l == toPrint[j]: 
       #print('Dupe----------------------------------xxxxxxxxxxxOOOOOOOOOOO')
       foundDupe = True
    if foundDupe == False:toPrint.append(l)

  #print(len(toWrite))
  #print(len(toPrint))
  #print("linesRead  " + str(len(toPrint)))


  entries = []
  for i in range(len(toPrint)):
    entries.append(toPrint[i].split(","))

  #for i in range(len(toPrint)):
    #print(toPrint[i] + "\n")
    #outie.write(toPrint[i] + "\n")
  #print(len(entries), "AA")
  if escape == "BREAK":
   #print  ([escape] + entries)
   #return [escape] + entries
   return entries
  else:
   return entries

#blackBox(open("C:\\Users\\i\\AppData\\LocalLow\\Wizards Of The Coast\\MTGA\\Player.log", "r"))