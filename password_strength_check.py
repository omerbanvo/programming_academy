points = 0 #points counter - global
#function recieves a password as an argument, and gives it a rating
def password_strength():
    global points
    if points <=0:
        print("password is weak")
    if points >=1 and points <=3:
        print("moderate password")
    if points >= 4:
        print("strong password")    

#adding all points:
def adding_points(password):
    global points
    contains_common_words_points = lambda item: ("admin" in item) + ("123456" in item)
    sub = contains_common_words_points(password)
    points -=sub
    try:
        x = has_special_characters(password)
        if x!= 0:
            points+= x
    except:
        pass

    has_lower = lambda password: any(p.islower() for p in password)
    if has_lower(password):
        points+=1
    has_upper = lambda password: any(p.isupper() for p in password)
    if(has_upper(password)):
        points+=1
    has_nums = lambda password: any(p.isdigit() for p in password)
    if has_nums(password):
        points+=1
    points += points_for_len(password)




#return weather the string has special letters
def has_special_characters(password):
    special_characters = [
        "!", "@", "#", "$", "%", "^", "&", "*",
        "(", ")", "-", "_", "=", "+",
        "[", "]", "{", "}", "|",
        ";", ":", "'", '"', ",", ".", "<", ">",
        "/", "?", "`", "~"
    ]
    if any(s in special_characters for s in password):
        return 1

#return points for each length of word
def points_for_len(password):
    length = len(password) 
    if length > 8 and length < 11:
        return 1
    elif length >= 12:
        return 2
    else:
        return 0

password = "P@ssw0rd"
#adding the points:
adding_points(password)
#getting feedback for the points
password_strength()