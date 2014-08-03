#!/usr/bin/python

#http://pythonhosted.org/python-gnupg/
import gnupg
import os
import tarfile
import json
import string
import random
 
class gpgj():   
    
    homefile = "/home/light/Desktop/testgpg"
    homefileout = "/home/light/Desktop/testgpgout"
    homefileout3 = "/home/light/Desktop/testgpgoutverif"
    gpgp = None
    password = 'jlhdie'
    mailuser = 'johnleger@free.fr'
    dico = {}
    
    def __init__(self):
        self.gpgp = gnupg.GPG(gnupghome="/home/light/.gnupg")
        self.gpgp.encoding = 'utf-8'
            
    def crypt_string(self,string):
        return str(self.gpgp.encrypt(string,self.mailuser))
    
    def crypt_file(self,filepathin,filepathout):
        f = open(filepathin, 'rb')
        if not self.gpgp:
            print "SOUCIS"
        status = self.gpgp.encrypt_file(f, self.mailuser, output=filepathout)
        if not status.ok:
            print "error crypting "+filepathin
            print 'status: ', status.status
            print 'stderr: ', status.stderr
              
    def decrypt_string(self,string):
        return str(self.gpgp.decrypt(string,passphrase=self.password))
    
    def decrypt_file(self,filepathin,filepathout):
        status = self.gpgp.decrypt_file(open(filepathin, 'rb'), passphrase=self.password, output=filepathout)
        if not status.ok:
            print "error decrypting "+filepathin
            print 'status: ', status.status
            print 'stderr: ', status.stderr
      
    
    def crypt_folder(self,path, pathout):
        foldercontent = os.listdir(path)
        foldercontentout = os.listdir(pathout)
        for files in foldercontent:
            #If it is not an invisible folder
            if not files[0] == ".":
                #If it is an application
                if files[-4:] == ".app":
                    if files+".gpgz" not in foldercontentout:
                        print files+" is an application"
                        tar = tarfile.TarFile(path+"/"+files+".tar", 'w')
                        tar.add(path+"/"+files,files)
                        tar.close()
                        self.crypt_file(path+"/"+files+".tar",pathout+"/"+files+".gpgz")
                        try:
                            os.remove(path+"/"+files+".tar")
                        except:
                            print "error removing tar"
                    else:
                        print files+" is an application already gppz"
                #If it is an gpg file
                elif files[-4:] == ".gpg" or files[-5:] == ".gpgz":
                    print files+" is already gpged (1)"
                #If it is a folder
                elif os.path.isdir(path+"/"+files):
                    #print files+" is a directory"
                    try:
                        os.mkdir(pathout+"/"+files)
                    except:
                        pass
                    self.crypt_folder(path+"/"+files,self.homefileout+"/"+files)
                #If it is a folder
                else: 
                    if files+".gpg" in foldercontentout:
                        print files+" is already gpged (2)"
                    else:
                        print "Crypting: "+files
                        self.crypt_file(path+"/"+files,pathout+"/"+files+".gpg")
                        
    def decrypt_folder(self,path, pathout):
        foldercontent = os.listdir(path)
        foldercontentout = os.listdir(pathout)
        for files in foldercontent:
            #If it is not an invisible folder
            if not files[0] == ".":
                #If it is an application
                if files[-5:] == ".gpgz":
                    if files[:-5] not in foldercontentout:
                        print "decrypting application "+files
                        self.decrypt_file(path+"/"+files,pathout+"/"+files+".tar")
                        tar = tarfile.TarFile(pathout+"/"+files+".tar", 'r')
                        tar.extractall(pathout)
                        tar.close()
                        try:
                            os.remove(pathout+"/"+files+".tar")
                        except:
                            print "error removing tar"
                    else:
                        print files +" already decrypted (2)"
                #If it is an gpg file
                elif files[-4:] == ".gpg":
                    if files[:-4] not in foldercontentout:
                        print "decrypting "+files
                        self.decrypt_file(path+"/"+files,pathout+"/"+files[:-4])
                    else:
                        print files+" already decrypted (1)"
                #If it is a folder
                elif os.path.isdir(path+"/"+files):
                    try:
                        os.mkdir(pathout+"/"+files)
                    except:
                        pass
                    self.decrypt_folder(path+"/"+files, pathout+"/"+files)
                else: 
                    print "ERROR file unknown "+files
                        
    def crypt_folder_new(self,path, pathout):
        foldercontent = os.listdir(path)
        foldercontentout = self.load_name_already_crypted(pathout)
        for files in foldercontent:
            #If it is not an invisible folder
            if not files[0] == ".":
                
                #If it is an application
                if files[-4:] == ".app":
                    if files not in foldercontentout:
                        files_crypt = self.crypt_namefile(files)
                        print files+" is an application"
                        tar = tarfile.TarFile(path+"/"+files_crypt+".tar", 'w')
                        tar.add(path+"/"+files,files)
                        tar.close()
                        self.crypt_file(path+"/"+files_crypt+".tar",pathout+"/"+files_crypt+".gpg")
                        try:
                            os.remove(path+"/"+files_crypt+".tar")
                        except:
                            print "error removing tar"
                    else:
                        print files+" is an application already gppz"
                #If it is an gpg file
                elif files[-4:] == ".gpg":
                    print files+" is already gpged (1)"
                #If it is a folder
                elif os.path.isdir(path+"/"+files):
                    #print files+" is a directory"
                    if files not in foldercontentout:
                        files_crypt = self.crypt_namefile(files)
                        try:
                            os.mkdir(pathout+"/"+files_crypt)
                        except:
                            pass
                        self.crypt_folder_new(path+"/"+files,self.homefileout+"/"+files_crypt)
                    else:
                        self.crypt_folder_new(path+"/"+files,self.homefileout+"/"+foldercontentout[files])
                #If it is a folder
                else: 
                    if files in foldercontentout:
                        print files+" is already gpged (2)"
                    else:
                        print "Crypting: "+files
                        files_crypt = self.crypt_namefile(files)
                        self.crypt_file(path+"/"+files,pathout+"/"+files_crypt+".gpg")
                        
    def decrypt_folder_new(self,path, pathout):
        foldercontent = os.listdir(path)
        foldercontentout = os.listdir(pathout)
        for files_crypt in foldercontent:
            #If it is not an invisible folder
            if not files_crypt[0] == ".":
                if os.path.isdir(path+"/"+files_crypt):
                    files = self.decrypt_namefile(files_crypt)
                    try:
                        os.mkdir(pathout+"/"+files)
                    except:
                        pass
                    self.decrypt_folder_new(path+"/"+files_crypt, pathout+"/"+files)
                else:
                    files = self.decrypt_namefile(files_crypt[0:-4])
                    #If it is an application
                    if files[-4:] == ".app":
                        if files not in foldercontentout:
                            print "decrypting application "+files
                            self.decrypt_file(path+"/"+files_crypt,pathout+"/"+files+".tar")
                            tar = tarfile.TarFile(pathout+"/"+files+".tar", 'r')
                            tar.extractall(pathout)
                            tar.close()
                            try:
                                os.remove(pathout+"/"+files+".tar")
                            except:
                                print "error removing tar: "+pathout+"/"+files_crypt[0:-4]+".tar"
                        else:
                            print files +" already decrypted (2)"
                    #If it is an gpg file
                    elif files_crypt[-4:] == ".gpg":
                        if files not in foldercontentout:
                            print "decrypting "+files
                            self.decrypt_file(path+"/"+files_crypt,pathout+"/"+files)
                        else:
                            print files+" already decrypted (1)"
                    #If it is a folder
                    else: 
                        print "ERROR file unknown "+files
    
    def save_dico(self):
        test = open(self.homefileout+"/.save.json",'w')
        test.write(json.dumps(self.dico))
        test.close()
    
    def load_dico(self):
        self.dico = {}
        try:
            test = open(self.homefileout+"/.save.json",'r')
            self.dico = json.loads(test.readline())         
            test.close()
        except:
            pass
        
    
    def crypt_namefile(self,filename):
        filename_crypt = self.crypt_string(filename)
        filename_rand = self.gen_random_name()
        self.dico[filename_rand] = filename_crypt
        return filename_rand
    
    def decrypt_namefile(self,filename_rand):
        filename_crypt = self.dico[filename_rand]
        filename = self.decrypt_string(filename_crypt)
        return filename
        
    
    def gen_random_name(self):
        word = ""
        for i in range(7):
            word += random.choice(string.letters)
        while word in self.dico:
            word = ""
            for i in range(7):
                word += random.choice(string.letters)
        return word
    
    def CRYPT(self,folderin,folderout):
        self.homefile = folderin
        self.homefileout = folderout
        self.load_dico()
        self.crypt_folder_new(folderin,folderout)
        self.save_dico()
    
    def DECRYPT(self,folderin,folderout):
        self.homefileout = folderin
        self.homefileout3 = folderout
        self.load_dico()
        self.decrypt_folder_new(folderin,folderout)
        self.save_dico()
    
    def load_name_already_crypted(self,pathout):
        foldercontent = os.listdir(pathout)
        files_already_present = {}
        for files_crypt in foldercontent:
            #If it is not an invisible folder
            if not files_crypt[0] == ".":
                if os.path.isdir(pathout+"/"+files_crypt):
                    files_already_present[self.decrypt_namefile(files_crypt)] = files_crypt
                    tmp = self.load_name_already_crypted(pathout+"/"+files_crypt)
                    for value in tmp:
                        files_already_present[value] = tmp[value]
                else:
                    files_already_present[self.decrypt_namefile(files_crypt[0:-4])] = files_crypt[0:-4]
        return files_already_present
    
if __name__ == "__main__":
    
    #input_data = gpg.gen_key_input(name_email='johnleger@free.fr',passphrase='jlhdie')
    #key = gpg.gen_key(input_data)
    #print key
    try:
        #os.remove(homefile+"/.save.json")
        ""
    except:
        pass
    """
    self.load_dico()

    print "\nCRYPTING\n"
    self.crypt_folder_new(homefile,homefileout)
    print "\nDECRYPTING\n"
    self.decrypt_folder_new(homefileout,homefileout3)
    print "\nFIN\n"
    self.save_dico()
    """
    ddd = gpgj()
    print "change les paths ci dessous"
    ddd.CRYPT("in","out")
    #ddd.DECRYPT("/Users/john/Desktop/testgpgout","/Users/john/Desktop/testgpgoutverif")

