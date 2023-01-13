$.ajaxSetup({
    type: "POST",
    data: {},
    dataType: 'json',
    xhrFields: {
        withCredentials: true
    },
    crossDomain: true,
    contentType: 'application/json; charset=utf-8'
});

var evolutioNames = {
    "url": "http://127.0.0.1:5000/evolutionNames",
    "method": "GET",
    "timeout": 0,
};
const options_area = document.getElementById("mapValueOptionsArea");
const evolutions_list = document.getElementById("mapValueEvolutionsList");
const giants_list = document.getElementById("mapValueGiantsList");
const active_results_table = document.getElementById("mapValuesResultsTableActive");
const idle_results_table = document.getElementById("mapValuesResultsTableIdle");

var unlocked_enemies = [];
var unlocked_giants = [];

function enemy_checkboxes(list) {
    for (const enemy of list) {
        evolutions_list.appendChild(create_evolution_checkbox(enemy, unlocked_enemies));
    }
}

function giant_checkboxes(list) {
    for (const giant of list) {
        giants_list.appendChild(create_evolution_checkbox(giant, unlocked_giants));
    }
}

function create_evolution_checkbox(name, unlocked_array) {
    var checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.name = name;
    checkbox.id = name;
    checkbox.addEventListener('change', function () {
        if (this.checked) {
            unlocked_array.push(name)
        } else {
            const index = unlocked_array.indexOf(name);
            if (index > -1) {
                unlocked_array.splice(index, 1);
            }
        }
        // console.log(unlocked_array)
    });

    var label = document.createElement("label")
    label.textContent = name;
    label.htmlFor = name;

    var container = document.createElement("li");
    container.appendChild(checkbox);
    container.appendChild(label);
    return container;
}

async function get_evolution_names() {
    const fetchPromise = fetch("http://127.0.0.1:5000/evolutionNames");
    fetchPromise.then(response => {
        return response.json();
    }).then(response => {
        enemy_checkboxes(response[0]);
    });
}

async function get_giant_names() {
    const fetchPromise = fetch("http://127.0.0.1:5000/giantNames");
    fetchPromise.then(response => {
        return response.json();
    }).then(response => {
        giant_checkboxes(response[0]);
    });
}

get_evolution_names()
get_giant_names()


// const base_enemies = [];
// const map_active_value_result_cells = {};
// const map_idle_value_result_cells = {};
// let pattern_level_input = null;
// let need_for_kill_input = null;
// let enemy_invasion_input = null;
// let multa_hostibus_input = null;
// let bone_rib_whistle_input = null;
// let bring_hell_input = null;
// let doomed_input = null;
// let big_troubles_input = null;
// const evolved = {};
// const giant_bought = {};
// const MAX_PATTERN_LEVEL = 3;
// const MIN_PATTERN_LEVEL = 1;
// const setup_map_value_area = async () => {
//     // const bonus_index = maps.findIndex((m) => m.name === "Bonus Stage");
//     // if (bonus_index !== -1) {
//     //     maps.splice(bonus_index, 1);
//     // }
//     // const bonus_two_index = maps.findIndex((m) => m.name === "Bonus Stage 2");
//     // if (bonus_two_index !== -1) {
//     //     maps.splice(bonus_two_index, 1);
//     // }
//     // const bonus_special_index = maps.findIndex((m) => m.name === "Special Bonus Stage");
//     // if (bonus_special_index !== -1) {
//     //     maps.splice(bonus_special_index, 1);
//     // }
//     // delete enemies["Soul Goblin"];
//     // delete enemies["Soul Hobgoblin"];
//     // delete enemies["Soul Goblin Chief"];
//     const options_area = document.getElementById("mapValueOptionsArea");
//     const evolutions_list = document.getElementById("mapValueEvolutionsList");
//     const giants_list = document.getElementById("mapValueGiantsList");
//     const active_results_table = document.getElementById("mapValuesResultsTableActive");
//     const idle_results_table = document.getElementById("mapValuesResultsTableIdle");
//     if (options_area === null || evolutions_list === null || active_results_table === null || idle_results_table === null || giants_list === null) {
//         return;
//     }
//     for (const [name, enemy] of Object.entries(enemies)) {
//         if (enemy.base) {
//             let evolved_enemy = enemy;
//             do {
//                 if (evolved_enemy.evolution === undefined) {
//                     break;
//                 }
//                 const evolved_name = evolved_enemy.evolution;
//                 evolved_enemy = enemies[evolved_enemy.evolution];
//                 evolutions_list.appendChild(create_evolution_checkbox(evolved_name, on_evolution_toggle));
//             } while (evolved_enemy !== undefined);
//             base_enemies.push(enemy);
//         }
//         evolved[name] = false;
//     }
//     for (const giant of giants) {
//         giants_list.appendChild(create_evolution_checkbox(giant.name, on_giant_toggle));
//         giant_bought[giant.name] = false;
//     }
//     const create_map_row = (table, map, type) => {
//         const coins = document.createElement("td");
//         const souls = document.createElement("td");
//         if (type === "active") {
//             map_active_value_result_cells[map.name] = {coins, souls};
//         } else if (type === "idle") {
//             map_idle_value_result_cells[map.name] = {coins, souls};
//         }
//         const map_row = document.createElement("tr");
//         const map_name_cell = document.createElement("td");
//         map_name_cell.textContent = map.name;
//         map_row.appendChild(map_name_cell);
//         map_row.appendChild(coins);
//         map_row.appendChild(souls);
//         table.appendChild(map_row);
//     };
//     for (const map of maps) {
//         create_map_row(active_results_table, map, "active");
//         create_map_row(idle_results_table, map, "idle");
//     }
//     pattern_level_input = document.querySelector("input[name=maxPatternLevel]");
//     if (pattern_level_input !== null) {
//         pattern_level_input.value = String(1);
//         pattern_level_input.addEventListener("change", () => {
//             if (pattern_level_input !== null) {
//                 const current_pattern_level_value = Number(pattern_level_input.value);
//                 if (isNaN(current_pattern_level_value)) {
//                     pattern_level_input.value = String(MIN_PATTERN_LEVEL);
//                 }
//                 if (current_pattern_level_value > MAX_PATTERN_LEVEL) {
//                     pattern_level_input.value = String(MAX_PATTERN_LEVEL);
//                 } else if (current_pattern_level_value < MIN_PATTERN_LEVEL) {
//                     pattern_level_input.value = String(MIN_PATTERN_LEVEL);
//                 }
//             }
//             calculate_map_values();
//         });
//     }
//     need_for_kill_input = document.querySelector("input[name=needForKill]");
//     enemy_invasion_input = document.querySelector("input[name=enemyInvasion]");
//     multa_hostibus_input = document.querySelector("input[name=multaHostibus]");
//     bone_rib_whistle_input = document.querySelector("input[name=boneRibWhistle]");
//     bring_hell_input = document.querySelector("input[name=bringHell]");
//     doomed_input = document.querySelector("input[name=doomed]");
//     big_troubles_input = document.querySelector("input[name=bigTroubles]");
//     calculate_map_values();
// };