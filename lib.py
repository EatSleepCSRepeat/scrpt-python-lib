import urllib.request as urllib_rq
import os

variables = {}

def execute_scrpt(cmd, variables=variables):
    try:
        if cmd.startswith("stdout.display_text "):
            arg = cmd[20:].strip()
            if arg.startswith('disvar='):
                variable_name = arg[7:].strip()
                if variable_name in variables:
                    print(variables[variable_name])
                else:
                    print("Variable not found")
            else:
                print(arg)

        elif cmd.startswith("std.help ") or cmd == "std.help":
            print("Available functions:")
            print("\033[93mscrpt.root.exit\033[0m \033[90m--\033[0m \033[32mExits Scrpt\033[0m")
            print("\033[93mstdout.display_text\033[0m \033[90m--\033[0m \033[32mPrints out text to the console (or stdout)\033[0m")
            print("\033[93m/define\033[0m \033[90m--\033[0m \033[32mDefines a variable (syntax: /define [integer|string] [name] [value])\033[0m")
            print("\033[93mpacwit [option] [package]\033[0m \033[90m--\033[0m \033[32mPackage manager for Scrpt\033[0m")

        elif cmd.startswith("scrpt.root.exit ") or cmd == "scrpt.root.exit":
            print("Exiting...")
            print("Exited main scrpt process at code 0 with reason 'User exited the command prompt'")
            return  # Use return instead of break

        elif cmd.startswith("/define "):
            split_v = cmd.split(maxsplit=3)
            if len(split_v) != 4:
                print("at line 1 (temp.spt)")
                print("\033[31mInvalid syntax for /define. Use /define [integer|string] [name] [value]\033[0m")
                return  # Use return instead of continue

            var_type = split_v[1]
            var_name = split_v[2]
            var_value = split_v[3]

            if var_type == 'integer':
                variables[var_name] = int(var_value)
            elif var_type == 'string':
                variables[var_name] = var_value
            else:
                print("Unsupported variable type. Use 'integer' or 'string'.")

        elif cmd.startswith("pacwit "):
            split_cmd = cmd.split()
            if len(split_cmd) < 3:
                print("Invalid pacwit command. Use pacwit [-i|-wsl -i|-list-pkg] [package]")
                return  # Use return instead of continue
            
            option = split_cmd[1]
            package = split_cmd[2]

            if option == '-i':
                if package == 'rustup':
                    file = urllib_rq.urlretrieve('https://win.rustup.rs', 'rustup.exe')
                    if file:
                        print("\033[90mpackage-wither\033[0m \033[32msuccess\033[0m\nSuccessfully installed \033[93mrustup\033[0m!")
                elif package == 'git-windows':
                    file = urllib_rq.urlretrieve('https://github.com/git-for-windows/git/releases/download/v2.33.1.windows.1/Git-2.33.1-64-bit.exe', 'git.exe')
                    if file:
                        print("\033[90mpackage-wither\033[0m \033[32msuccess\033[0m\nSuccessfully installed \033[93mGit for Windows\033[0m!")
                else:
                    print(f"Unknown package '{package}' for installation.")
            
            elif option == '-wsl':
                if len(split_cmd) < 4 or split_cmd[3] not in ['rustup']:
                    print("Invalid -wsl command. Use pacwit -wsl -i [package]")
                    return  # Use return instead of continue
                
                if split_cmd[3] == 'rustup':
                    res = os.system("wsl curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh")
                    if res != 0:
                        print("\033[90mpackage-wither\033[0m \033[31merror\033[0m\nFailed to install \033[93mrustup\033[0m in WSL.")
                else:
                    print(f"Unknown package '{package}' for WSL installation.")

            elif option == '-list-pkg':
                print("Available packages: \nGit for Windows\nRust\n\n(BETA V1.0)")
            else:
                print(f"Unknown option '{option}' for pacwit.")
        
        elif cmd.startswith("stdout "):
            spl = cmd.split()
            if spl[1] == 'display-cw-file':
                mod_file = __file__.replace(".py", ".exe")
                print(mod_file)
        else:
            print(f"Command '{cmd}' not recognized. Type std.help for a list of commands.")
    except Exception as e:
        print(f"Error: {e}")

execute_scrpt("stdout.display_text \"Hello, world!\"")
