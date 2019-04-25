import threading


def main():
    print("Begin")
    timer = threading.Timer(10.0, failure)
    timer.start()
    user_input = input("Type this sentence in 10 seconds")
    while user_input != "Type this sentence in 10 seconds":
        print("Oof")
        user_input = input("Type this sentence in 10 seconds")
    timer.cancel()
    print("You did it! Good for you!")


def failure():
    print("Whomp whomp")
    quit()


if __name__ == '__main__':
    main()
