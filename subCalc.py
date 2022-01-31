import sys
import random


def subnet_calc():
    try:
        print("\n")

        # IP tikrinimas
        while True:
            ip_address = input("Įveskite IP adresą: ")

            # Iskaidomas IP ir tikrinamas ar atitinka salygas.
            a = ip_address.split('.')
            # print(a)

            # Netinkami adresai kurie prasideda 0, 127, 224. Pirmas 169 ir antras 254 negalibuti kartu.
            # Trecias ir ketvirtas galimi skaiciai nuo 0 iki 255
            if (len(a) == 4) and (1 <= int(a[0]) <= 223) and (int(a[0]) != 127) and (int(a[0]) != 169 or int(a[1]) != 254) and (0 <= int(a[1]) <= 255 and 0 <= int(a[2]) <= 255 and 0 <= int(a[3]) <= 255):
                break

            else:
                print("\nIP adresas netinkamas, bandykite dar karta!\n")
                continue

        masks = [255, 254, 252, 248, 240, 224, 192, 128, 0]

        # Tikrinam subnet mask
        while True:
            subnet_mask = input("Iveskite subnet mask: ")
            b = subnet_mask.split('.')
            # Pirmas skaivius privalomas 255, kiti bet kurie is saraso masks.
            if (len(b) == 4) and (int(b[0]) == 255) and (int(b[1]) in masks) and (int(b[2]) in masks) and (int(b[3]) in masks) and (int(b[0]) >= int(b[1]) >= int(b[2]) >= int(b[3])):
                break

            else:
                print("\nNetinkamas subnet mask, bandykite dar karta!\n")
                continue

        mask_octets_padded = []
        mask_octets_decimal = subnet_mask.split('.')
        #print (mask_octets_decimal)

        for octet_index in range(0, len(mask_octets_decimal)):

            #print (bin(int(mask_octets_decimal[octet_index])))

            binary_octet = bin(int(mask_octets_decimal[octet_index])).split("b")[1]
            #print(binary_octet) #octet mask in binary

            if len(binary_octet) == 8:
                mask_octets_padded.append(binary_octet)

            elif len(binary_octet) < 8:     #jeigu truksta uzpildom 8bit
                binary_octet_padded = binary_octet.zfill(8)
                mask_octets_padded.append(binary_octet_padded)

        #print(mask_octets_padded)
        
        decimal_mask = "".join(mask_octets_padded)
        #print(decimal_mask)  # PVZ: 255.255.255.0 => 11111111111111111111111100000000

        #skaiciuojam hostu bitai maskese ir koks skaicius hostu ir subnetu
        no_of_zeros = decimal_mask.count("0")
        no_of_ones = 32 - no_of_zeros
        no_of_hosts = abs(2 ** no_of_zeros - 2)  # grazina teigiama mask /32

        #print(no_of_zeros)
        #print(no_of_ones)
        #print(no_of_hosts)

        #gaunamas wildcard mask
        wildcard_octets = []
        for w_octet in mask_octets_decimal:
            wild_octet = 255 - int(w_octet)
            wildcard_octets.append(str(wild_octet))

        #print(wildcard_octets)

        wildcard_mask = ".".join(wildcard_octets)
        #print(wildcard_mask)

        ip_octets_padded = []
        ip_octets_decimal = ip_address.split(".")

        for octet_index in range(0, len(ip_octets_decimal)):

            binary_octet = bin(int(ip_octets_decimal[octet_index])).split("b")[1]

            if len(binary_octet) < 8:
                binary_octet_padded = binary_octet.zfill(8)
                ip_octets_padded.append(binary_octet_padded)

            else:
                ip_octets_padded.append(binary_octet)

        #print(ip_octets_padded)
        binary_ip = "".join(ip_octets_padded)

        #print(binary_ip) #PVZ: 192.168.2.100 => 11000000101010000000001001100100

        #gauname tinklo adresa ir broudcast adresa is binary stringo auksciau
        network_address_binary = binary_ip[:(no_of_ones)] + "0" * no_of_zeros
        #print(network_address_binary)

        broadcast_address_binary = binary_ip[:(no_of_ones)] + "1" * no_of_zeros
        #print(broadcast_address_binary)

        net_ip_octets = []
        for octet in range(0, len(network_address_binary), 8):
            net_ip_octet = network_address_binary[octet:octet + 8]
            net_ip_octets.append(net_ip_octet)

        #print(net_ip_octets)

        net_ip_address = []
        for each_octet in net_ip_octets:
            net_ip_address.append(str(int(each_octet, 2)))

        #print(net_ip_address)

        network_address = ".".join(net_ip_address)
        #print(network_address)

        bst_ip_octets = []
        for octet in range(0, len(broadcast_address_binary), 8):
            bst_ip_octet = broadcast_address_binary[octet:octet + 8]
            bst_ip_octets.append(bst_ip_octet)

        #print(bst_ip_octets)

        bst_ip_address = []
        for each_octet in bst_ip_octets:
            bst_ip_address.append(str(int(each_octet, 2)))
        
        #print(bst_ip_address)

        broadcast_address = ".".join(bst_ip_address)

        #print(broadcast_address)

        #rezultatas pasirinkto ip/mask
        print("\n")
        print("Tinklo Adresas yra: %s" % network_address)
        print("Broadcast Adresas yra: %s" % broadcast_address)
        print("Skaicius galimu vartotoju per subnet: %s" % no_of_hosts)
        print("Wildcard mask: %s" % wildcard_mask)
        print("Mask bitais (Pool): %s" % no_of_ones)
        print("\n")

        #IP adresu generatorius pagal subnet
        while True:
            generate = input("Generuoti atsitiktinius IP adresus is subnet? (y/n)")

            if generate == "y":
                generated_ip = []

                #Gauti galimus IP adresus intervale tarp broadcast ir tinklo adreso
                for indexb, oct_bst in enumerate(bst_ip_address):
                    #print(indexb, oct_bst)
                    for indexn, oct_net in enumerate(net_ip_address):
                        #print(indexn, oct_net)
                        if indexb == indexn:
                            if oct_bst == oct_net:
                                #prideda identiska octa i generated_ip sarasa
                                generated_ip.append(oct_bst)
                            else:
                                #generuoja atsitiktini(us) skaiciu(s) is octet diapazono ir prideda i sarasa
                                generated_ip.append(str(random.randint(int(oct_net), int(oct_bst))))
                
                #Ip adresas sugeneruotas is subnet poolo
                #print(generated_ip)
                y_iaddr = ".".join(generated_ip)
                #print(y_iaddr)

                print ("Atsitiktinis IP adresas yra: %s" % y_iaddr)
                print("\n")
                continue

            else:
                print("Viso!\n")
                break


    except KeyboardInterrupt:
        print("\n\nProgram Aborted by user. Exiting...\n")
        sys.exit()


# Funkcijos isaukimas
subnet_calc()
