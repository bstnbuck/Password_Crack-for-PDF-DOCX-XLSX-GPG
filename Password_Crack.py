
import itertools,string, msoffcrypto, pikepdf, sys, subprocess


def main():                                                                 #main function to select function
    print("Which file would you like to decrypt?")
    which = int(input("1 = .pdf, 2 = .docx, 3 = PGP, 11 =simple brute-force a password (only passwords with 1-5 letters)\n99 = Stop! : "))
    if which == 1:
        try:                                                                #start functions, if error returned print error-message
            file_pdf = str(input("Which PDF-File?\n"))                      #enter file to search password
            decrypt_pdf(file_pdf)
        except:
            print("Error!")
    elif(which == 2):
        try:
            file_docx = str(input("Which DOCX/XLSX-File?\n"))
            decrypt_docx(file_docx)
        except:
            print("Error!")
    elif(which == 3):
        try:
            file_gpg = str(input("Which File?\n"))
            decrypt_gpg(file_gpg)
        except:
            print("Error!")
    elif(which == 11):
        try:
            print(brute_force())
        except:
            print("Error!")
    elif(which == 99):                                                      #if you still know the password. :D
        print("Stopping...")
        exit(0)
    else:
        print("not implemented yet")                                        #if you're stupid :D
    input("Press any key to continue...")



def brute_force():                                                          #to proof how long (attempts) the algorithm need to find password, use this.
    password = input("which password do you want to brute-force? ")         #input searched password
    chars = string.ascii_letters + string.digits                            #all ascii-letters and digits
    attempts = 0                                                            #count attempts
    if(len(password) <=5):                                                  #proof password-size 
        for plen in range(1, 6):                                            #all passwords with 1 to 5 letters
                for guess in itertools.product(chars, repeat=plen):         #guess = generated password
                        attempts += 1                                       #increment counter 
                        guess = ''.join(guess)                              
                        #print(guess,attempts)                              #for debug, print generated password and attempt
                        if guess == password:                               #proof guess = password
                           return ("[BRUTE-FORCE]: found password! password: {} with {} attempts".format(guess,attempts))   #if true print password and attempts 
    else:
        print("password too long!")
                                 


def decrypt_pdf(file_pdf):                                                          
    chars = string.ascii_letters + string.digits
    attempts = 0
    print("Searching for password!\nThis may take long time...")            #print that you can go shopping :D
    for plen in range(1, 6):                                                #brute-force procedure already the same
        for guess in itertools.product(chars, repeat=plen):
            attempts += 1
            guess = ''.join(guess)
            #print(guess,attempts)                                          #Debug
            try:
                pdf=pikepdf.open(file_pdf, password=guess)                  #try start pikepdf with open the file (declared as file_pdf) and generated password
                pdf.save('decrypted.pdf')                                   #save opened pdf-file decrypted in new file
                print("[PDF BRUTE-FORCE]: found password! password: {} with {} attempts".format(guess,attempts))    #print that you've won :D
                return True
            except:
                #print(str(attempts)+" not correct!")                       #Debug
                continue                                                    #if open failed, continue with next password

    
def decrypt_docx(file_docx):
    chars = string.ascii_letters + string.digits
    attempts = 0
    print("Searching for password!\nThis may take long time...")            #print that you can go shopping :D
    for plen in range(1, 6):                                                #already the same
        for guess in itertools.product(chars, repeat=plen):
            attempts += 1
            guess = ''.join(guess)
            #print(guess,attempts)                                          #Debug
            try:
                file = msoffcrypto.OfficeFile(open(file_docx, "rb"))        #try start msoffcrypto-tool as OfficeFile with file-name and read-access only 
                file.load_key(password=guess)                               #if password required, take the generated
                file.decrypt(open("decrypted.docx", "wb"))                  #if password correct, open new file with write-access and copy content in it 
                print("[DOCX, XLSX BRUTE-FORCE]: found password! password: {} with {} attempts".format(guess,attempts))
                return True
            except:
                #print(str(attempts)+"not correct!")                        #Debug
                continue                                                    #otherwise continue with next password
    

def decrypt_gpg(file_gpg):
    chars = string.ascii_letters + string.digits
    attempts = 0
    print("Searching for password!\nThis may take long time...")            #print that you can go shopping :D
    for plen in range(1, 6):                                                #already the same
        for guess in itertools.product(chars, repeat=plen):
            attempts += 1
            guess = ''.join(guess)
            #print(guess,attempts)                                          #Debug
            try:
                if checkPassword(file_gpg, guess):                          #try get true by using function checkPassword which use the file as file_gpg and generated password
                    print("[GPG BRUTE-FORCE]: found password! password: {} with {} attempts".format(guess,attempts))    #print success!
                    return True
            except:
                #print(str(attempts)+" not correct!")                       #Debug
                continue                                                    #otherwise next password


def checkPassword(filename, password):                                      #function to check password from gpg-encrypted files
    output=""
    try:                                                                    #try create new subprocess with check_output function. Execute command at shell.
                                                                            #gpg = start gpg, --pinentry-mode loopback = send a password directly to GnuPG, 
                                                                            #rather than GnuPG itself prompting for the password.
                                                                            #--output decrypted_gpg.txt = after decryption save it decrypted in txt-file
                                                                            #--batch --yes = execute int batch true
                                                                            #--passphrase password = generated password from function decrypt_gpg()
                                                                            #-d filename = encrypted file to decrypt
                                                                            #shell = True --> open in shell
        subprocess.check_output("gpg --pinentry-mode loopback --output decrypted_gpg.txt --batch --yes --passphrase " + password + " -d " + filename + " 2>&1", shell=True)
        return True                                                         #if executed without errors return True and password was correct
    except subprocess.CalledProcessError as e:                              #if subprocess-error you can print it out
        #out = str(e.output)                                                #Debug
        #print(out)                                                         #Debug
        return False                                                        #password wasn´t correct
    except:
        return False                                                        #if other error return False --> next password



if __name__ == "__main__":                                                  #declare function main() as first executed function
    main()