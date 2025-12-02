from typing import Dict, Type, List
import random
from Card import Card, School
from Offense.cards_offense import (
    Strike, Slash, HeavyStrike, Execute, PoisonStrike, AreaAttack
)
from Defense.cards_defense import (
    ShieldUp, Dodge, ArmorUp, CounterAttack, Regeneration, Heal, Parry
)
from Utility.cards_utility import (
    DrawCards, DrawAndDiscount, BattleRage, ManaGain, DiscardForPower,
    Cycle, Duplicate, UpgradeCard, CostReduction, ExhaustForEffect, Scry
)
import card_ids as CID

# Main registry: ID -> Card Class
CARD_REGISTRY: Dict[int, Type[Card]] = {
    CID.STRIKE: Strike,
    CID.SLASH: Slash,
    CID.HEAVY_STRIKE: HeavyStrike,
    CID.EXECUTE: Execute,
    CID.POISON_STRIKE: PoisonStrike,
    CID.AREA_ATTACK: AreaAttack,
    
    CID.SHIELD_UP: ShieldUp,
    CID.DODGE: Dodge,
    CID.ARMOR_UP: ArmorUp,
    CID.COUNTER_ATTACK: CounterAttack,
    CID.REGENERATION: Regeneration,
    CID.HEAL: Heal,
    CID.PARRY: Parry,
    
    CID.DRAW_CARDS: DrawCards,
    CID.DRAW_AND_DISCOUNT: DrawAndDiscount,
    CID.BATTLE_RAGE: BattleRage,
    CID.MANA_GAIN: ManaGain,
    CID.DISCARD_FOR_POWER: DiscardForPower,
    CID.CYCLE: Cycle,
    CID.DUPLICATE: Duplicate,
    CID.UPGRADE_CARD: UpgradeCard,
    CID.COST_REDUCTION: CostReduction,
    CID.EXHAUST_FOR_EFFECT: ExhaustForEffect,
    CID.SCRY: Scry,
}


def create_card(card_id: int, tier: int = 0, school: School = School.NORMAL) -> Card:
    """
    Factory function to create card instances
    
    Args:
        card_id: The card ID (first 3 digits determine type)
        tier: Card tier (0=base, 1=upgraded once, etc.)
        school: Card school (NORMAL, MAGICAL, or TECHNICAL)
    
    Returns:
        A new instance of the requested card
    
    Raises:
        ValueError: If card_id is not in registry
    
    Example:
        >>> from card_ids import STRIKE
        >>> from Card import School
        >>> strike = create_card(STRIKE, tier=0, school=School.NORMAL)
        >>> magic_strike = create_card(STRIKE, tier=1, school=School.MAGICAL)
    """
    if card_id not in CARD_REGISTRY:
        raise ValueError(f"Invalid card ID: {card_id}")
    
    card_class = CARD_REGISTRY[card_id]
    return card_class(card_id, tier, school)


def get_random_card_ids(n: int, card_type: int = None) -> List[int]:
    """
    Get n random card IDs, optionally filtered by type
    
    Args:
        n: Number of card IDs to return
        card_type: Optional filter - 0=Offense, 1=Defense, 2=Utility
    
    Returns:
        List of random card IDs
    
    Example:
        >>> # Get 3 random offense cards
        >>> ids = get_random_card_ids(3, card_type=0)
        >>> # Get 5 random cards from any type
        >>> ids = get_random_card_ids(5)
    """
    if card_type is not None:
        pool = [id for id in CARD_REGISTRY.keys() if CID.get_card_type(id) == card_type]
    else:
        pool = list(CARD_REGISTRY.keys())
    
    return random.sample(pool, min(n, len(pool)))


def get_all_card_ids() -> List[int]:
    """Return all valid card IDs"""
    return list(CARD_REGISTRY.keys())


def get_card_ids_by_type(card_type: int) -> List[int]:
    """
    Get all card IDs of a specific type
    
    Args:
        card_type: Type code (0=Offense, 1=Defense, 2=Utility)
    
    Returns:
        List of card IDs matching the type
    
    Example:
        >>> offense_ids = get_card_ids_by_type(0)
    """
    return [id for id in CARD_REGISTRY.keys() if CID.get_card_type(id) == card_type]
