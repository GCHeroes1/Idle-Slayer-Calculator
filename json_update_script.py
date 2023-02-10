from pathlib import Path

from Armory import get_armory_json, get_armory_info
from Criticals import get_crit_json
from Dimensions import get_dimension_json
from Enemies import get_enemies_json
from Giants import get_giants_json
from Patterns import get_dimension_patterns_json
from Rage import get_rage_json
from RandomBoxes import get_random_box_json, get_random_box_event_odds_json, get_random_box_extra_options_json
from StonesOfTime import get_stones_of_time_json, get_sot_info
from Upgrades import get_giant_costs_json, get_upgrades_json

if __name__ == '__main__':
    Path("./data").mkdir(parents=True, exist_ok=True)

    get_armory_json()
    get_armory_info()
    get_crit_json()
    get_dimension_json()
    get_enemies_json()
    get_giant_costs_json()
    get_giants_json()
    get_dimension_patterns_json()
    get_rage_json()
    get_random_box_json()
    get_random_box_event_odds_json()
    get_random_box_extra_options_json()
    get_stones_of_time_json()
    get_sot_info()
    get_upgrades_json()
