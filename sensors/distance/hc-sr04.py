#!/usr/bin/env python3
import signal
import sys
import time
import wiringpi as pi

trigger_pin = 17
echo_pin = 23


def send_trigger_pulse() -> None:
    pi.digitalWrite(trigger_pin, pi.HIGH)
    time.sleep(.0001)
    pi.digitalWrite(trigger_pin, pi.LOW)


def wait_for_echo(value, timeout) -> None:
    count = timeout
    while pi.digitalRead(echo_pin) != value and count > 0:
        count -= 1


def get_distance() -> float:
    send_trigger_pulse()
    wait_for_echo(True, 10000)
    start = time.time()
    wait_for_echo(False, 10000)
    pulse_len = time.time() - start
    return pulse_len / .000058


def exit(signal, frame):
    print("signal: {}. frame: {}".format(signal, frame))
    sys.exit(1)


def main():
    """ entrypoint
    wiringpi needs sudo
    """
    signal.signal(signal.SIGINT, exit)
    signal.signal(signal.SIGTERM, exit)
    signal.signal(signal.SIGHUP, exit)
    signal.signal(signal.SIGQUIT, exit)

    pi.wiringPiSetupGpio()
    pi.pinMode(trigger_pin, pi.OUTPUT)
    pi.pinMode(echo_pin, pi.INPUT)
    while True:
        print("{}cm".format(get_distance()))
        time.sleep(1)


if __name__ == "__main__":
    main()
