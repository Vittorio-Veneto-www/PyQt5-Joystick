# PyQt5-Joystick
A simple joystick written in PyQt5 with style control

# Features:
# Style controls:
- Pivot radius
- Stick radius
- Set geometry (will resize pivot and stick accordingly; maintain original center)
# Custom properties (can be set in designer's dynamic properties)
- pivotRadius
- stickRadius
- Setters and getters
# Custom signals
- stickMoved() -> tuple[int, float]
  - int represents direction
    - CENTER, UP, DOWN, LEFT, RIGHT constants in module
  - float represents the ratio of the distance to center to the pivot radius

# Reference:
https://stackoverflow.com/a/55899694
