import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import random
import os
from pathlib import Path
from typing import List, Tuple, Dict, Any
from Code.Character.Character import Character
from Code.Cards.Card import Card
from Code.Cards.card_registry import create_card
from Code.Cards.card_ids import *
import Code.Cards.card_ids as CID


class EnemyAI:

    def __init__(self, model_path: str = None):
        if model_path is None:
            project_root = Path(__file__).resolve().parent.parent.parent
            self.model_path = str(project_root / "enemy_ai_model.keras")
        else:
            self.model_path = model_path
        self.model = None
        self.state_size = self._calculate_state_size()
        self.action_size = self._calculate_action_size()
        self._build_model()

    def _calculate_state_size(self) -> int:
        player_stats = 5
        enemy_stats = 5
        hand_features = 10 * 4
        return player_stats + enemy_stats + hand_features

    def _calculate_action_size(self) -> int:
        return 11

    def _build_model(self):
        self.model = keras.Sequential([
            layers.Dense(64, activation='relu', input_shape=(self.state_size,)),
            layers.Dropout(0.1),
            layers.Dense(32, activation='relu'),
            layers.Dense(self.action_size, activation='softmax')
        ])

        self.model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )

    def _encode_character_state(self, character: Character) -> List[float]:
        return [
            character.health / character.max_health,
            character.mana / character.current_max_mana if character.current_max_mana > 0 else 0,
            min(character.block / 20.0, 1.0),
            1.0 if character.dodge > 0 else 0.0,
            min(character.turn_number / 10.0, 1.0)
        ]

    def _encode_card(self, card: Card) -> List[float]:
        if card is None:
            return [0, 0, 0, 0]
        return [
            card.card_id / 2000.0,
            card.tier / 3.0,
            card.mana_cost / 5.0,
            card.get_effect_value(card.tier) / 20.0
        ]

    def get_state_vector(self, enemy: Character, player: Character) -> np.ndarray:
        state = []
        state.extend(self._encode_character_state(player))
        state.extend(self._encode_character_state(enemy))

        for i in range(10):
            if i < len(enemy.hand):
                state.extend(self._encode_card(enemy.hand[i]))
            else:
                state.extend([0, 0, 0, 0])

        return np.array(state, dtype=np.float32)

    def get_available_actions(self, enemy: Character) -> List[int]:
        actions = []
        for i, card in enumerate(enemy.hand):
            if card.mana_cost <= enemy.mana:
                actions.append(i)
        actions.append(10)
        return actions

    def choose_action(self, enemy: Character, player: Character) -> int:
        if self.model is None:
            available = self.get_available_actions(enemy)
            return random.choice(available) if available else self.action_size - 1

        state = self.get_state_vector(enemy, player)
        state = state.reshape(1, -1)

        predictions = self.model.predict(state, verbose=0)[0]

        available_actions = self.get_available_actions(enemy)
        if not available_actions:
            return self.action_size - 1

        best_action = max(available_actions, key=lambda x: predictions[x])
        return best_action

    def get_card_from_action(self, action: int, enemy: Character) -> Card:
        if action < len(enemy.hand):
            card = enemy.hand[action]
            if card.mana_cost <= enemy.mana:
                return card
        return None

    def save_model(self, filepath: str = None):
        if filepath is None:
            filepath = self.model_path
        if self.model:
            if filepath.endswith('.h5'):
                print("Saving model in legacy HDF5 (.h5) format as requested.")
            self.model.save(filepath)
            print(f"AI model saved to {filepath}")

    def load_model(self, filepath: str = None):
        if filepath is None:
            filepath = self.model_path
        tried = []
        candidates = [filepath]
        if filepath.endswith('.keras'):
            candidates.append(filepath[:-6] + '.h5')
        elif filepath.endswith('.h5'):
            candidates.append(filepath[:-3] + '.keras')

        for candidate in candidates:
            if candidate in tried:
                continue
            tried.append(candidate)
            if os.path.exists(candidate):
                try:
                    self.model = keras.models.load_model(candidate)
                    print(f"AI model loaded from {candidate}")
                    return True
                except Exception as e:
                    print(f"Failed to load model from {candidate}: {e}")

        print(f"No AI model found at any of: {candidates}")
        return False