N = 5

serverList = []
serverConnectLastTime = []
failureCount = []
logfile = open('./logfile.txt','r')


txtLine = logfile.readline()
while txtLine:
    line = txtLine.strip('\n').split(',')
    if not line[1] in serverList:
        serverList.append(line[1])
        serverConnectLastTime.append(line[0])
        failureCount.append(N)

    index = serverList.index(line[1])
    if failureCount[index] == N:
        serverConnectLastTime[index] = line[0]

    if line[2] == '-':
        failureCount[index] -= 1
    else:
        if failureCount[index] <= 0:
            time = (int(line[0])  - int(serverConnectLastTime[index]))*1000 + int(line[2])
            print(serverList[index] + ',' + str(time))
        failureCount[index] = N;
    txtLine = logfile.readline()
logfile.close()
