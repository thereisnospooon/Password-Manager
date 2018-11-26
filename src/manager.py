from Crypto.Cipher import AES
import hashlib
import csv
import os

PSWRD_FILE = "pswrd_file.csv"


class Manager:

    def __init__(self, file_path: str, key: str):
        self.key = key
        self.pswrd_file_path = file_path
        self.decrypter, self.encrypter = self.generate_encryptor()  # Does encryption and decryption

    def add_password(self, tag: str, username: str, password: str):
        """
        adds a password to the file
        :param tag: Tag of the password
        :param username: username
        :param password: password
        """
        if os.path.exists(self.pswrd_file_path):
            with open(self.pswrd_file_path, "a") as file:
                file_writer = csv.writer(file)
                username, password = self.buff_to_16bit(username, password)
                encrypted_pswrd = self.encrypter.encrypt(password)
                print("decrypt right after encrypt:")
                print(self.decrypter.decrypt(encrypted_pswrd))
                encrypted_username = self.encrypter.encrypt(username)
                file_writer.writerow(
                    [tag, encrypted_username, encrypted_pswrd])  # Todo: make impossible to add 2 tags with same name
        else:
            with open(self.pswrd_file_path, "w") as file:
                fields = ['tag', 'username', 'password']
                file_writer = csv.DictWriter(file, fields)
                file_writer.writeheader()
                username, password = self.buff_to_16bit(username, password)
                encrypted_pswrd = self.encrypter.encrypt(password)
                print("decrypt right after encrypt:")
                print(self.decrypter.decrypt(encrypted_pswrd))
                encrypted_username = self.encrypter.encrypt(username)
                file_writer.writerow({"tag": tag, "username": encrypted_username, "password": encrypted_pswrd})

    def update_password(self, tag: str, username: str, password: str):
        pass

    def get_password(self, tag: str, username: str = None):
        with open(self.pswrd_file_path, "r") as file:
            file_reader = csv.DictReader(file)
            for row in file_reader:
                if row["tag"] == tag or row["username"] == username:  # Assumes every account has a distinct username
                    out_username, out_password = self.buff_to_16bit(row["username"], row["password"])
                    print(self.decrypter.decrypt(out_username))
                    print(self.decrypter.decrypt(out_password))

        return None

    def generate_encryptor(self):
        """
        Generates the encryptor - decrypter object
        :return: the object used for encryption and decryption
        """
        self.key = hashlib.sha256(self.key.encode('utf-8')).digest()
        print(self.key)
        IV = 16 * '\x00'
        mode = AES.MODE_CBC
        return AES.new(self.key, mode, IV=IV), AES.new(self.key, mode, IV=IV)

    def buff_to_16bit(self, username, password):
        """
        Given 2 strings, checks if buff is needed
        :param username: first string
        :param password: second string
        :return: the strings buffed
        """
        if len(username) % 16 == 0:
            first_out = username
        else:
            first_out = self.buff_single_string(username)
        if len(password) % 16 == 0:
            second_out = password
        else:
            second_out = self.buff_single_string(password)
        return first_out, second_out

    def buff_single_string(self, string):
        """
        Given a string, buffs it
        :param string: The string to buff
        :return:
        """
        output = string
        while len(output) % 16 != 0:
            output += '~'
        return output

    def renewDecrypt(self):

        IV = 16 * '\x00'
        mode = AES.MODE_CBC
        self.decrypter, self.encrypter = AES.new(self.key, mode, IV=IV), AES.new(self.key, mode, IV=IV)
