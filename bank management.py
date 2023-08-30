import sqlite3,random,datetime,os
conn=sqlite3.connect("dheeraj.db")

conn.execute(''' 

            create table IF NOT EXISTS customer_details(
            accountNo VARCHAR(20) NOT NULL,
            First_name VARCHAR(20) NOT NULL,
            Last_name VARCHAR(20) NOT NULL,
            Balance INTEGER NOT NULL,
            Bcode VARCHAR(20) NOT NULL,
            MobileNo VARCHAR(10) NOT NULL,
            AdharNo CHAR(12) NOT NULL,
            Date DATE NOT NULL,
            Time TIME NOT NULL,
            UNIQUE(adharNo));
''')
conn.execute('''
             create table IF NOT EXISTS log(
             account_no CHAR(10) NOT NULL,
             T_id CHAR(10) NOT NULL,
             Description CHAR(10) NOT NULL,
             sender VARCHAR(20) NOT NULL,
             reciever VARCHAR(20) NOT NULL,
             DeAmt INTEGER,
             CrAmt INTEGER,
             Date DATE NOT NULL,
             Time TIME NOT NULL,
             PRIMARY KEY (T_id)
             );
''')
conn.commit()

def createAccount():
    accountNo  = input("enter account number")
    First_Name = input("enter name")
    Last_Name  = input("enter name")
    Balance    = int(input("enter amount"))
    Bcode      = input("enter Branch Code")
    Mobile     = int(input("enter mobile number"))
    AdharNo    = int(input("enter adhar number"))
    t = datetime.datetime.now().strftime("%x")
    d = datetime.datetime.now().strftime("%X")
    t_id=(random.randint(000000,999999))

    # print(f'Account name:{accountNo} \n First name:{First_name} \n last name:{Last_name} \n balance: {Balance} \n Bcode:{Bcode} \n mobile:{Mobile} \n adharNO:{AdharNo} \n time:{Time} \n date:{Date}')
    conn.execute(f'''
            insert into customer_details("accountNo","First_name","Last_name","Balance","Bcode","MobileNo","AdharNo","Time","Date")VALUES('{accountNo}','{First_Name}','{Last_Name}','{Balance}','{Bcode}','{Mobile}','{AdharNo}','{t}','{d}');     
    ''')
    conn.execute(f'''
            insert into log("account_no","T_id","Description","sender","reciever","CrAmt","Date","Time")VALUES('{accountNo}','{t_id}','self','{First_Name} {Last_Name}','{First_Name} {Last_Name}','{Balance}','{d}','{t}')
    ''')
    conn.commit() 
# createAccount()


def withdrawal():
    acc_no= input('Enter your Account number')
    name=input('Enter your name')
    withdraw_amount=int(input("Enter the amount you want to withdraw"))
    self_balance= conn.execute(f''' 
                    SELECT Balance FROM cuStomer_details
                    WHERE First_name is '{name}';    
    ''')
    for x in self_balance:
        if x[0]< withdraw_amount:
            print('Insufficient Balance')
        else:
            t_id= (random.randint(000000,999999))
            date_= datetime.datetime.now().strftime("%x")
            time_= datetime.datetime.now().strftime("%X")
            conn.execute(f''' 
                INSERT INTO "log" ("account_no", "T_id", "Description", "sender", "reciever", "DeAmt", "Date", "Time") VALUES ('{acc_no}', '{t_id}', 'self withdrawal', '{name}', '{name}', '{withdraw_amount}', '{date_}', '{time_}');
            ''')
            self_balance= conn.execute(f''' 
                    SELECT Balance FROM customer_details
                    WHERE First_name is '{name}';    
            ''')
            balance2= balance_generator(self_balance)
            conn.execute(f''' 
                UPDATE customer_details SET Balance= {balance2 - withdraw_amount} WHERE First_name is '{name}'
            ''')
            conn.commit()   

def deposit():
    acc_no= input('Enter your Account number')
    name=input('Enter your name' )
    deposit_amount=int(input("tEnter the amount you want to deposit"))
    self_balance= conn.execute(f''' 
                    SELECT Balance FROM customer_details
                    WHERE First_name is '{name}';    
    ''')
    for x in self_balance:
        if x[0]< deposit_amount:
            print('Insufficient Balance')
        else:
            t_id=(random.randint(000000,999999))
            date_= datetime.datetime.now().strftime("%x")
            time_= datetime.datetime.now().strftime("%X")
            conn.execute(f''' 
                INSERT INTO "log" ("account_no", "T_id", "Description", "sender", "reciever", "CrAmt", "Date", "Time") VALUES ('{acc_no}', '{t_id}', 'self deposit', '{name}', '{name}', '{deposit_amount}', '{date_}', '{time_}');
                
            ''')
            self_balance= conn.execute(f''' 
                    SELECT Balance FROM customer_details
                    WHERE First_name is '{name}';    
            ''')
            balance2= balance_generator(self_balance)
            conn.execute(f''' 
                UPDATE customer_details SET Balance= {balance2 + deposit_amount} WHERE First_name is '{name}'
            ''')
            conn.commit()  


def transferMoney():
    accountNo1=input("enter your account number")
    name1=input("enter your name")
    accountNo2=input("enter reciever account number")
    name2=input("enter reciever name")
    balance=int(input("enter the amount you want to transfer"))

    a=conn.execute(f'''
              select Balance from customer_details
              where First_name is '{name1}';

                ''')
    for x in a:
        if x[0]<balance:
            print('insufficient balance')
        else:
            t_id=random.randint(000000,99999)
            date=datetime.datetime.now().strftime("%x")
            time_=datetime.datetime.now().strftime("%X")
            conn.execute(f'''
                        insert into "log"("account_no","T_id","Description","sender","reciever","DeAmt","Date","Time")VALUES('{accountNo1}','{t_id}','{name1}sent{name2}','{name1})','{name2}','{balance}','{date}','{time_}');
            ''')
            recievers_balance= conn.execute(f'''
                                        select Balance from customer_details
                                        where First_name is '{name2}';  
            ''')        
            balance2=balance_generator(recievers_balance)
            conn.execute(f'''
                        update customer_details set Balance={balance2+balance}
                        where First_name is '{name2}'
            ''')
            senders_balance=conn.execute(f'''
                                        select Balance from customer_details
                                        where First_name is '{name1}';
            ''')
            balance3=balance_generator(senders_balance)
            conn.execute(f'''
                        update customer_details set Balance={balance3-balance}
            where First_name is'{name1}'
            ''')
            conn.commit()

def balance_generator(cursor_):
        for item_ in cursor_:
            _= item_[0]
            return _
# deposit()
# withdrawal()

def log():
    accnm=input("enter your account name")
    _=conn.execute(f'''
                select * from log where sender='{accnm}'or reciever='{accnm}';
    ''')
    
    for i in _:
        print(f'Account No: \t {i[0]} \n T_ID \t {i[1]} \n Description \t {i[2]} \n Sender \t {i[3]} \n Reciever \t {i[4]} \n DeAmt \t {i[5]} \n CrAmt \t {i[6]} \n Date \t {i[7]} \n Time \t {i[8]} \n')

def statement():
    statement_name=input('Enter your name')
    statement_holder=conn.execute(f'''
                    Select * FROM customer_details WHERE First_name = '{statement_name}' ;
    ''')
    f2 = open("Statement.txt", "w+", encoding='utf-8')
    for i in statement_holder:
        for j in range(len(i)):
            f2.write(str(i[j]))
            f2.write('\t\t\t\t')
    f2.write('\n')



# start of the program
ch='8'
num=0
try:
    while ch != 7:

        print("\033[1m" + "\t\t\t\t\tMAIN MENU" + "\033[0m")
        print("\t\t\t\t\t1. CREATE ACCOUNT")
        print("\t\t\t\t\t2. WITHDRAW AMOUNT")
        print("\t\t\t\t\t3. DEPOSIT AMOUNT")
        print("\t\t\t\t\t4. TRANSFER AMOUNT")
        print("\t\t\t\t\t5. ACCOUNT LOGS")
        print("\t\t\t\t\t6. STATEMENT")
        print("\t\t\t\t\t7. EXIT")
        print("\t\t\t\t\tSelect Your Option (1-8)\n")    
        if ch == '1':
            createAccount()
        elif ch =='2':
            withdrawal()
        elif ch == '3':
            deposit()
        elif ch == '4':
            transferMoney()
        elif ch == '5':
            log()
        elif ch == '6':
            statement()
        elif ch == '7':
            print("\t\t\t\t\t\t" + "\033[1m" +"Thanks for using bank managemnt system" +"\033[0m")
            break
        elif ch == '8':
            pass
        else :
            print("\t\t\t\t\Invalid choice")
        ch = input("\t\t\t\t\tEnter your choice : ")
        print("\n")

except Exception as exc:
    print('\n\t\t\t\t\t try again')
    os.system('Clear')
    os.system('Python bank management.py')