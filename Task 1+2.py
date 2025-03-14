answer=""
answers=["cairo","the buyer","hydrogen","7 day"]
question=[" what the capital of the egypt :"," What is the largest planet in the solar system? :"
          ," What is the chemical element symbolized by [ H ] ? : ",
          "What are the days of the week? : "]
count=0
z=False
result_2=0
while  answers[0] != answer and not z:
    answer=input(question[0])
    count+=1
    if answers[0]==answer:
        result_2=25
        print    ("you win") 
        break
    elif count==3:
        print    ("you lose")
        break
    print    ("you lose")

count=0
result_1=0
while  answers[1] != answer and not z:
    answer=input(question[1])
    count+=1
    if answers[1]==answer:
        result_1=25
        print    ("you win") 
        break
    elif count==3:
        print    ("you lose")
        break
    print    ("you lose")
    

count=0
result_3=0
while  answers[2] != answer and not z:
    answer=input(question[2])
    count+=1
    if count==3: 
        print    ("you lose")
        break
    elif answers[2]==answer:
        result_3=25
        print    ("you win")
        break
    print    ("you lose")
 
count=0 
result_4=0  
while  answers[3] != answer and not z:
    answer=input(question[3])
    count+=1
    if count==4:
        
        print    ("you lose")  
        break
    elif answers[3]==answer:
        result_4=25
        print    ("you win")
        break
    print    ("you lose")   
print("result is : ",result_1+result_2+result_3+result_4) 
z=input("Do you want to finish the quiz? : ")
if z=="n":
    print("aa")
