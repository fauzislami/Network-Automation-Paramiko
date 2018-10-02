import paramiko
import time
from getpass import getpass
import sys
import os

try :
        print "=================================="
        print "Selamat Ngoprek Network Automation"
        print "==================================\n\n"

        #untuk memasukkan IP File yang berisi IP Address dari perangkat
        while True:
            try:
                    print "---Format IP Address---"
                    print "-----------------------"
                    print "---IP Address:Vendor---"
                    print "-----------------------"
                    input_file = raw_input("Masukkan IP File Anda : ")

                    #membaca file
                    r_input_file = open(input_file,"r").readlines()
                    break
            #jika IP File tidak dimasukkan
            except IOError:
                    print "IP File tidak ada! Silakan coba lagi!"
                    continue

        #memisahkan antara list IP Address dan list Vendor
        ip_list = []
        vendor_list = []

        for x in r_input_file:
            ip_list.append(x.split(";")[0]) #memasukkan IP Address ke dalam list dengan delimiter (;)
            vendor_list.append(x.split(';')[1].strip()) #memasukkan list vendor dan memakai fungsi strip () agar tidak ada whitespace

        #mengecek koneksi ke perangkat
        ok_ip_list = []
        ok_vendor_list = []
        print "Sedang mengecek koneksi . . . ."
        for index,ip in enumerate (ip_list): #mengurutkan IP Address dengan index diikuti dengan IP Address
            response = os.system("ping -c 3 {}".format(ip))

            if response == 0: #jika koneksi sedang UP
                print "\n\n{} is up\n\n".format(ip)
                ok_ip_list.append(ip) #menambahkan IP mana saja yang UP
                ok_vendor_list.append(vendor_list[index]) #hanya menambahkan elemen dari list vendor
            else: #jika koneksi sedang DOWN
                print "\n\n{} is down!\n\n".format(ip)


        #Memasukkan konfigurasi Cisco
        while True:
                try:
                    input_cisco_config = raw_input("Masukkan File Konfigurasi Cisco : ")

                    #membaca file Konfigurasi
                    r_input_cisco_config = open(input_cisco_config,"r").readlines()
                    break

                except IOError:
                    print "File konfigurasi tidak ada! Silakan coba lagi!"
                    continue

        #Konfigurasi konfigurasi MikroTik
        while True:
            try:
                input_mikrotik_config = raw_input("Masukkan File Konfigurasi MikroTik : ")

                #membaca file Konfigurasi
                r_input_mikrotik_config = open(input_mikrotik_config,"r").readlines()
                break

            except IOError:
                print "File konfigurasi tidak ada! Silakan coba lagi!"
                continue

        username = raw_input("Username : ") #meminta autentikasi username
        password = getpass()   #meminta autentikasi password

        print "Sedang melakukan konfigurasi, mohon sabar menunggu . . . ."
        for index,ip in enumerate(ok_ip_list):
            ssh_client = paramiko.SSHClient() #membuat variabel untuk ssh ssh_client
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #agar bisa koneksi ke perangkat lalu menyimpan host key nya
            ssh_client.connect (hostname=ip,username=username,password=password) #memasukkan hostname, username dan password untuk koneksi ssh
            print "Berhasil masuk ke {}".format(ip)

            #jika yang dikonfigurasi adalah Cisco
            if ok_vendor_list[index].lower() == "cisco":
                    conn = ssh_client.invoke_shell() #memanggil shell interaktif

                    for config in r_input_cisco_config:
                        conn.send(config +"\n") #untuk memasukkan baris per baris konfigurasi ke dalam invoke_shell
                        time.sleep(1) #delay 1 detik
                    print "Konfigurasi Berhasil Untuk {}\n".format(ip)

            #jika yang dikonfigurasi adalah input_mikrotik_config
        else :
                for config in r_input_mikrotik_config:
                    ssh_client.exec_command(config) #eksekusi command
                    time.sleep(1)
                print "Konfigurasi Berhasil Untuk {}\n".format(ip)
except KeyboardInterrupt:
    print "\n\nProgram dibatalkan\n\n"
    sys.exit()
