import subprocess
import os.path
import logging


# TODO: For subst,  use windll.kernel32.DefineDosDeviceW
# TODO: For netuse, use win32wnet from pywin32

r"""
Example of "net use" command output
-----------------------------------

Les nouvelles connexions seront mémorisées.


État         Local     Distant                   Réseau

-------------------------------------------------------------------------------
            A:        \\view                    ClearCase Dynamic Views
Déconnectée  H:        \\SFCRL10003\COMMUN       Microsoft Windows Network
            M:        \\view\app_evc            ClearCase Dynamic Views
            N:        \\view\afaucon_01_vw      ClearCase Dynamic Views
Non disponib O:        \\view\afaucon_02_vw      ClearCase Dynamic Views
Déconnectée  P:        \\sfcrl10002.next.loc\Preston_NT
                                                Microsoft Windows Network
Déconnectée  S:        \\sfcrl10002.next.loc\PL  Microsoft Windows Network
Déconnectée  T:        \\sfcrl10002.next.loc\AQ  Microsoft Windows Network
Déconnectée  U:        \\SFCRL10003\COMMUN       Microsoft Windows Network
Déconnectée  V:        \\SFCRL10003\EBE          Microsoft Windows Network
Déconnectée  W:        \\sfcrl10003.next.loc\IND Microsoft Windows Network
Déconnectée  X:        \\SFCRL10003\BSI          Microsoft Windows Network
Déconnectée  Y:        \\sfcrl10003.next.loc\AFS Microsoft Windows Network
Déconnectée  Z:        \\sfcrl10002.next.loc\PERS\afaucon
                                                Microsoft Windows Network
Déconnectée            \\cwcrl196tw\C            Microsoft Windows Network
                    \\view\afaucon_02_vw      ClearCase Dynamic Views
                    \\view\cc_adm_view        ClearCase Dynamic Views
                    \\view\livraison_agl      ClearCase Dynamic Views
La commande s’est terminée correctement.

Example of "subst" command output
---------------------------------

E:\: => C:\A\...
F:\: => C:\B\...
...

"""


def _program_to_use(path):
    if path.startswith('\\\\'):
        return 'netuse'
    elif path[1:3] == ':\\':
        return 'subst'
    else:
        raise Exception  # TODO: Improve the exception here

def _call(command_line):
    """
    [summary]
    
    :param command_line: [description]
    :type command_line: [type]
    :return: [description]
    :rtype: [type]
    """
    completed_process = subprocess.run(command_line.split(' '), stdout=subprocess.PIPE)
    output = completed_process.stdout.decode(('cp850').encode('latin-1','replace').decode('latin-1'))
    # print(output)
    return output
    

# Internal functions
# ==================

class CommandLine():
    """
    [summary]
    """

    def __init__(self, method):
        """
        [summary]
        """
        self.method = method

        if method != 'netuse' and method != 'subst':
            raise Exception # TODO: Improve this statement

    def list(self):
        """
        [summary]
        
        :return: [description]
        :rtype: [type]
        """
        if self.method == 'netuse':
            command_line = 'net use'
        if self.method == 'subst':
            command_line = 'subst'
        return _call(command_line)

    def add(self, dl, path):
        """
        [summary]
        
        :param dl: [description]
        :type dl: [type]
        :param path: [description]
        :type path: [type]
        :return: [description]
        :rtype: [type]
        """
        if self.method == 'netuse':
            command_line = 'net use ' + dl + ': ' + path
        if self.method == 'subst':
            command_line = 'subst ' + dl + ': ' + path
        return _call(command_line)

    def remove(self, dl):
        """
        [summary]
        
        :param dl: [description]
        :type dl: [type]
        :return: [description]
        :rtype: [type]
        """
        if self.method == 'netuse':
            command_line = 'net use ' + dl + ': /DELETE'
        if self.method == 'subst':
            command_line = 'subst ' + dl + ': /DELETE'
        return _call(command_line)

class DriveInfo:
    """
    [summary]
    """

    def __init__(self, letter, netuse=None, subst=None, is_physical=False):
        """
        Object constructor
        """
        self.letter = letter
        self.netuse = netuse
        self.subst = subst
        self.is_physical = is_physical

    def is_used(self):
        """
        [summary]
        
        :return: [description]
        :rtype: [type]
        """
        return self.is_physical or self.netuse is not None or self.subst is not None
    
    def is_available(self):
        """
        [summary]
        
        :return: [description]
        :rtype: [type]
        """
        return not self.is_used()

    def __str__(self): 
        """
        For call to str(). Allows to prints readable form of the object for end users.
        
        :return: [description]
        :rtype: [type]
        """
        retstring = ""
        if self.is_physical:
            retstring = retstring + '{}: physical drive\n'.format(self.letter)
        elif self.netuse is not None and self.subst is not None:
            retstring = retstring + '{}: {}\n'.format(self.letter, self.netuse)
            retstring = retstring + '   {}\n'.format(self.subst)
        elif self.netuse is not None:
            retstring = retstring + '{}: {}\n'.format(self.letter, self.netuse)
        elif self.subst is not None:
            retstring = retstring + '{}: {}\n'.format(self.letter, self.subst)
        else:
            retstring = retstring + '{}: unused\n'.format(self.letter)
        return retstring[:-1]  # Removing the last character that is a '\n'

# Public interface
# ================

ALL = 0
USED_ONLY = 1
AVAILABLE_ONLY = 2
USED_BY_NETUSE_ONLY = 3
USED_BY_SUBST_ONLY = 4
PHYSICAL_ONLY = 5

class Drives:
    """
    [summary]
    """

    drive_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def __init__(self, kind=ALL):
        """
        Object constructor
        """

        drives_info = {}
        for drive_letter in Drives.drive_letters:
            drives_info.update({'{}'.format(drive_letter) : DriveInfo(drive_letter)})

        # Netuse part
        output = CommandLine('netuse').list()
        output_lines = output.split("\n")

        for output_line in output_lines:
            x = output_line.split(":")
            if len(x) == 2:
                left_part = x[0].strip()
                right_part = x[1].strip()

                drive_letter = left_part[-1].upper()
                path         = right_part.split(' ')[0]

                if drive_letter.isalpha() and path.startswith(r'\\'):
                    drives_info[drive_letter].netuse = path
                else:
                    # Something went wrong
                    raise Exception # TODO: Improve this statement

        # Subst part
        output = CommandLine('subst').list()
        output_lines = output.split("\n")

        for output_line in output_lines:
            x = output_line.split(" => ")
            if len(x) == 2:
                left_part = x[0].strip()
                right_part = x[1].strip()

                drive_letter = left_part[0].upper()
                path         = right_part

                if drive_letter.isalpha() and os.path.exists(path):
                    drives_info[drive_letter].subst = path
                else:
                    # Something went wrong
                    raise Exception # TODO: Improve this statement

        # Detecting physical drives
        for drive_letter in Drives.drive_letters:
            if drives_info[drive_letter].netuse is None and drives_info[drive_letter].subst is None:
                if os.path.exists(drive_letter + ':'):
                    drives_info[drive_letter].is_physical = True
                else:
                    drives_info[drive_letter].is_physical = False

        # Create the attributes of the object
        for drive_letter in drives_info:
            drive = drives_info[drive_letter]
            if kind == ALL:
                self.__dict__[drive_letter] = drive
            if kind == USED_ONLY and drive.is_used():
                self.__dict__[drive_letter] = drive
            if kind == AVAILABLE_ONLY and drive.is_available():
                self.__dict__[drive_letter] = drive
            if kind == USED_BY_NETUSE_ONLY and drive.netuse:
                self.__dict__[drive_letter] = drive
            if kind == USED_BY_SUBST_ONLY and drive.subst:
                self.__dict__[drive_letter] = drive
            if kind == PHYSICAL_ONLY and drive.is_physical:
                self.__dict__[drive_letter] = drive

    def drive(self, drive_letter):
        """
        [summary]
        
        :param drive_letter: [description]
        :type drive_letter: [type]
        :return: [description]
        :rtype: [type]
        """
        return getattr(self, drive_letter.upper())

    def drives_iter(self):
        """
        [summary]
        
        :yield: [description]
        :rtype: [type]
        """
        for drive_letter in self.__dict__.keys():
            yield self.drive(drive_letter)

    def __str__(self):
        """
        For call to str(). Allows to prints readable form of the object for end users.
        
        :return: [description]
        :rtype: [type]
        """
        retstring = ""
        for drive in self.drives_iter():
            retstring = retstring + str(drive) + '\n'
        return retstring[:-1]  # Removing the last character that is a '\n'
                
def add(drive_letter, path):
    """
    Description to write
    """
    drive = Drives().drive(drive_letter)
    logging.debug('BEFORE --> ' + str(drive))

    if drive.is_available():
        
        program = _program_to_use(path)
        _ = CommandLine(program).add(drive_letter, path)

        drive = Drives().drive(drive_letter)
        logging.debug('AFTER --> ' + str(drive))

        if drive.is_used():
            status = 'Success'
            message = '{} drive successfully added'.format(drive_letter)
        else:
            status = 'Failed'
            message = 'Impossible to add {} drive'
    else:
        status = 'Failed'
        message = '{} drive already used. Adding impossible'.format(drive_letter)

    return status, message

def remove(drive_letter):
    """
    Description to write
    """
    drive = Drives().drive(drive_letter)
    logging.debug('BEFORE --> ' + str(drive))

    if drive.is_used():

        _ = CommandLine('netuse').remove(drive_letter)
        _ = CommandLine('subst').remove(drive_letter)

        drive = Drives().drive(drive_letter)
        logging.debug('AFTER --> ' + str(drive))

        if drive.is_available():
            status = 'Success'
            message = '{} drive successfully removed'.format(drive_letter)
        else:
            status = 'Failed'
            message = 'Impossible to remove {} drive'
    else:
        status = 'Failed'
        message = '{} drive not used. Removing impossible'.format(drive_letter)

    return status, message