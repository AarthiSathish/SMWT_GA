from utils import *
from itertools import permutations
import math
import time as t
import random
from search_template import *
import copy
MAX=10000000000000
class TotWeightedTardiness(Problem):
    def __init__(self,time,weights,due,pop_num):
        self.time=time
        self.weights=weights
        self.due=due
        self.n=len(time)
        self.population=[]
        self.wmd=self.get_wmdd()
        self.spt=self.wspt()
        self.ed=self.edd()
        self.morhodg=self.hodgson()
        self.min=self.minheur()
        self.init_population(pop_num)
        self.initial=self.get_individual()

    def getNum(self,v):
    	index = random.randint(0, len(v) - 1)
    	num = v[index]
    	v.remove(v[index])
    	return num

    def get_individual(self):
        v=list(range(0,self.n))
        individual=[]
        while(len(v)):
            individual.append(self.getNum(v))
        return individual

    def get_wmdd(self):
        wmdd=[]
        for i in range(self.n):
            wmdd.append((max(self.due[i],self.time[i])/self.weights[i],i))
        wmdd.sort()
        return wmdd

    def wspt(self):
        spt=[]
        for i in range(self.n):
            spt.append((self.time[i]/self.weights[i],i))
        spt.sort()
        return spt

    def edd(self):
        edd=[]
        for i in range(self.n):
            edd.append((self.due[i],i))
        edd.sort()
        return edd

    def get_tardiness(self,seq):
        t=0
        s=[]
        for i in seq:
            t=t+self.time[i[2]]
            td=max(0,t-i[0])
            s.append((i[0],self.weights[i[2]]*td,i[2]))
        return s

    def hodgson(self):
        seq=[]
        removed=[]
        for i in range(self.n):
            seq.append((self.due[i],0,i))
        seq.sort()
        t=1
        while(t==1):
            seq=self.get_tardiness(seq)
            max=0
            mtime=self.time[seq[max][2]]
            ind=-1
            for i in range(len(seq)):
                if(seq[i][1]!=0):
                    ind=i
                    break
                if(self.time[seq[i][2]]>mtime):
                    max=i
                    mtime=self.time[seq[max][2]]
            if(ind!=-1):
                r=seq.pop(max)
                removed.append(r)
            else:
                t=0
        return (seq+removed)

    def minheur(self):
        val=[]
        for i in range(40):
            val.append((self.due[i]*self.time[i]/self.weights[i],i))
        val.sort()
        return val

    def init_population(self,pop_num):
        ind=[i[1] for i in self.wmd]
        self.population.append((self.fitness(ind),ind))
        ind=[i[1] for i in self.spt]
        self.population.append((self.fitness(ind),ind))
        ind=[i[1] for i in self.ed]
        self.population.append((self.fitness(ind),ind))
        ind=[i[2] for i in self.morhodg]
        self.population.append((self.fitness(ind),ind))
        ind=[i[1] for i in self.min]
        self.population.append((self.fitness(ind),ind))
        for i in range(pop_num-len(self.population)):
            individual=self.get_individual()
            if(individual not in self.population):
                self.population.append((self.fitness(individual),individual))

    def fitness(self,state):
        if(sorted(state)!=list(range(0,40))):
            return -MAX
        wt=0
        ct=0
        for i in state:
            ct=ct+self.time[i]
            td=max(0,ct-self.due[i])
            wt=wt+(self.weights[i]*td)
        return (-1*wt)

    def actions(self,state):
        swaps=[]
        for i in range(50):
            k=random.randint(0,len(state)-1)
            k1=random.randint(0,len(state)-1)
            if(k!=k1):
                swaps.append((k,k1))
        return swaps

    def result(self,state,action):
        new=copy.deepcopy(state)
        new[action[0]],new[action[1]]=new[action[1]],new[action[0]]
        return new

    def value(self,state):
        return self.fitness(state)

def genetic_algorithm(p,ngen,pmut):
    fittest_individual=max(p.population)
    if(fittest_individual[0]==0):
        return fittest_individual
    for i in range(ngen):
        population=crossover(p,select(p))
        p.population=mutate(p,population,pmut)
        m=max(p.population)
        if(m[0]>fittest_individual[0]):
            fittest_individual=m
        if(fittest_individual[0]==0):
            return fittest_individual
    return fittest_individual

def select(p):
    sampler=weighted_sampler([i[1] for i in p.population],[-1/i[0] for i in p.population])
    return ([[sampler() for _ in range(2)] for _ in range(len(p.population))])

def crossover(p,parents):
    popl=[]
    for i in parents:
        c=random.randint(0,len(i[0]))
        offspring=[(p.fitness(i[0][:c]+i[1][c:]),i[0][:c]+i[1][c:]),(p.fitness(i[1][:c]+i[0][c:]),i[1][:c]+i[0][c:])]
        popl.append(max(offspring))
    return popl

def mutate(p,population,pmut):
    for i in range(len(population)):
        if(probability(pmut)):
            c1=random.randint(0,p.n-1)
            c2=random.randint(0,p.n-1)
            population[i][1][c1],population[i][1][c2]=population[i][1][c2],population[i][1][c1]
            population[i]=(p.fitness(population[i][1]),population[i][1])
    return population






f = open("wt40.txt", "r")
f1=open("wtopt40.txt","r")
error=0
no=0
notoptimal=0
tot_time=0
for x in f:
    time=[]
    weights=[]
    due=[]
    for i in x.split():
        time.append(int(i))
    i1=f.readline()
    for i in i1.split():
        time.append(int(i))
    i1=f.readline()
    for i in i1.split():
        weights.append(int(i))
    i1=f.readline()
    for i in i1.split():
        weights.append(int(i))
    i1=f.readline()
    for i in i1.split():
        due.append(int(i))
    i1=f.readline()
    for i in i1.split():
        due.append(int(i))
    ans=int(f1.readline().split()[0])
    pop_num=10
    anss=[]
    for ind in range(5):
        st=t.time()
        p=TotWeightedTardiness(time,weights,due,pop_num)
        g=genetic_algorithm(p,10000,0.1)
        tot_time=tot_time+(t.time()-st)
        anss.append(-1*g[0])
    no=no+1
    if(min(anss)!=ans):
        if(min(anss)>ans):
            error=error+(min(anss)-ans)
            notoptimal=notoptimal+1
        print("\nOptimal Answer:",ans,"\tObtained Answer:",min(anss))
print("\nTotal Instances:",no)
print("\nInstances with non-optimal solution:",notoptimal)
print("\nAverage Deviation from Optimal value per Instance:",error/(no-1))
print("Avg. Time per Instance:",tot_time/no)

