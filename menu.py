import sys
import time
def showMenu():
    print ("\n######################## MENU #######################")
    print("1 - Escolher horários definidos")
    print ("2 - Escolher por intervalo de tempo")
    print("0 - Sair do programa")
    print ("#######################################################")


def isTimeFormat(input):
    try:
        time.strptime(input,'%H:%M')
        return True
    except ValueError:
        return False

def askInput(option):
    global userTimes                    #global para pegar a variabvel userTimes global
    if(option == "1"):    
        print("Entre com os horários desejados, no padrao hh:mm hh:mm hh:mm ...")
        userTimes = input("Horarios: ")
        print(userTimes)
    elif(option == "2"):
        print("Entre com o horários inicial desejado e o intervalo de tempo, no padrao hh:mm hh:mm")
        userTimes = input("Horario e intervalo de tempo: ")
        print(userTimes)
    elif(option == "0"):
        print("Saindo do programa...")
        sys.exit()
    else:
        print("Opcao invalida, tente novamente")
        option = input("Entre com a opção desejada: ")
        askInput(option)

    userTimesList = userTimes.split(" ")
    for userTimes in userTimesList:
        if(not isTimeFormat(userTimes)):
            print("Horario " + userTimes + " invalido. Tente novamente usando o formato HH:MM para cada horario")
            askInput(option)

            break

userTimes = "" #Criar variavel global de entrada do usuário
showMenu()
option = input("Entre com a opção desejada: ")
print("Opção " + option + " selecionada")
askInput(option)

print("Horarios salvos com sucesso")
file = open("horarios.txt", "w")
file.write(option +"\n")
########### bug ###########
#print(userTimes) # <-- something is happening that userTimes here is just receiving the last entered time
#for i in userTimes.split(' '):
#    file.write(i+'\n')
file.write(userTimes)
file.close()