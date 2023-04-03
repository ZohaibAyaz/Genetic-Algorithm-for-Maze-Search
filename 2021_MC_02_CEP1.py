from pyamaze import maze,COLOR,agent
from random import *
rows=17
columns=17
a=maze(rows,columns)
a.CreateMaze(rows,columns,loopPercent=100)
bb=agent(a,1,1,shape='arrow',footprints=True,color='yellow')
dic=a.maze_map
# print(dic)

Total_population=500
path,path_length,inf_steps,fitt=[],[],[],[]
iteration=0
ch=0
W_l,W_f,W_t=2,3,3

                                # Defining (creating) different User-Defined Functions
# User-Define Function for generating population
def Random_population():
        population=[[[1]+[randint(1,rows) for _ in range (columns-2)]+[rows],[randint(0,1) for _ in range(2)]] for _ in range (Total_population)]
        return population
# User-Define Function for calculating Total turns
def Total_Turns():
    Turns=[]
    for i in range(Total_population):
        j,o=population[i]
        # print(j)
        turns=0
        for k in range (columns-1):
            if j[k]!=j[k+1]:
                turns+=1
        Turns.append(turns)   
    return Turns           

#  User-Define Function for calculating Path, Path length, Infeasible_steps
def infeasible_steps(l:list):
    chr, [orient, direction] = l
    # print(chr, orient, direction)
    inf_steps=[]
    path=[]
    if ch==1:
        path.append((1,1))
    if rows!=columns:
        orient=0
    #  Exclusive or operator for creating selection bit for selecting row wise or column wise movement of agent
    select=orient^direction  
    a_point,inc,inf_steps=(1,1),1,[]
    for i in range (0,len(chr)-1):
        next=i+1
        Boundary=(chr[i+1]+1) if chr[i+1]>chr[i] else (chr[i+1]-1)
        while inc!= Boundary:
            if orient==0:
                b_point=(inc,next+select)
            else:
                b_point=(next+select,inc)
            if ch==1 and b_point not in ((1,1),(rows,columns)):
                path.append(b_point)
            if b_point[0]-a_point[0]!=0:
                if b_point[0]-a_point[0]>0:
                    if dic[a_point]['S']==0:
                            inf_steps.append(1)
                    else:
                        inf_steps.append(0)
                else:
                    if dic[a_point]['N']==0:
                            inf_steps.append(1)
                    else:
                        inf_steps.append(0)
            elif b_point[1]-a_point[1]!=0:
                if b_point[1]-a_point[1]>0:
                    if dic[a_point]['E']==0:
                            inf_steps.append(1)
                    else:
                        inf_steps.append(0)
                else:
                    if dic[a_point]['W']==0:
                            inf_steps.append(1)
                    else:
                        inf_steps.append(0)
            # Assigning value of b to a
            a_point=b_point
            if chr[i+1]>chr[i]:
                    inc+=1
            else: 
                    inc-=1
        if chr[i+1]>chr[i]:
            inc-=1
        else:
            inc+=1
    if ch==1:
        path.append((rows,columns))
        return path,len(inf_steps),sum(inf_steps)
    return len(inf_steps),sum(inf_steps)   

#   User define function for creating chromosomes from parents(fittest chromosomes)
def Cross_over(chr:list):
    cross_point=randint(2,columns-2)
    # print(cross_point)
    let=int(Total_population/2)
    for i in range (let,(Total_population-1),2):
        chr[i][0]=chr[i-let][0][0:cross_point]+chr[i-let+1][0][cross_point:]
        chr[i+1][0]=chr[i-let+1][0][0:cross_point]+chr[i-let][0][cross_point:]

#   User define function for changing random bit in the chromosomes after crossing over
def Mutation(chr:list):
    for i in range (Total_population):
        Gene,direction_bit=chr[i]
        Gene[randint(2,columns-2)]=randint(1,rows)
        if i>=int(Total_population/2):
            direction_bit[0],direction_bit[1]=randint(0,1),randint(0,1)

#   User define function for calculating fitness of chromosome
def fitness(turns, length, infeasible):
    # inf_min=0
    f_t=1-(turns-min(Turn))/(max(Turn)-min(Turn))
    f_l=1-(length-min(path_length))/(max(path_length)-min(path_length))
    f_inf=1-(infeasible-min(inf_steps))/(max(inf_steps)-min(inf_steps))
    return (100*W_f*f_inf)*((W_l*f_l)+(W_t*f_t))/(W_l+W_t)

#  Start of Main Function
population=Random_population()
# print(population)       
while(iteration<2500):
    path,path_length,inf_steps,fitt=[],[],[],[]
    print(f'Generation: {iteration}') 
    Turn=Total_Turns() 
    # print(Turn)       
    inf=[infeasible_steps(chr) for chr in population]
    # print(f'{inf}\n')
    for i in range (Total_population):
        path_length.append(inf[i][0]); inf_steps.append(inf[i][1])
    for i in range (Total_population):
        fit=fitness(Turn[i], path_length[i], inf_steps[i])
        fitt.append(fit)
        #  Checking solution found or not
        if inf_steps[i]==0:
            ch=1
            sol_path, sol_path_length, sol_inf = infeasible_steps(population[i])
            sol_turns = Turn[i]
            print(f'\nChromosome = {population[i][0]}\nPath Length = {sol_path_length}\nTurns = {sol_turns}\nInfeasible Steps = {sol_inf}\nPath = {sol_path}')
            a.tracePath({bb:sol_path}, delay=150)
            a.run()
            break
    if ch==1:
        break
    # print(path_length, inf_steps)
    # print(fitt)

    #  Sorting population on basis of fitness
    pop=list(zip(population,fitt))
    Sorted_pop=sorted(pop,key= lambda x: x[1],reverse=True)
    population=[x[0] for x in Sorted_pop]
    # print(f'{population}\n')

    #  Sorting turns on basis of fitness
    t=list(zip(Turn,fitt))
    Sorted_t=sorted(t,key= lambda x: x[1],reverse=True)
    Turn=[x[0] for x in Sorted_t]
    # print(Turn)
    
    Cross_over(population)
    # print(f'{population}\n')
    Mutation(population)
    # print(f'{population}\n')
    iteration+=1

