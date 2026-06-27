import os
import sys
import json
import time

# Mocking pyautogui to run verification in environment that might lack display / UI loop
class MockPyAutoGUI:
    def __init__(self):
        self.FAILSAFE = True
        self.clicked_coords = []
        self.written_text = []
        self.pressed_keys = []
        self.hotkeys = []
        self.keys_down = []
        self.keys_up = []
        
    def hotkey(self, *args):
        print(f"[MockPyAutoGUI] Pressing hotkey combo: {args}")
        self.hotkeys.append(args)

    def keyDown(self, key):
        print(f"[MockPyAutoGUI] Key down: {key}")
        self.keys_down.append(key)

    def keyUp(self, key):
        print(f"[MockPyAutoGUI] Key up: {key}")
        self.keys_up.append(key)

    def screenshot(self, region=None):
        # Create a mock image with a red strip for testing detection
        from PIL import Image, ImageDraw
        width = region[2] if region else 500
        height = region[3] if region else 500
        img = Image.new('RGB', (width, height), color=(30, 30, 30))
        
        # Draw a red line to simulate error message red bar/text
        draw = ImageDraw.Draw(img)
        draw.line([(10, 50), (100, 50)], fill=(200, 20, 20), width=2)
        return img
        
    def click(self, x, y):
        print(f"[MockPyAutoGUI] Clicking at {x}, {y}")
        self.clicked_coords.append((x, y))
        
    def write(self, text, interval=0.0):
        print(f"[MockPyAutoGUI] Writing text: '{text}'")
        self.written_text.append(text)
        
    def press(self, key):
        print(f"[MockPyAutoGUI] Pressing key: {key}")
        self.pressed_keys.append(key)

# Substitute pyautogui
import pyautogui
mock_pyautogui = MockPyAutoGUI()

# Temporarily patch pyautogui
original_screenshot = pyautogui.screenshot
original_click = pyautogui.click
original_write = pyautogui.write
original_press = pyautogui.press
original_hotkey = getattr(pyautogui, 'hotkey', None)
original_keyDown = getattr(pyautogui, 'keyDown', None)
original_keyUp = getattr(pyautogui, 'keyUp', None)

pyautogui.screenshot = mock_pyautogui.screenshot
pyautogui.click = mock_pyautogui.click
pyautogui.write = mock_pyautogui.write
pyautogui.press = mock_pyautogui.press
pyautogui.hotkey = mock_pyautogui.hotkey
pyautogui.keyDown = mock_pyautogui.keyDown
pyautogui.keyUp = mock_pyautogui.keyUp

try:
    from auto_continuer import send_continue_command, load_config
    
    print("[Test] Loading configuration...")
    config = load_config()
    print(f"[Test] Config loaded: {config}")
    
    print("[Test] Sending continue command via mockup...")
    send_continue_command(config)
    
    print("[Test] Verifying simulation inputs...")
    expected_pin1 = config.get("click_coords_1", [100, 800])
    expected_pin2 = config.get("click_coords_2", config.get("chat_input_coords", [100, 950]))
    
    assert len(mock_pyautogui.clicked_coords) >= 2, "Should click at least 2 times sequentially!"
    assert mock_pyautogui.clicked_coords[0] == (expected_pin1[0], expected_pin1[1]), f"Pin 1 click coordinate mismatch! Got {mock_pyautogui.clicked_coords[0]}, expected {expected_pin1}"
    assert mock_pyautogui.clicked_coords[1] == (expected_pin2[0], expected_pin2[1]), f"Pin 2 click coordinate mismatch! Got {mock_pyautogui.clicked_coords[1]}, expected {expected_pin2}"
    
    # Check hotkey combo / keyDown ctrl / keyUp ctrl / delete / backspace press
    assert 'ctrl' in mock_pyautogui.keys_down, "ctrl key down not found!"
    assert 'a' in mock_pyautogui.pressed_keys, "a key press not found!"
    assert 'ctrl' in mock_pyautogui.keys_up, "ctrl key up not found!"
    assert "delete" in mock_pyautogui.pressed_keys or "backspace" in mock_pyautogui.pressed_keys, "Delete/Backspace key press not found!"
    
    expected_message = config.get("continue_message", "Continue the current task if it is not yet complete. If the current task has already been completed, analyze the project and automatically implement the next meaningful feature that best fits the existing architecture and roadmap. Ensure the new feature is fully integrated, follows the project's coding style, does not break existing functionality, and includes all necessary code, tests, and documentation where applicable. Repeat this workflow until no further meaningful improvements can be identified")
    assert mock_pyautogui.written_text[0] == expected_message, f"Written text mismatch! Expected: {expected_message}, got: {mock_pyautogui.written_text[0]}"
    assert "enter" in mock_pyautogui.pressed_keys, "Enter key press mismatch!"
    
    print("[Test] Verifying periodic settings load...")
    assert config.get("periodic_send_enabled") == True
    assert config.get("periodic_send_interval_seconds") == 300
    
    print("\n[Test] ALL TESTS PASSED SUCCESSFULLY! The auto-continuer logic works flawlessly.")
    
finally:
    # Restore original pyautogui
    pyautogui.screenshot = original_screenshot
    pyautogui.click = original_click
    pyautogui.write = original_write
    pyautogui.press = original_press
    if original_hotkey is not None:
        pyautogui.hotkey = original_hotkey
    if original_keyDown is not None:
        pyautogui.keyDown = original_keyDown
    if original_keyUp is not None:
        pyautogui.keyUp = original_keyUp
