N = 5

serverList = []
serverConnectLastTime = []
serverFailureStatus = []
subnetList = []
subnetConnectLastTime = []
subnetFailureStatus = []
logfile = open('./logfile.txt','r')

def subnetNetworkCalc(address):
    ip = address.split('/')
    ipBits = ip[0].split('.')
    netAddressDex = int(ipBits[0])
    for i in range(1, 4):
        netAddressDex <<=8
        netAddressDex += int(ipBits[i])
    mask = pow(2,32) - pow(2,32-int(ip[1]))
    subnetAddressDex = netAddressDex & mask
    for i in range(4):
        ipBits[3-i] = str(subnetAddressDex%256)
        subnetAddressDex >>=8
    return '.'.join(ipBits) + '/' + ip[1]

txtLine = logfile.readline()
while txtLine:
    line = txtLine.strip('\n').split(',')
    subnetAddress = subnetNetworkCalc(line[1])
    if not line[1] in serverList:
        serverList.append(line[1])
        serverConnectLastTime.append(line[0])
        serverFailureStatus.append(N)
    if not subnetAddress in subnetList:
        subnetList.append(subnetAddress)
        subnetConnectLastTime.append(line[0])
        subnetFailureStatus.append(N)

    serverIndex = serverList.index(line[1])
    if serverFailureStatus[serverIndex] == N:
        serverConnectLastTime[serverIndex] = line[0]
    subnetIndex = subnetList.index(subnetAddress)
    if subnetFailureStatus[subnetIndex] == N:
        subnetConnectLastTime[subnetIndex] = line[0]

    if line[2] == '-':
        serverFailureStatus[serverIndex] -= 1
        subnetFailureStatus[subnetIndex] -= 1
    else:
        if serverFailureStatus[serverIndex] <= 0:
            time = (int(line[0])  - int(serverConnectLastTime[serverIndex]))*1000 + int(line[2])
            print('failure server : ' + serverList[serverIndex] + ',' + str(time))
        serverFailureStatus[serverIndex] = N;
        if subnetFailureStatus[subnetIndex] <= 0:
            time = (int(line[0])  - int(subnetConnectLastTime[subnetIndex]))*1000 + int(line[2])
            print('failure subnet : ' + subnetList[subnetIndex] + ',' + str(time))
        subnetFailureStatus[subnetIndex] = N;
    txtLine = logfile.readline()


logfile.close()