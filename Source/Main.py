import sys
from Queue import PriorityQueue
# open and read from input file
lines=[]
with open(sys.argv[1]) as f:
    lines.extend(f.read().splitlines())

searchType=lines[0];
fuel=lines[1];
source=lines[2];
destination=lines[3];

#create a new file to write the output
fo= open("output.txt", "wb")
input=lines[4:];
generatedGraph={};
for line in input:
	adj_list=line.split(':');
	node=adj_list[0];
	neighbours=adj_list[1].split(',');
	neighbour_list=[];
	neighbour_map = {};
	for neighbour in neighbours:
		keyvalue=neighbour.split('-');
		neighbour_list.append(neighbour.strip());
		neighbour_map[keyvalue[0].strip()]=keyvalue[1].strip();
	generatedGraph[node]=neighbour_list;

#Breadth First Search
# find all the neighbours for a node insert to queue at the end
# pick from start of queue
def bfs_findPath(generatedGraph, source, destination,fuelgiven):
	queue=[];path=[];
	queue.append(source);
	if source == destination:
		return source,fuelgiven;
	pathLength={};
	pathLength[source]=0;
	while queue:
		path.append(queue.pop(0));
		node=path[-1].split('-'); #S-A S-B #S-A-B S-A-D
		singlenode=node[-1];
		neighbours=generatedGraph[singlenode];
		neighbours.sort();
		for neighbour in neighbours:
			nodeCostList=neighbour.split('-');
			if nodeCostList[0] not in node:
				newPath=path[-1]+"-"+nodeCostList[0];
				pathLength[newPath]=pathLength[path[-1]]+int(nodeCostList[1]);
				fuelRemains=fuelgiven-pathLength[newPath];
				if(fuelRemains>=0 and nodeCostList[0] == destination):
					return newPath, fuelRemains;
				queue.append(newPath);
	return 'No Path',-1;

#depth first search
# find all the neighbours for a node 
# arrange inverse to the order in graph
# insert to queue at the end, take paths on all the neighbours - pick from end of queue
def dfs_findPath(generatedGraph, source, destination,fuelgiven):
	stack=[];path=[];
	stack.append(source);
	if source == destination:
		return source,fuelgiven;
	pathLength={};
	pathLength[source]=0;
	while stack:
		path.append(stack.pop());
		node=path[-1].split('-'); #S-A S-B #S-A-B S-A-D
		singlenode=node[-1];
		neighbours=generatedGraph[singlenode];
		neighbours.sort();
		count=0;
		reversestack=[];
		for neighbour in neighbours:
			nodeCostList=neighbour.split('-');
			if nodeCostList[0] not in node:
				count += 1;
				newPath=path[-1]+"-"+nodeCostList[0];
				pathLength[newPath] = pathLength[path[-1]] + int(nodeCostList[1]);
				if(count==1):
					fuelRemains = fuelgiven - pathLength[newPath];
					if (fuelRemains >= 0 and nodeCostList[0] == destination):
						return newPath, fuelRemains;
				reversestack.append(newPath);
		stack.extend(reversestack[::-1]);
	return 'No Path',-1;

#uniform cost search
#travel and expand on neighbours for nodes in BFS order
#Use priorityQueue to expand nodes in order the of high to low priority(cost)
def ucs_findPath(generatedGraph, source, destination,fuelgiven):
	if source == destination:
	 return source,fuelgiven;
	pathCost={};
	pathCost[source]=0;
	ucsDS = PriorityQueue();
	ucsDS.put((0, source));
	while ucsDS:
		weight,path = ucsDS.get()
		node=path.split('-')[-1];
		if node == destination:
			remFuel=int(fuel)-weight;
			return path,remFuel;
		neighbours=generatedGraph[node];
		for neighbour in neighbours:
			nodeAndWeight=neighbour.split('-'); # S-30, A-40 divide by '-'
			if nodeAndWeight[0] not in path:
				newPath=path+'-'+nodeAndWeight[0]; #existing path + newwly added node
				pathCost[newPath]=weight+int(nodeAndWeight[1]); #calculate cost of the path
				ucsDS.put((pathCost[newPath], newPath))
	return 'No Path',-1

#different calls for different searches
if searchType == 'BFS':
	dronePath,fuelRemains=bfs_findPath(generatedGraph, source, destination, int(fuel));
if searchType == 'DFS':
	dronePath,fuelRemains=dfs_findPath(generatedGraph, source, destination, int(fuel));
if searchType == 'UCS':
	dronePath,fuelRemains=ucs_findPath(generatedGraph, source, destination, int(fuel));

if fuelRemains==-1:
	fo.write(dronePath);
else:
		fo.write(dronePath);
		fo.write(' ');
		fo.write(str(fuelRemains));


