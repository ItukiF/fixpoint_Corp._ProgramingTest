N = 5
m = 5
t = 100

serverList = []
serverConnectLastTime = []
failureCount = []
responseBuffer = []
oldestBuffer = []
overloadStatus = []
overloadTime = []
logfile = open('./logfile.txt','r')


txtLine = logfile.readline()
while txtLine:
    line = txtLine.strip('\n').split(',')
    if not line[1] in serverList:
        serverList.append(line[1])
        serverConnectLastTime.append(line[0])
        failureCount.append(N)
        responseBuffer.append([-1]*m)
        oldestBuffer.append(0)
        overloadStatus.append(0)
        overloadTime.append(line[0])

    if line[2] == '-':
        index = serverList.index(line[1])
        failureCount[index] -= 1
    else:
        index = serverList.index(line[1])
        if failureCount[index] <= 0:
            time = (int(line[0])  - int(serverConnectLastTime[index]))*1000 + int(line[2])
            print('failure server : ' + serverList[index] + ',' + str(time))
        serverConnectLastTime[index] = line[0]
        failureCount[index] = N;

    if not line[2] == '-':
        responseBuffer[index][oldestBuffer[index]] = int(line[0])*1000 + int(line[2])
        oldestBuffer[index] = (oldestBuffer[index] + 1) % m
    if not -1 in responseBuffer[index]:
        averageTime = 0
        for i in range(m):
            averageTime += responseBuffer[index][i]%1000
        averageTime /= m
        if averageTime > t:
            if overloadStatus[index] == 0:
                overloadTime[index] = line[0]
                overloadStatus[index] = 1
        elif overloadStatus[index] == 1:
            print('overload condition : ' + line[1] + ',' + overloadTime[index] + '~' + line[0])
            overloadStatus[index] = 0

    txtLine = logfile.readline()

for i in range(len(serverList)):
    if overloadStatus[i] == 1:
        print('overload condition : ' + line[1] + ',' + overloadTime[i] + '~' + serverConnectLastTime[i])
logfile.close()