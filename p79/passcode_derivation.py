# passcode_derivation.py
# Given list of successful login attempts
# consisting of 3 digits of the password
# determine the shortest possible complete password

import collections

def modify_possible_passwords (password, login_att):
    
    for ch in str(login_att):
        if ch not in str(password):
            password += ch
        else: # do nothing unless more than one
            chcounter = collections.Counter (str(login_att))
            pass_counter = collections.Counter (password)
            while chcounter[ch] > pass_counter[ch]:
                password += ch
                pass_counter[ch] += 1
                
    return password

def order_possible_password (password, login_att):
    login_str = str(login_att)

    password_index = []
    for ch in login_str:
        password_index.append (password.find (ch))

    
    password = list(password)
    
    
    for i in range (len(password_index)-1):
        for j in range(i+1, len(password_index)):
            if password_index[i] > password_index[j]:
                temp = password[password_index[i]]
                password[password_index[i]] = password[password_index[j]]
                password[password_index[j]] = temp

                temp_index = password_index[i]
                password_index[i] = password_index[j]
                password_index[j] = temp_index

    return "".join(password)

short_password = ""
input_file = "keylog.txt"
with open (input_file, 'r') as f1:
    for line in f1:
        x1 = line.split('\n')
        short_password = modify_possible_passwords (short_password,x1[0])

f1.close()

with open (input_file, 'r') as f2:
    for line in f2:
        x1 = line.split ('\n')
        short_password =  order_possible_password (short_password, x1[0])
f2.close()

with open (input_file, 'r') as f3:
    for line in f3:
        x1 = line.split ('\n')
        old_password = short_password
        short_password =  order_possible_password (short_password, x1[0])
        if old_password != short_password:
            print old_password, short_password, x1[0]
f3.close()

print short_password
