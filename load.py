
def loadData(name, passwd, email):
    print("------Loading Data------")
    with open('www.csdn.net.sql', 'rb')as f:
        for line in f.readlines():
            try:
                line = line.decode('UTF-8').split("#")
            except:
                continue
            name.append(line[0].strip())
            passwd.append(line[1].strip())
            email.append(line[2].strip())
    with open('plaintxt_yahoo.txt', 'rb')as f:
        for line in f.readlines():
            try:
                line = line.decode('UTF-8').split(":")
            except:
                continue
            if(len((line)) == 3):
                name.append(line[1].strip())
                passwd.append(line[2].strip())
    print("------Load Over---------")

if __name__ == "__main__":
    name = []
    passwd = []
    email = []

    loadData(name, passwd, email)
