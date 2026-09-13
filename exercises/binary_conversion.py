def decimal_to_binary(n, bit_size):
    counter= bit_size-1
    bits = 1
    while counter>0:
        bits*=2
        counter-=1

    binary_list = []
    while bits > 0:
        if bits<=n:
            binary_list.append(1)
            n = n-bits
        else:
            binary_list.append(0)
        
        bits = bits//2
    return binary_list

    

def apply_two_complement():
    pass


try:
    regular_number = int(input("enter a decimal number:\n"))
    def get_bit_size(num):
        if num == 0:
            return 0
        i = 1
        counter=0
        while i <= num:
            counter+=1
            i*=2
        return counter

    bit_size = get_bit_size(regular_number)
except: 
    print("you can input only numbers.")

print(decimal_to_binary(regular_number, bit_size))
