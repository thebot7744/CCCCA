Password = input('Enter Your Password: ')
Testing = True
tester = Password
Uppercase = False
Lowercase = False
Number = False
Length = False
Strength = 0

#Checking the password strength
while Testing:
    for letter in tester:
        g = tester[:1]
        ifupper = g.isupper()
        iflower = g.islower()
        ifnumeric = g.isnumeric()
        if ifupper:
            Uppercase = True
            tester = tester[1:]
        elif iflower:
            Lowercase = True
            tester = tester[1:]
        elif ifnumeric:
            Number = True
            tester = tester[1:]
        if len(tester) == 0:
            Testing = False
if len(Password) >= 6:
    Length = True
if Lowercase:
    Strength += 1
if Uppercase:
    Strength += 1
if Number:
    Strength += 1
if Length:
    Strength += 1
#Showing Password Strength
if Strength == 1:
    print("Your password is very weak")
if Strength == 2:
    print("Your password is weak")
if Strength == 3:
    print("Your password is good")
if Strength == 4:
    print("Your password is strong")