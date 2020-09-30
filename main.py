
import __init__;
import models


def main():
    audio = models.fetch_audio()
    command = models.recognition_witai(audio)
    if command == 'hey sexy':
        print("at You service master")
        models.text_to_speech('at You service master')
    else:
        print("say my name first")
        models.text_to_speech('say my name first')


if __name__ == '__main__':
    main()