serverList = []
serverConnectLastTime = []
failureStatus = []
logfile = open('./logfile.txt','r')


txtLine = logfile.readline()
while txtLine:
    line = txtLine.strip('\n').split(',')
    if not line[1] in serverList:
        serverList.append(line[1])
        serverConnectLastTime.append(line[0])
        failureStatus.append(1)

    index = serverList.index(line[1])
    if failureStatus[index] == 1:
        serverConnectLastTime[index] = line[0]

    if line[2] == '-':
        failureStatus[index] = 0
    else:
        if failureStatus[index] == 0:
            time = (int(line[0])  - int(serverConnectLastTime[index]))*1000 + int(line[2])
            print(serverList[index] + ',' + str(time))
        failureStatus[index] = 1;
    txtLine = logfile.readline()
logfile.close()
