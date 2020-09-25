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
        print('Debug: checked first letter in string')
        if ifupper:
            Uppercase = True
            print('Debug: letter is upper')
            tester = tester[1:]
            print('Debug: now checking ', tester)
        elif iflower:
            Lowercase = True
            print('Debug: letter is lower')
            tester = tester[1:]
            print('Debug: now checking ', tester)
        elif len(Password) >= 6:
            Length = True
        if len(tester) == 0:
            Testing = False
        else:
            Number = True
            print('Debug: other symbol detected')
            tester = tester[1:]
            print('Debug: now checking ', tester)
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