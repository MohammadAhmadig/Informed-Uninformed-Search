#///////////////////////////////////////////////////////////////
#\\\\\\\\\\\\\\\\\\\Written By : Mohammad Ahmadi\\\\\\\\\\\\\\\\
#///////////////////////////////////////////////////////////////
print "Enter 1 for BFS: "
print "Enter 2 for DFS: "
print "Enter 3 for IDS: "
print "Enter 4 for A*: "
algorithm =raw_input('')
global money
money=input("Enter Your Money: ")
moneychangers=[]
mymap=[]
numOfNode=0
flag=0
direction=""
myfile = open("map.txt","r+")

array=myfile.readline().split()
nrow=eval(array[0])
ncol=eval(array[1])
for i in range(nrow):
	mymap.append(myfile.readline())
myrow=mycol=0
counter=0
mini=10000
sumi=0
Addr_changers=[]
for i in range(nrow):
	print mymap[i]
	for j in range(ncol):
		if mymap[i][j]>='a' and mymap[i][j]<='z':
			counter+=1
			Addr_changers.append([i,j])
		elif mymap[i][j]=='*':
			myrow=i
			mycol=j		
			
for i in range(counter):
	array=myfile.readline().split()
	moneychangers.append([array[0],eval(array[1])])			

distance=[[1000 for i in range(ncol)] for i in range(nrow)]#///////for Astar heuristic

def Hx():#heuristic H(x)
	global mymap
	global distance
	global nrow
	global ncol
	global counter
	global sumi
	global mini
	global Addr_changers
	
	for i in range(nrow):
		for j in range(ncol):
			if(mymap[i][j]>='a' and mymap[i][j]<='z'):
				distance[i][j]=0
			elif(mymap[i][j]=="#"):
				distance[i][j]=1000
			else:
				for k in range(counter):
					sumi=pow(i-(Addr_changers[k][0]),2)+pow(j-(Addr_changers[k][1]),2)
					if(mini > sumi):
						mini = sumi
				distance[i][j]=mini
				mini=10000	

def Ids(x,y,Dir,depth):
	global mymap
	global numOfNode
	global direction
	global money
	global moneychangers
	global flag
	global goalDepth
	global visit
	
	visit[x][y]=1
	if(flag==2):
		return	
	if mymap[x][y]=='#':
		return
	
	numOfNode+=1
	direction=direction+Dir
	print direction
	
	print x , y
	print mymap[x][y]
	if mymap[x][y]>='a' and mymap[x][y]<='z':
		for i in range(len(moneychangers)):
			if mymap[x][y]==moneychangers[i][0]:
				mymap[x]=mymap[x][:y]+"."+mymap[x][y+1:]
				if(money >= moneychangers[i][1]):
					money-=moneychangers[i][1]
					break
				else:
					money=0
					flag=2
					return	
	
	print "depth",depth
	if(depth==goalDepth):#/////
		return
	
	if(flag==0):#/////////
		if(visit[x][y+1]==0):
			Ids(x,y+1,"R",depth+1)#R
		if(visit[x+1][y]==0):
			Ids(x+1,y,"D",depth+1)#D
		if(visit[x][y-1]==0):
			Ids(x,y-1,"L",depth+1)#L
		if(visit[x-1][y]==0):
			Ids(x-1,y,"U",depth+1)#U
		
	return	
	

def Dfs(x,y,Dir):
	global mymap
	global numOfNode
	global direction
	global money
	global moneychangers
	global flag
	
	if(flag==2):
		return	
	if mymap[x][y]=='#':
		return
	
	numOfNode+=1
	direction=direction+Dir
	print direction
	if(direction[-2:]=="RL"):
		flag=1
		mymap[x]=mymap[x][:y+1]+"#"+mymap[x][y+2:]
		print x , y
	if(direction[-2:]=="LR"):
		flag=0
		mymap[x]=mymap[x][:y-1]+"#"+mymap[x][y:]
	
	if(direction[-2:]=="DU"):
		mymap[x]=mymap[x+1][:y]+"#"+mymap[x+1][y+1:]		
	
	if(direction[-2:]=="UD"):
		mymap[x]=mymap[x-1][:y]+"#"+mymap[x-1][y+1:]	
	
	print x , y
	print mymap[x][y]
	if mymap[x][y]>='a' and mymap[x][y]<='z':
		for i in range(len(moneychangers)):
			if mymap[x][y]==moneychangers[i][0]:
				mymap[x]=mymap[x][:y]+"."+mymap[x][y+1:]#/////////
				if(money >= moneychangers[i][1]):
					money-=moneychangers[i][1]
					break
				else:
					money=0
					flag=2
					return
	if(direction[-1:]=="L"):
		flag=1			
	if(direction[-1:]=="R"):
		flag=0
	if(flag==1):
		Dfs(x,y-1,"L")#L
		Dfs(x+1,y,"D")#D
		Dfs(x,y+1,"R")#R
		Dfs(x-1,y,"U")#U	
			
	if(flag==0):
		Dfs(x,y+1,"R")#R
		Dfs(x+1,y,"D")#D
		Dfs(x,y-1,"L")#L
		Dfs(x-1,y,"U")#U
		
	return

def Astar(x,y,Dir,depth):
	global queue
	global visit
	global mymap
	global numOfNode
	global direction
	global money
	global moneychangers
	global flag	
	global distance
	global counter
	
	visit[x][y]=1
	if(flag==2):
		return
	
	numOfNode+=1
	direction=direction+Dir
	print direction
	
	print x , y
	print mymap[x][y]
	if mymap[x][y]>='a' and mymap[x][y]<='z':
		for i in range(len(moneychangers)):
			if mymap[x][y]==moneychangers[i][0]:
				mymap[x]=mymap[x][:y]+"."+mymap[x][y+1:]#////
				Addr_changers.remove([x,y])
				counter-=1
				Hx()
				if(money >= moneychangers[i][1]):
					money-=moneychangers[i][1]
					break
				else:
					money=0
					flag=2
					return
			
	if(flag==0):
		if(mymap[x][y+1]!="#" and visit[x][y+1]==0):		
			queue.append([x,y+1,"R",depth+1])
			visit[x][y+1]=1
		if(mymap[x+1][y]!="#" and visit[x+1][y]==0):	
			queue.append([x+1,y,"D",depth+1])
			visit[x+1][y]=1
		if(mymap[x][y-1]!="#" and visit[x][y-1]==0):	
			queue.append([x,y-1,"L",depth+1])
			visit[x][y-1]=1
		if(mymap[x-1][y]!="#" and visit[x-1][y]==0):	
			queue.append([x-1,y,"U",depth+1])
			visit[x-1][y]=1
	bestpoint=0
	mini2=10000
	for i in range(len(queue)):
		Fx = distance[queue[i][0]][queue[i][1]] + depth # F(x)=G(x) + H(x)
		if(mini2 > Fx):
			mini2 = Fx
			bestpoint=i

	if(len(queue)==0):
		flag=2
	else:
		xy=queue[bestpoint]
		queue.remove(xy)
		Astar(xy[0],xy[1],xy[2],xy[3])
		
	return	

queue=[]
visit=[[0 for i in range(ncol)] for i in range(nrow)]
def Bfs(x,y,Dir):
	global queue
	global visit
	global mymap
	global numOfNode
	global direction
	global money
	global moneychangers
	global flag	
	
	visit[x][y]=1
	if(flag==2):
		return
	
	numOfNode+=1
	direction=direction+Dir
	print direction
	
	print x , y
	print mymap[x][y]
	if mymap[x][y]>='a' and mymap[x][y]<='z':
		for i in range(len(moneychangers)):
			if mymap[x][y]==moneychangers[i][0]:
				if(money >= moneychangers[i][1]):
					money-=moneychangers[i][1]
					break
				else:
					money=0
					flag=2
					return
			
	if(flag==0):
		if(mymap[x][y+1]!="#" and visit[x][y+1]==0):		
			queue.append([x,y+1,"R"])
			visit[x][y+1]=1
		if(mymap[x+1][y]!="#" and visit[x+1][y]==0):	
			queue.append([x+1,y,"D"])
			visit[x+1][y]=1
		if(mymap[x][y-1]!="#" and visit[x][y-1]==0):	
			queue.append([x,y-1,"L"])
			visit[x][y-1]=1
		if(mymap[x-1][y]!="#" and visit[x-1][y]==0):	
			queue.append([x-1,y,"U"])
			visit[x-1][y]=1
			
	if(len(queue)==0):
		flag=2
	else:
		xy=queue[0]
		queue.remove(xy)
		Bfs(xy[0],xy[1],xy[2])
		
	return	


dollars=0
for i in range(len(moneychangers)):
	dollars+=moneychangers[i][1]
if(money>dollars):
	print "Not exist enough Dollar"
elif(algorithm=="1"):
	Bfs(myrow,mycol,"")
	print "\n\nNumber of Nodes: ",numOfNode
	print "Path: ",direction
elif(algorithm=="2"):
	Dfs(myrow,mycol,"")
	print "\n\nNumber of Nodes: ",numOfNode
	print "Path: ",direction
elif(algorithm=="3"):
	goalDepth=input("Enter Depth: ")
	Ids(myrow,mycol,"",0)
	print "\n\nThe Rest of Money: ",money
	print "Number of Nodes: ",numOfNode
	print "Path: ",direction
elif(algorithm=="4"):
	Hx()
	Astar(myrow,mycol,"",0)
	print "\n\nNumber of Nodes: ",numOfNode
	print "Path: ",direction
else:
	print "INVALID INPUT!!!!!!!!!"
	
	