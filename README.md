```bash
echo "deb [trusted=yes] https://github.com/li3coLich/keyboard_teleop/raw/jammy-humble-amd64/ ./" | sudo tee /etc/apt/sources.list.d/li3coLich_keyboard_teleop.list
echo "yaml https://github.com/li3coLich/keyboard_teleop/raw/jammy-humble-amd64/local.yaml humble" | sudo tee /etc/ros/rosdep/sources.list.d/1-li3coLich_keyboard_teleop.list
```
