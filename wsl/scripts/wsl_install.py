import sys, os, traceback, types
 
def isUserAdmin():
    if os.name == 'nt':
        import ctypes
        # WARNING: requires Windows XP SP2 or higher!
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            traceback.print_exc()
            print("Admin check failed, assuming not an admin.")
            return False
    else:
        raise(RuntimeError, "Unsupported operating system for this module: %s" % (os.name,))
   
def runAsAdmin(cmdLine=None, wait=True):
 
    if os.name != 'nt':
        raise(RuntimeError, "This function is only implemented on Windows.")
   
    import win32api, win32con, win32event, win32process
    from win32com.shell.shell import ShellExecuteEx
    from win32com.shell import shellcon
   
    python_exe = sys.executable
 
    if cmdLine is None:
        cmdLine = [python_exe] + sys.argv
    elif type(cmdLine) != list:
        raise ValueError("cmdLine is not a sequence.")
    cmd = '"%s"' % (cmdLine[0],)
    # XXX TODO: isn't there a function or something we can call to massage command line params?
    params = " ".join(['"%s"' % (x,) for x in cmdLine[1:]])
    cmdDir = ''
    showCmd = win32con.SW_SHOWNORMAL
    #showCmd = win32con.SW_HIDE
    lpVerb = 'runas'  # causes UAC elevation prompt.
   
    # print "Running", cmd, params
 
    # ShellExecute() doesn't seem to allow us to fetch the PID or handle
    # of the process, so we can't get anything useful from it. Therefore
    # the more complex ShellExecuteEx() must be used.
 
    # procHandle = win32api.ShellExecute(0, lpVerb, cmd, params, cmdDir, showCmd)
 
    procInfo = ShellExecuteEx(nShow=showCmd,
                              fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
                              lpVerb=lpVerb,
                              lpFile=cmd,
                              lpParameters=params)
 
    if wait:
        procHandle = procInfo['hProcess']    
        obj = win32event.WaitForSingleObject(procHandle, win32event.INFINITE)
        rc = win32process.GetExitCodeProcess(procHandle)
        # print "Process handle %s returned code %s" % (procHandle, rc)
    else:
        rc = None
 
    return rc

def enableWindowsFeature(feature):
    return runAsAdmin([
        'dism.exe',
        '/online', 
        '/enable-feature', 
        f'/featurename:{feature}',
        '/all',
        '/norestart'
    ])

ret1 = enableWindowsFeature('Microsoft-Windows-Subsystem-Linux')
# Error code 3010 - The requested operation is successful. Changes will not be effective until the system is rebooted. 
if ret1 == 3010:
    print("Reboot required")
elif ret1 != 0:
    print(f"Failed to enable WSL subsystem for Windows. DISM exit code: {ret1}")
    exit(1)

ret2 = enableWindowsFeature('VirtualMachinePlatform')
# Error code 3010 - The requested operation is successful. Changes will not be effective until the system is rebooted. 
if ret2 == 3010:
    print("Reboot required")
elif ret2 != 0:
    print(f"Failed to enable VirtualMachinePlatform on Windows. DISM exit code: {ret2}")
    exit(1)

if ret1 == 3010 or ret2 == 3010:
    print("Please reboot and start script again.")
    exit(1)

