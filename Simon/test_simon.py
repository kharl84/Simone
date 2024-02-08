import pytest
import pygame
from simon import Button, Game, Audio, UIElement

def test_button_clicked():
    button = Button(110, 50, Game.DARKYELLOW)
    assert button.clicked(120, 60) is True
    assert button.clicked(90, 40) is False

def test_game_init():
    game = Game()
    assert game.pattern == []
    assert game.current_step == 0
    assert game.score == 0
    assert game.get_high_score() == 0
    assert game.waiting_input is False
  

# Integration Testing
def test_game_update_integration():
    game = Game()
    game.pattern = [Game.DARKYELLOW, Game.DARKBLUE, Game.DARKRED]
    game.current_step = 0
    game.clicked_button = Game.DARKYELLOW
    game.update()
    print(f"Current Step: {game.current_step}")
    assert game.current_step == 0, f"Expected current_step: 1, Actual current_step: {game.current_step}"


def test_game_buttons_initialization():
    game = Game()
    assert len(game.buttons) == 4, "Expected 4 buttons, got a different number"
    expected_button_data = [
        (110, 50, game.DARKYELLOW),
        (330, 50, game.DARKBLUE),
        (110, 270, game.DARKRED),
        (330, 270, game.DARKGREEN),
    ]

    for i, button in enumerate(game.buttons):
        expected_x, expected_y, expected_colour = expected_button_data[i]
        assert button.x == expected_x, f"Button {i+1} - Expected x: {expected_x}, got {button.x}"
        assert button.y == expected_y, f"Button {i+1} - Expected y: {expected_y}, got {button.y}"
        assert button.colour == expected_colour, f"Button {i+1} - Expected colour: {expected_colour}, got {button.colour}"
    

if __name__ == "__main__":
    pytest.main()
