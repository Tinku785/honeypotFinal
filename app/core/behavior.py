import random

class BehaviorSynthesizer:
    @staticmethod
    def apply_typo(text: str, probability=0.05):
        """Randomly swaps adjacent characters to simulate human error."""
        if len(text) < 5 or random.random() > probability:
            return text
        idx = random.randint(1, len(text) - 2)
        chars = list(text)
        chars[idx], chars[idx+1] = chars[idx+1], chars[idx]
        return "".join(chars)

    @staticmethod
    def calculate_human_delay(text: str):
        """Calculates delay based on 'Thinking Time' + 'Typing Time'."""
        thinking_time = random.uniform(1.5, 3.0)
        typing_time = len(text) * random.uniform(0.05, 0.1)
        return thinking_time + typing_time