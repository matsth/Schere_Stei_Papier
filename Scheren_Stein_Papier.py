import random as rng
import numpy as np

#AI
#------------------------------------------------------------------
global aichoice
global aibehaviorlearning
global aibehavior

#AIinfos
#------------------------------------------------------------------
global userchoice
global lastwon
global moveused

#Rest
#------------------------------------------------------------------
aiWins = 0
playerWins = 0
draws = 0
lastwon = None
aibehavior = 0

#0 = Schere
#1 = Stein
#2 = Papier
numbertonamearr = ['Schere', 'Stein', 'Papier']

#Set up Fitst Array
#0 = Random()
#1 = Copycat()
#2 = Counterlose()
#3 = CounterCounterwin()
#4 = Countermosteplayed()
aibehaviorlearning = np.array([1, 30, 30, 30, 30, 30])

moveused = np.array([0, 0, 0])


#AI behavior
#------------------------------------------------------------------
#Random Choice of Counter
def Random():
    global aichoice
    aichoice = rng.randint(0,2)

#Copy the move of the Oponent
def Copycat():
    global aichoice
    global userchoice

    aichoice = userchoice

#Counter last move of oponent
def Winlast():
    global aichoice
    global userchoice

    match userchoice:
        case 0:
            aichoice = 1
        case 1:
            aichoice = 2
        case 2:
            aichoice = 0

#Counter the move that would lose aiganst the last enemy played move
def Counterlose():
    global aichoice
    global userchoice

    match userchoice:
        case 0:
            aichoice = 2
        case 1:
            aichoice = 0
        case 2:
            aichoice = 1

#Counter the Counter of what last won
def CounterCounterwin():
    global aichoice
    global aibehavior
    global lastwon
    
    if not(lastwon == None):
        match lastwon:
            case 0:
                aichoice = 2
            case 1:
                aichoice = 0
            case 2:
                aichoice = 1
        
    else:
        Random()
        aibehavior = 0

#Counter what your oponent plays most
def Countermosteplayed():
    global aichoice
    global moveused

    if(moveused[0] > moveused[1]):
        if(moveused[0] > moveused[2]):
            aichoice = 1
        else:
            aichoice = 0
    else:
        if(moveused[1] > moveused[2]):
            aichoice = 2
        else:
            aichoice = 0

#AI learning
#------------------------------------------------------------------
def AIlearning(modi):
    global aibehavior
    global aibehaviorlearning

    
    aibehaviorlearning[aibehavior] += modi

    if not(aibehaviorlearning[aibehavior] >= 1):
        aibehaviorlearning[aibehavior] = 1

    if(aibehaviorlearning[0] > 1):
        aibehaviorlearning[0] = 1

def ChooseAI():
    global aibehaviorlearning
    global aibehavior

    x = rng.randint(1, np.sum(aibehaviorlearning))

    if(x <= aibehaviorlearning[0]):
        Random()
        aibehavior = 0
    elif(x <= aibehaviorlearning[0] + aibehaviorlearning[1]):
        Copycat()
        aibehavior = 1
    elif(x <= aibehaviorlearning[0] + aibehaviorlearning[1] + aibehaviorlearning[2]):
        Winlast()
        aibehavior = 2
    elif(x <= aibehaviorlearning[0] + aibehaviorlearning[1] + aibehaviorlearning[2] + aibehaviorlearning[3]):
        Counterlose()
        aibehavior = 3
    elif(x <= aibehaviorlearning[0] + aibehaviorlearning[1] + aibehaviorlearning[2] + aibehaviorlearning[3] + aibehaviorlearning[4]):
        CounterCounterwin()
        aibehavior = 4
    else:
        Countermosteplayed()
        aibehavior = 5
        
#Game
#------------------------------------------------------------------
Random()
leave = 0
error = 0
result = None

print('Bitte wählen sie Schere, Stein oder Papier aus.\nMit X verlassen sie das Spiel.\n')
while (leave <= 0):
    #User Input
    userchoice = input()

    if(userchoice == 'X' or userchoice == 'x'):
        leave = 1
    elif(userchoice == 'Schere' or userchoice == '0'):
        userchoice = 0
    elif(userchoice == 'Stein' or userchoice == '1'):
        userchoice = 1
    elif(userchoice == 'Papier' or userchoice == '2'):
        userchoice = 2
    else:
        error = 1
        print('Ungültige eingabe!')

    #Actual Game
    if not(error >= 1):
        if(leave <=0):
            match aichoice:
                case 0:
                    match userchoice:
                        case 0:
                            result = 'Du wählst ' + numbertonamearr[userchoice] + ', KI wählt ' + numbertonamearr[aichoice] + ' unentschieden!' + str(aibehavior)
                            moveused[userchoice] += 1
                            draws += 1
                        case 1:
                            result = 'Du wählst ' + numbertonamearr[userchoice] + ', KI wählt ' + numbertonamearr[aichoice] + ' Du gewinnst!' + str(aibehavior)
                            moveused[userchoice] += 1
                            playerWins += 1
                            lastwon = userchoice
                            AIlearning(-1)
                        case 2:
                            result = 'Du wählst ' + numbertonamearr[userchoice] + ', KI wählt ' + numbertonamearr[aichoice] + ' KI gewinnst!' + str(aibehavior)
                            moveused[userchoice] += 1
                            aiWins += 1
                            lastwon = aichoice
                            AIlearning(1)
                case 1:
                    match userchoice:
                        case 0:
                            result = 'Du wählst ' + numbertonamearr[userchoice] + ', KI wählt ' + numbertonamearr[aichoice] + ' KI gewinnst!' + str(aibehavior)
                            moveused[userchoice] += 1
                            aiWins += 1
                            lastwon = aichoice
                            AIlearning(1)
                        case 1:
                            result = 'Du wählst ' + numbertonamearr[userchoice] + ', KI wählt ' + numbertonamearr[aichoice] + ' unentschieden!' + str(aibehavior)
                            moveused[userchoice] += 1
                            draws += 1
                        case 2:
                            result = 'Du wählst ' + numbertonamearr[userchoice] + ', KI wählt ' + numbertonamearr[aichoice] + ' Du gewinnst!' + str(aibehavior)
                            moveused[userchoice] += 1
                            playerWins += 1
                            lastwon = userchoice
                            AIlearning(-1)
                case 2:
                    match userchoice:
                        case 0:
                            result = 'Du wählst ' + numbertonamearr[userchoice] + ', KI wählt ' + numbertonamearr[aichoice] + ' Du gewinnst!' + str(aibehavior)
                            moveused[userchoice] += 1
                            playerWins += 1
                            lastwon = userchoice
                            AIlearning(-1)
                        case 1:
                            result = 'Du wählst ' + numbertonamearr[userchoice] + ', KI wählt ' + numbertonamearr[aichoice] + ' Ki gewinnst!' + str(aibehavior)
                            moveused[userchoice] += 1
                            aiWins += 1
                            lastwon = aichoice
                            AIlearning(1)
                        case 2:
                            result = 'Du wählst ' + numbertonamearr[userchoice] + ', KI wählt ' + numbertonamearr[aichoice] + ' unentschieden!' + str(aibehavior)
                            moveused[userchoice] += 1
                            draws += 1
                case other:
                    result = 'Error!'

            ChooseAI()
            
        else:
            result = 'Exit!\n' + 'KI wins: ' + str(aiWins) + '\nPlayer wins: ' + str(playerWins) + '\nDraws: ' + str(draws) + '\n' +  str(aibehaviorlearning) + '\n' +  str(moveused)

        print(result)
    else:
        error = 0
