import subprocess
import os.path
import logging


# TODO: For subst,  use windll.kernel32.DefineDosDeviceW
# TODO: For netuse, use win32wnet from pywin32

def _program_to_use(path):
    if path.startswith('\\\\'):
        return 'net use'
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
    completed_process = subprocess.run(command_line.split(' '), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = completed_process.stdout.decode(('cp850').encode('latin-1','replace').decode('latin-1'))
    #print(output)
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

        if method != 'net use' and method != 'subst':
            raise Exception # TODO: Improve this statement

    def list(self):
        """
        [summary]
        
        :return: [description]
        :rtype: [type]
        """
        if self.method == 'net use':
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
        if self.method == 'net use':
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
        if self.method == 'net use':
            command_line = 'net use ' + dl + ': /DELETE'
        if self.method == 'subst':
            command_line = 'subst ' + dl + ': /D'
        return _call(command_line)

class DriveInfo:
    """
    [summary]
    """
    DISPLAY_ALL = 0
    DISPLAY_NETUSE_ONLY = 1
    DISPLAY_SUBST_ONLY = 2

    def __init__(self, letter):
        """
        Object constructor
        """
        self.letter = letter
        self.netuse = None
        self.subst = None
        self.is_physical = False

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

    def __str__(self, kind=DISPLAY_ALL): 
        """
        For call to str(). Allows to prints readable form of the object for end users.
        
        :return: [description]
        :rtype: [type]
        """
        retstring = ""
        if self.is_physical:
            retstring = retstring + '{}: physical drive\n'.format(self.letter)
        elif self.netuse is not None and self.subst is not None:
            if kind == DriveInfo.DISPLAY_ALL:
                retstring = retstring + '{} --> {}\n'.format(self.letter, self.netuse)
                retstring = retstring + '  --> {}\n'.format(self.subst)
            if kind == DriveInfo.DISPLAY_NETUSE_ONLY:
                retstring = retstring + '{} --> {}\n'.format(self.letter, self.netuse)
            if kind == DriveInfo.DISPLAY_SUBST_ONLY:
                retstring = retstring + '{} --> {}\n'.format(self.letter, self.subst)
        elif self.netuse is not None:
            retstring = retstring + '{} --> {}\n'.format(self.letter, self.netuse)
        elif self.subst is not None:
            retstring = retstring + '{} --> {}\n'.format(self.letter, self.subst)
        else:
            retstring = retstring + '{}: unused\n'.format(self.letter)
        return retstring[:-1]  # Removing the last character that is a '\n'

    def string_representation(self, kind):
        """
        [summary]
        
        :param kind: [description]
        :type kind: [type]
        :return: [description]
        :rtype: [type]
        """
        return self.__str__(kind)


# Public interface
# ================

ALL = 0
USED = 1
AVAILABLE = 2
NETWORK = 3
LOCAL = 4
PHYSICAL = 5

class Drives:
    """
    [summary]
    """

    drive_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def __init__(self):
        """
        Object constructor
        """
        self.update()
    
    def update(self):
        """
        [summary]
        
        :raises Exception: [description]
        :raises Exception: [description]
        """
        drives_info = {}
        for drive_letter in Drives.drive_letters:
            drives_info.update({'{}'.format(drive_letter) : DriveInfo(drive_letter)})

        # Netuse part
        output = CommandLine('net use').list()
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
            self.__dict__[drive_letter] = drive

    def drives_iter(self):
        """
        [summary]
        
        :yield: [description]
        :rtype: [type]
        """
        for drive_letter in self.__dict__.keys():
            yield self.drive(drive_letter)

    def drive(self, drive_letter):
        """
        [summary]
        
        :param drive_letter: [description]
        :type drive_letter: [type]
        :return: [description]
        :rtype: [type]
        """
        return getattr(self, drive_letter.upper())

    def letters(self, kind=ALL):
        """
        [summary]
        
        :return: [description]
        :rtype: [type]
        """
        retval = []
        for drive in self.drives_iter():
            if kind == ALL:
                retval.append(drive.letter)
            if kind == USED and drive.is_used():
                retval.append(drive.letter)
            if kind == AVAILABLE and drive.is_available():
                retval.append(drive.letter)
            if kind == NETWORK and drive.netuse:
                retval.append(drive.letter)
            if kind == LOCAL and drive.subst:
                retval.append(drive.letter)
            if kind == PHYSICAL and drive.is_physical:
                retval.append(drive.letter)
        return retval

    def __str__(self, kind=None):
        """
        For call to str(). Allows to prints readable form of the object for end users.
        
        :param kind: [description], defaults to None
        :type kind: [type], optional
        :return: [description]
        :rtype: [type]
        """
        if kind is None:
            kind = ALL

        retstring = ""
        if kind == ALL or kind == USED:
            retstring = ""
            for drive in self.drives_iter():
                if drive.letter in self.letters(kind):
                    retstring = retstring + drive.string_representation(DriveInfo.DISPLAY_ALL) + '\n'

        if kind == NETWORK or kind == LOCAL:
            retstring = ""
            for drive in self.drives_iter():
                if drive.letter in self.letters(kind):
                    if kind == NETWORK:
                        retstring = retstring + drive.string_representation(DriveInfo.DISPLAY_NETUSE_ONLY) + '\n'
                    if kind == LOCAL:
                        retstring = retstring + drive.string_representation(DriveInfo.DISPLAY_NETUSE_ONLY) + '\n'
            
        if kind == AVAILABLE or kind == PHYSICAL:
            for drive in self.drives_iter():
                if drive.letter in self.letters(kind):
                    retstring = retstring + drive.letter + '\n'
        return retstring[:-1]  # Removing the last character that is a '\n'

    def string_representation(self, kind):
        """
        [summary]
        
        :param kind: [description]
        :type kind: [type]
        :return: [description]
        :rtype: [type]
        """
        return self.__str__(kind)
    
    def add(self, drive_letter, path):
        """
        [summary]
        
        :param drive_letter: [description]
        :type drive_letter: [type]
        :param path: [description]
        :type path: [type]
        :return: [description]
        :rtype: [type]
        """
        drive = self.drive(drive_letter)
        logging.debug('BEFORE --> ' + str(drive))

        if drive.is_available():
            
            program = _program_to_use(path)
            _ = CommandLine(program).add(drive_letter, path)
            self.update()

            drive = self.drive(drive_letter)
            logging.debug('AFTER --> ' + str(drive))

            if drive.is_used():
                status = 'Success'
                message = '{} drive successfully added'.format(drive_letter)
            else:
                status = 'Failed'
                message = 'Impossible to add {} drive'.format(drive_letter)
        else:
            status = 'Failed'
            message = '{} drive already used. Adding impossible'.format(drive_letter)

        return status, message

    def remove(self, drive_letter):
        """
        Description to write
        """
        drive = self.drive(drive_letter)
        logging.debug('BEFORE --> ' + str(drive))

        if drive.is_used():

            _ = CommandLine('net use').remove(drive_letter)
            _ = CommandLine('subst').remove(drive_letter)
            self.update()

            drive = self.drive(drive_letter)
            logging.debug('AFTER --> ' + str(drive))

            if drive.is_available():
                status = 'Success'
                message = '{} drive successfully removed'.format(drive_letter)
            else:
                status = 'Failed'
                message = 'Impossible to remove {} drive'.format(drive_letter)
        else:
            status = 'Failed'
            message = '{} drive not used. Removing impossible'.format(drive_letter)

        return status, message