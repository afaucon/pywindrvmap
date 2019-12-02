import json
import logging
import os
import os.path
import pathlib
import subprocess

from .__info__ import __package_name__, __version__


config_file_name = '.' + __package_name__ + '-' + __version__ + '-config.json'


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
        self.is_physical = False

        self._netuse = None
        self._subst = None

    def network_shortcut(self):
        return self._netuse

    def local_shortcut(self):
        return self._subst
    
    def is_available(self):
        """
        [summary]
        
        :return: [description]
        :rtype: [type]
        """
        return not self.is_used()

    def is_used(self):
        """
        [summary]
        
        :return: [description]
        :rtype: [type]
        """
        return self.is_physical or self.is_shortcut()
    
    def is_shortcut(self):
        """
        [summary]
        
        :return: [description]
        :rtype: [type]
        """
        return self._netuse is not None or self._subst is not None

    def get_shortcut(self):
        """
        [summary]
        
        :return: [description]
        :rtype: [type]
        """
        if self._netuse:
            return self._netuse
        elif self._subst:
            return self._subst
        else:
            return None

    def __str__(self, kind=DISPLAY_ALL): 
        """
        For call to str(). Allows to prints readable form of the object for end users.
        
        :return: [description]
        :rtype: [type]
        """
        retstring = ""
        if self.is_physical:
            retstring = retstring + '{}: physical drive\n'.format(self.letter)
        elif self._netuse is not None and self._subst is not None:
            if kind == DriveInfo.DISPLAY_ALL:
                retstring = retstring + '{} --> {}\n'.format(self.letter, self._netuse)
                retstring = retstring + '  --> {}\n'.format(self._subst)
            if kind == DriveInfo.DISPLAY_NETUSE_ONLY:
                retstring = retstring + '{} --> {}\n'.format(self.letter, self._netuse)
            if kind == DriveInfo.DISPLAY_SUBST_ONLY:
                retstring = retstring + '{} --> {}\n'.format(self.letter, self._subst)
        elif self._netuse is not None:
            retstring = retstring + '{} --> {}\n'.format(self.letter, self._netuse)
        elif self._subst is not None:
            retstring = retstring + '{} --> {}\n'.format(self.letter, self._subst)
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
PHYSICAL = 3
SHORTCUT = 4
NETWORK_SHORTCUT = 5
LOCAL_SHORTCUT = 6

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
                    drives_info[drive_letter]._netuse = path
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
                    drives_info[drive_letter]._subst = path
                else:
                    # Something went wrong
                    raise Exception # TODO: Improve this statement

        # Detecting physical drives
        for drive_letter in Drives.drive_letters:
            if drives_info[drive_letter]._netuse is None and drives_info[drive_letter]._subst is None:
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

    def get(self, kind=ALL):
        """
        [summary]
        
        :return: [description]
        :rtype: [type]
        """
        retval = []
        for drive in self.drives_iter():
            if kind == ALL:
                retval.append(drive)
            if kind == USED and drive.is_used():
                retval.append(drive)
            if kind == AVAILABLE and drive.is_available():
                retval.append(drive)
            if kind == PHYSICAL and drive.is_physical:
                retval.append(drive)
            if kind == SHORTCUT and drive.is_shortcut():
                retval.append(drive)
            if kind == NETWORK_SHORTCUT and drive.network_shortcut():
                retval.append(drive)
            if kind == LOCAL_SHORTCUT and drive.local_shortcut():
                retval.append(drive)
        return retval

    def letters(self, kind=ALL):
        """
        [summary]
        
        :return: [description]
        :rtype: [type]
        """
        return [drive.letter for drive in self.get(kind)]

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
        if kind == ALL or kind == USED or kind == SHORTCUT:
            retstring = ""
            for drive in self.get(kind):
                retstring = retstring + drive.string_representation(DriveInfo.DISPLAY_ALL) + '\n'

        if kind == NETWORK_SHORTCUT or kind == LOCAL_SHORTCUT:
            retstring = ""
            for drive in self.get(kind):
                if kind == NETWORK_SHORTCUT:
                    retstring = retstring + drive.string_representation(DriveInfo.DISPLAY_NETUSE_ONLY) + '\n'
                if kind == LOCAL_SHORTCUT:
                    retstring = retstring + drive.string_representation(DriveInfo.DISPLAY_NETUSE_ONLY) + '\n'
            
        if kind == AVAILABLE or kind == PHYSICAL:
            for drive in self.get(kind):
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

class ConfigException(Exception):
    pass

class Config:
    
    def __init__(self):
        """
        Constructor of the class
        
        :raises ConfigException: If there is a json format error in the configuration file or if the configuration file is not a json object.
        """
        self.config_path = pathlib.Path(os.environ['HOMEDRIVE']) / pathlib.Path(os.environ['HOMEPATH']) / config_file_name
        if not self.config_path.is_file():
            self.mapping = {}
        else:
            try:
                with open(self.config_path, 'r') as f:
                    self.mapping = json.load(f)
            except json.decoder.JSONDecodeError as e:
                logging.error('Configuration json format error (line {}, column {}): {}'.format(str(e.lineno), str(e.colno), self.config_path))
                raise ConfigException('Configuration json format error (line {}, column {}): {}'.format(str(e.lineno), str(e.colno), self.config_path))
            else:
                # Validate the configuration
                if not isinstance(self.mapping, dict):
                    raise ConfigException('Configuration error (not an object): {}'.format(self.config_path))

                # Validate the content of the configuration
                # => No more validation here:
                # => Error will be raised later, when applying the configuration

                # for item in self.mapping:
                #     if not item.isalpha():
                #         raise DrivesMappingConfigException('Configuration error ({}): {}'.format(str(item), self.config_path))

                #     path = Path(self.mapping[item])
                #     if not path.is_dir():
                #         raise DrivesMappingConfigException('Configuration error ({}): {}'.format(str(item), self.config_path))
                #     else:
                #         self.mapping[item] = path

    def __str__(self):
        """
        For call to str(). Allows to prints readable form of the object for end users.
        
        :return: [description]
        :rtype: [type]
        """
        retstring = ""
        for drive_letter in self.mapping:
            retstring = retstring + '{} --> {}\n'.format(drive_letter, self.mapping[drive_letter])
        return retstring[:-1]  # Removing the last character that is a '\n'

    def add(self, drive_letter, destination):
        """
        [summary]
        
        :param drive_letter: [description]
        :type drive_letter: [type]
        :param destination: [description]
        :type destination: [type]
        :return: [description]
        :rtype: [type]
        """
        config_to_write  = self.mapping.copy()
        config_to_write[drive_letter] = destination

        config_file_existed = self.config_path.is_file()

        if self.mapping == config_to_write:
            status = 'Success'
            message = 'Configuration updated'
        else:
            try:
                with open(self.config_path, 'w') as f:
                    json.dump(config_to_write, f, sort_keys=True, indent=4)
            except:
                status = 'Failed'
                message = 'Impossible to write in configuration file: {}'.format(self.config_path)
            else:
                recovered_config = {}
                try:
                    with open(self.config_path, 'r') as f:
                        recovered_config = json.load(f)
                except:
                    status = 'Failed'
                    message = 'Impossible to read configuration file after update: {}'.format(self.config_path)
                else:
                    if recovered_config != config_to_write:
                        status = 'Failed'
                        message = 'Configuration file update failed: {}'.format(self.config_path)
                    else:
                        self.mapping = recovered_config

                        if not config_file_existed:
                            logging.info('Configuration file created: {}'.format(self.config_path))
                        
                        status = 'Success'
                        message = 'Configuration updated'

        return status, message

    def remove(self, drive_letter):
        """
        [summary]
        
        :param drive_letter: [description]
        :type drive_letter: [type]
        :return: [description]
        :rtype: [type]
        """
        config_to_write  = self.mapping.copy()
        config_to_write.pop(drive_letter, None)

        if self.mapping == config_to_write:
            status = 'Success'
            message = 'Configuration updated'
        else:
            try:
                with open(self.config_path, 'w') as f:
                    json.dump(config_to_write, f, sort_keys=True, indent=4)
            except:
                status = 'Failed'
                message = 'Impossible to write in configuration file: {}'.format(self.config_path)
            else:
                recovered_config = {}
                try:
                    with open(self.config_path, 'r') as f:
                        recovered_config = json.load(f)
                except:
                    status = 'Failed'
                    message = 'Impossible to read configuration file after update: {}'.format(self.config_path)
                else:
                    if recovered_config != config_to_write:
                        status = 'Failed'
                        message = 'Configuration file update failed: {}'.format(self.config_path)
                    else:
                        self.mapping = recovered_config

                        if self.mapping == {}:
                            logging.info('Configuration file deleted: {}'.format(self.config_path))
                            os.remove(self.config_path)

                        status = 'Success'
                        message = 'Configuration updated'

        return status, message