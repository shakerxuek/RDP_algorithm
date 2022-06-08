#Question1
def Mean(x):
    sum=0
    for i in x:
        sum+=i
    print(sum/len(x))

#Question2
def Exponetial_sum(a:int,b:int):
    if a<=0 or b<=0:
        print(0)
    else:
        sum=0
        for i in range(1,b+1):
            sum+=a**i
        print(sum)

#Question3
def String_sum(x:str):
    temp=x.split(',')
    if len(temp)<2:
        print('error')
    else:
        sum=0
        for i in temp:
            if i==' ':
              print('error')    
              return 0
            else:
                i=float(i)
                sum+=i
        print(sum)
        
#Question4
def Bounding_box(x:list):
    a=[]
    b=[]
    for i in x:
        a.append(i[0])
        b.append(i[1])
    maxX=max(a)
    maxY=max(b)
    minX=min(a)
    minY=min(b)
    maxp=(maxX,maxY)
    minp=(minX,minY)
    c=[minp,maxp]
    print(c)

#Question5
def Odd_elements(x:list):
    a=x[1::2]
    print(a)

#Question6
def Fibonacci(fibonacci_iter):
    output=[]
    for i in range(0,fibonacci_iter):
        if i==0:
            output.append(0)
        elif i==1:
            output.append(1)
        else:
            output.append(output[i-2]+output[i-1])
    print(output)

#human iterate, God recurve......
def Fibonacci(fibonacci_rec):
    if fibonacci_rec<=1:
        return fibonacci_rec
    else:
        return Fibonacci(fibonacci_rec-2)+Fibonacci(fibonacci_rec-1)

#uncomment them for test ( •̀ ω •́ )✧ 
# fibonacci_rec=int(input("How many recur?"))
# output=[]
# for i in range(0, fibonacci_rec):
#     output.append(Fibonacci(i))
# print(output)

#Question7
def Digits(x:int):
    output=[]
    while x:
        output.append(x%10)
        x=x//10
    output.reverse()
    print(output)

#Question8
def Palindome(x:str):
    output=[]
    routput=[]
    for i in x:
        output.append(i)
        routput.append(i)
    output.reverse()
    if output==routput:
        print(True)
    else:
        print(False)

#Question9
def Point_distance(x:tuple,y:tuple,z:tuple):
    if y==z:
        output=((x[0]-y[0])**2+(x[1]-y[1])**2)**0.5
    else:
        a=((x[0]-y[0])**2+(x[1]-y[1])**2)**0.5
        b=((x[0]-z[0])**2+(x[1]-z[1])**2)**0.5
        c=((z[0]-y[0])**2+(z[1]-y[1])**2)**0.5
        p=(a+b+c)/2
        s=(p*(p-a)*(p-b)*(p-c))**0.5
        output=s*2/c
        print(a,b,c,s)
    print(output)
    return output

#test part, uncomment one of them to test
#Q1:Mean([2,4,5,7,2])
#Q2:Exponetial_sum(3,4)
#Q3:String_sum('3.8,4.5,7.8')
#Q4:Bounding_box([(3,4),(-4,7),(2,5)])
#Q5:Odd_elements([3,'s',6,'y',7,'u','dse','789'])
#Q6:see details in the code for this question (ToT)/~~~
#Q7:Digits(68357529)
#Q8:Palindome('rotator')
#Q9:Point_distance((-1,0),(2,0),(-1,4))

