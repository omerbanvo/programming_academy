import threading

Counter = 0
#פעולה שמעלה את המשתנה הגלובלי ב 100,000
def Increase():
    global Counter
    for i in range(100000):
        Counter += 1

thread1 = threading.Thread(target= Increase)

#פעולה שמחסירה מהמשתנה הגלובלי 100,000ד
def Decrese():
    global Counter
    for i in range(100000):
        Counter -=1

thread2 = threading.Thread(target = Decrese)
thread1.start()
thread2.start()
thread1.join()
thread2.join()
print(Counter)
