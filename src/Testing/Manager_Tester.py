import manager


def write():
    psd_manager = manager.Manager("pswrd_file.csv", "helloworld")
    psd_manager.add_password("stam", "guy", "1234")


def read():
    psd_manager = manager.Manager("pswrd_file.csv", "helloworld")
    psd_manager.get_password("stam")


if __name__ == '__main__':
    write()
    read()
