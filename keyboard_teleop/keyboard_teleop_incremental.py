import os
import signal

import rclpy
from pynput.keyboard import Key, Listener

from keyboard_teleop.teleop import Teleop


class IncrementalKeyTeleop(Teleop):
    def __init__(self):
        super().__init__()
        self.key_listener = Listener(
            on_press=self.update_twist,
        )
        self.key_listener.start()
        self.declare_parameter("step", 0.)
        self.STEP = self.get_parameter("step").value
        self.angualr_step = 1.0
        self.linear_step = 1.0
        self.keys_bindings = {
            "w": (self.linear_step, 0.),  
            "s": (-self.linear_step, 0.),
            "a": (0., self.angualr_step),
            "d": (0., -self.angualr_step),
        }
        self.special_keys_bindings = {
            Key.up: (self.linear_step, 0),
            Key.down: (-self.linear_step, 0),
            Key.left: (0, self.angualr_step),
            Key.right: (0, -self.angualr_step),
        }
        self.get_logger().info(
            f"""
This node takes keypresses from the keyboard and publishes them 
as Twist messages. This is the incremental mode; every key press 
incrementally increase or decrease the respective dimensional speed.

WARNING: This node will take commands even if your terminal is not in focus!

Controls:

WASD or Arrows to increase/decrease speeds
Any other key to stop
CTRL-C or q to quit

Configuration:

Increment per keypress: {self.STEP} m/s or rad/s
Max Linear Speed: +/-{self.LINEAR_MAX} m/s
Max Angular Speed: +/-{self.ANGULAR_MAX} rad/s
"""
        )

    def update_twist(self, key):
        binding = None
        if self._is_special_key(key):
            if key in self.special_keys_bindings:
                binding = self.special_keys_bindings[key]
            else:
                print("stop!")
                self.write_twist(0.0, 0.0)
                return
        else:
            if key.char == "q":
                os.kill(os.getpid(), signal.SIGINT)
            if key.char in self.keys_bindings:                    
                binding = self.keys_bindings[key.char]
            else:
                self.write_twist(0.0, 0.0)
                return
        if binding is not None:
            new_linear = max(
                min(self.LINEAR_MAX, self.linear + binding[0]), 0.0 #-self.LINEAR_MAX
            )
            new_angular = max(
                min(self.ANGULAR_MAX, self.angular + binding[1]), -self.ANGULAR_MAX
            )
            self.write_twist(new_linear, new_angular)
        else:
            self.write_twist(self.linear, self.angular)

    def _is_special_key(self, key):
        try:
            key.char
            return False
        except AttributeError:
            return True


def main():
    try:
        rclpy.init()
        node = IncrementalKeyTeleop()
        rclpy.spin(node)
        rclpy.shutdown()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
