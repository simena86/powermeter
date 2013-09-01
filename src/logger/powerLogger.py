#!/usr/bin/python


"""
ddExample of how to use GPIO and TCP interrupts with RPIO.
RPIO Documentation: http://pythonhosted.org/RPIO
"""
import RPIO


def gpio_callback(gpio_id, val):
    print("gpio %s: %s" % (gpio_id, val))


# Two GPIO interrupt callbacks (second one with a debouce timeout of 100ms)
RPIO.add_interrupt_callback(14, gpio_callback, edge='rising', \
        debounce_timeout_ms=100)

# Starts waiting for interrupts (exit with Ctrl+C)
RPIO.wait_for_interrupts()

