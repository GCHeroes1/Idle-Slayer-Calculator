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

var SortDirection;
(function (SortDirection) {
    SortDirection[SortDirection["asc"] = 0] = "asc";
    SortDirection[SortDirection["des"] = 1] = "des";
})(SortDirection || (SortDirection = {}));

const sort_direction_to_string = (dir) => {
    switch (dir) {
        case SortDirection.asc:
            return "asc";
        case SortDirection.des:
            return "des";
    }
};

const sort_table_inner = (t_body, header_idx, dir) => {
    const rows = [];
    for (const element of t_body.childNodes) {
        if (element.nodeType == 1) {
            rows.push(element);
        }
    }
    rows.sort((a, b) => {
        const a_sort_value = Number(a.childNodes[header_idx].textContent);
        const b_sort_value = Number(b.childNodes[header_idx].textContent);
        if (!isNaN(a_sort_value) && !isNaN(b_sort_value)) {
            switch (dir) {
                case SortDirection.asc:
                    return a_sort_value - b_sort_value;
                case SortDirection.des:
                    return b_sort_value - a_sort_value;
            }
        } else {
            //fall back to string comparison
            const a_text = a.childNodes[header_idx].textContent;
            const b_text = b.childNodes[header_idx].textContent;
            switch (dir) {
                case SortDirection.asc:
                    if (a_text !== null && b_text !== null) {
                        return a_text.localeCompare(b_text);
                    }
                    if (a_text === null && b_text === null) {
                        return 0;
                    } else if (a_text === null) {
                        return 1;
                    } else {
                        return -1;
                    }
                case SortDirection.des:
                    if (a_text !== null && b_text !== null) {
                        return b_text.localeCompare(a_text);
                    }
                    if (a_text === null && b_text === null) {
                        return 0;
                    } else if (a_text === null) {
                        return -1;
                    } else {
                        return 1;
                    }
            }
        }
    });
    for (const row of rows) {
        t_body.appendChild(row);
    }
};

const setAllCheckboxes = (value) => {
    Array.from(document.getElementsByTagName("input")).forEach((input) => {
        if (input.type === "checkbox" && input.checked !== value) {
            input.click();
        }
    });
};

const setAllCollapse = (value) => {
    Array.from(document.getElementsByClassName("collapsible")).forEach((input) => {
        // false = collapse All -> if its active, you need to click it
        // true = uncollapse all -> if its not active, you need to click it
        if (value && !input.classList.contains("active")) {
            input.click()
        }
        if (!value && input.classList.contains("active")) {
            input.click()
        }
    });
};

const checkCoins = (value) => {
    current_coins = 0;
    Array.from(document.getElementsByTagName("input")).forEach((input) => {
        if (input.type === "checkbox" && input.checked === value) {
            if (+input.value > current_coins && input.value.includes("e")) {
                current_coins = +input.value;
            }
        }
    });
}

const change_table_sort = (event) => {
    var _a, _b;
    const header = event.currentTarget;
    const current_dir = header.classList.contains(sort_direction_to_string(SortDirection.des)) ? SortDirection.des : SortDirection.asc;
    const new_dir = current_dir === SortDirection.asc ? SortDirection.des : SortDirection.asc;
    const header_name = header.textContent;
    const all_headers = (_a = header.closest("tr")) === null || _a === void 0 ? void 0 : _a.childNodes;
    if (all_headers === undefined) {
        return;
    }
    let header_idx = -1;
    let count = 0;
    for (const header_element of all_headers) {
        if (header_element.nodeType === 1) {
            header_element.classList.remove(sort_direction_to_string(SortDirection.asc), sort_direction_to_string(SortDirection.des));
            if (header_element.textContent === header_name) {
                header_idx = count;
            }
            count++;
        }
    }
    header.classList.add(sort_direction_to_string(new_dir));
    if (header_idx === -1) {
        return;
    }
    const table = header.closest("table");
    const t_body = (_b = table === null || table === void 0 ? void 0 : table.getElementsByTagName("tbody")) === null || _b === void 0 ? void 0 : _b.item(0);
    if (t_body === null || t_body === undefined) {
        return;
    }
    sort_table_inner(t_body, header_idx, new_dir);
};

document.addEventListener("DOMContentLoaded", () => {
    create_table(unlocked_dimensions);
    // setup_random_box_simulation();
    void get_evolution_names();
    void get_giant_names();
    void get_upgrade_names();
    void get_armory();
    void get_stones();
    void get_random_boxes();
    void get_table_values();
    const sortable_headers = document.querySelectorAll(".sortable");
    for (const header of sortable_headers) {
        header.addEventListener("click", change_table_sort);
    }
    // handle clicks on check/uncheck all
    document.getElementById("checkAll").addEventListener("click", () => {
        setAllCheckboxes(true);
    });
    document.getElementById("unCheckAll").addEventListener("click", () => {
        setAllCheckboxes(false);
    });
    // handle clicks on collapse/uncollapse all
    document.getElementById("collapseAll").addEventListener("click", () => {
        setAllCollapse(false);
    });
    document.getElementById("uncollapseAll").addEventListener("click", () => {
        setAllCollapse(true);
    });
    document.getElementById("updateTables").addEventListener("click", () => {
        delete_table();
        create_table(unlocked_dimensions);
        void get_table_values();
    });
});

var coll = document.getElementsByClassName("collapsible");
for (var i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function () {
        this.classList.toggle("active");
        var content = this.nextElementSibling;
        if (content.style.display === "block") {
            content.style.display = "none";
        } else {
            content.style.display = "block";
        }
    });
}

const dimension_options_area = document.getElementById("mapValueDimensions");
const enemy_spawn_options_area = document.getElementById("mapValueEnemySpawnRateList");
const giant_spawn_options_area = document.getElementById("mapValueGiantSpawnRateList");
const bow_soul_options_area = document.getElementById("mapValueBowSouls");
const rage_soul_options_area = document.getElementById("mapValueRageSouls");
const giant_soul_options_area = document.getElementById("mapValueGiantSouls");
const critical_options_area = document.getElementById("mapValueCritical");
const evolutions_list = document.getElementById("mapValueEvolutionsList");
const giants_list = document.getElementById("mapValueGiantsList");
const armory_names = document.getElementById("mapValueArmoryNames");
const armory_list = document.getElementById("mapValueArmoryList");
const armory_options = document.getElementById("mapValueArmoryOptions");
const armory_levels = document.getElementById("mapValueArmoryLevels");
const stone_names = document.getElementById("mapValueStoneNames");
const stone_levels = document.getElementById("mapValueStoneLevels");
const random_box_options_area = document.getElementById("mapValueRandomBoxes");
const random_box_time = document.getElementById("mapValueRandomBoxesTime");
const active_results_table = document.getElementById("mapValuesResultsTableActive");
const bow_results_table = document.getElementById("mapValuesResultsTableBow");
const rage_results_table = document.getElementById("mapValuesResultsTableRage");

let unlocked_dimensions = ["Hills", "Frozen Fields", "Jungle", "Modern City", "Haunted Castle"];
let unlocked_enemies = [];
let unlocked_giants = [];
let unlocked_enemy_spawn_upgrades = [];
let unlocked_giant_spawn_upgrades = [];
let unlocked_bow_soul_upgrades = [];
let unlocked_giant_soul_upgrades = [];
let unlocked_rage_soul_upgrades = [];
let unlocked_critical_upgrades = [];
let unlocked_random_box_upgrades = [];
let unlocked_armory = {};
let unlocked_stones = {};
let current_coins = 0;
let map_active_value_result_cells = {};
const map_bow_value_result_cells = {};
const map_rage_value_result_cells = {};

function enemy_checkboxes(list) {
    list[0].forEach((enemy, index) => {
        let cost = list[1][index];
        cost = cost[[cost.length - 1]]
        evolutions_list.appendChild(create_evolution_checkbox(enemy, cost, unlocked_enemies));
    });
}

function giant_checkboxes(list) {
    list[0].forEach((giant, index) => {
        let cost = list[1][index];
        if (cost[3]) {
            cost = cost[3]
        } else {
            cost = 0
        }
        giants_list.appendChild(create_evolution_checkbox(giant, cost, unlocked_giants));
    });
}

function upgrade_checkboxes(list) {
    list[0].forEach((upgrade, index) => {
        bow_soul_options_area.appendChild(create_evolution_checkbox(upgrade[0], upgrade[1], unlocked_bow_soul_upgrades));
    });
    list[1].forEach((upgrade, index) => {
        giant_soul_options_area.appendChild(create_evolution_checkbox(upgrade[0], upgrade[1], unlocked_giant_soul_upgrades));
    });
    list[2].forEach((upgrade, index) => {
        rage_soul_options_area.appendChild(create_evolution_checkbox(upgrade[0], upgrade[1], unlocked_rage_soul_upgrades));
    });
    list[3].forEach((upgrade, index) => {
        enemy_spawn_options_area.appendChild(create_evolution_checkbox(upgrade[0], upgrade[1], unlocked_enemy_spawn_upgrades));
    });
    list[4].forEach((upgrade, index) => {
        giant_spawn_options_area.appendChild(create_evolution_checkbox(upgrade[0], upgrade[1], unlocked_giant_spawn_upgrades));
    });
    list[5].forEach((upgrade, index) => {
        critical_options_area.appendChild(create_evolution_checkbox(upgrade[0], upgrade[1], unlocked_critical_upgrades));
    });
    list[6].forEach((upgrade, index) => {
        random_box_options_area.appendChild(create_evolution_checkbox(upgrade[0], upgrade[1], unlocked_random_box_upgrades));
    });
    list[7].forEach((upgrade, index) => {
        dimension_options_area.appendChild(create_evolution_checkbox(upgrade[0], upgrade[1], unlocked_dimensions));
    });
}

function create_evolution_checkbox(name, cost, unlocked_array) {
    var checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.name = name;
    checkbox.id = name;
    checkbox.value = cost;
    checkbox.addEventListener('change', function () {
        if (this.checked) {
            unlocked_array.push(name);
        } else {
            const index = unlocked_array.indexOf(name);
            if (index > -1) {
                unlocked_array.splice(index, 1);
            }
        }
        checkCoins(true);
        if (unlocked_array === unlocked_random_box_upgrades) {
            void get_random_boxes();
        }
        // get_table_values();
        // console.log(unlocked_array);
    });

    var label = document.createElement("label")
    cost = cost.toString().replace("+", "")
    label.textContent = name + " [" + cost + "]";
    label.htmlFor = name;

    var container = document.createElement("li");
    container.appendChild(checkbox);
    container.appendChild(label);
    return container;
}

function calculate_map_values_active(active_souls) {
    for (const [key, value] of Object.entries(active_souls)) {
        map_active_value_result_cells[key]["coins"].innerText = String((value["Coins"]).toFixed(2));
        map_active_value_result_cells[key]["souls"].innerText = String((value["Souls"]).toFixed(2));
    }
}

function calculate_map_values_bow(bow_souls) {
    for (const [key, value] of Object.entries(bow_souls)) {
        map_bow_value_result_cells[key]["coins"].innerText = String((value["Coins"]).toFixed(2));
        map_bow_value_result_cells[key]["souls"].innerText = String((value["Souls"]).toFixed(2));
    }
}

function calculate_map_values_rage(rage_souls) {
    for (const [key, value] of Object.entries(rage_souls)) {
        map_rage_value_result_cells[key]["coins"].innerText = String((value["Coins"]).toFixed(2));
        map_rage_value_result_cells[key]["souls"].innerText = String((value["Souls"]).toFixed(2));
    }
}

const create_map_row = (table, map, type) => {
    const coins = document.createElement("td");
    const souls = document.createElement("td");
    if (type === "active") {
        map_active_value_result_cells[map] = {coins, souls};
    } else if (type === "bow") {
        map_bow_value_result_cells[map] = {coins, souls};
    } else if (type === "rage") {
        map_rage_value_result_cells[map] = {coins, souls};
    }
    const map_row = document.createElement("tr");
    map_row.classList.add(type + "_");
    const map_name_cell = document.createElement("td");
    map_name_cell.textContent = map;
    map_row.appendChild(map_name_cell);
    map_row.appendChild(coins);
    map_row.appendChild(souls);
    table.appendChild(map_row);
};

function create_table(dimensions) {
    for (const map of dimensions) {
        create_map_row(active_results_table, map, "active");
        create_map_row(bow_results_table, map, "bow");
        create_map_row(rage_results_table, map, "rage");
    }
}

function delete_table() {
    Array.from(document.getElementsByClassName("active" + "_")).forEach((input) => {
        input.remove()
    })
    Array.from(document.getElementsByClassName("bow" + "_")).forEach((input) => {
        input.remove()
    })
    Array.from(document.getElementsByClassName("rage" + "_")).forEach((input) => {
        input.remove()
    })
}

async function get_evolution_names() {
    const fetchPromise = fetch("http://127.0.0.1:5000/evolutionNames");
    fetchPromise.then(response => {
        return response.json();
    }).then(response => {
        enemy_checkboxes(response);
    });
}

async function get_giant_names() {
    const fetchPromise = fetch("http://127.0.0.1:5000/giantNames");
    fetchPromise.then(response => {
        return response.json();
    }).then(response => {
        giant_checkboxes(response);
    });
}

async function get_upgrade_names() {
    const fetchPromise = fetch("http://127.0.0.1:5000/upgradeNames");
    fetchPromise.then(response => {
        return response.json();
    }).then(response => {
        upgrade_checkboxes(response);
    });
}

async function get_table_values() {
    console.log(unlocked_armory);
    const fetchPromise = fetch("http://127.0.0.1:5000/calculateStats", {
        method: "GET",
        headers: {
            "DIMENSIONS": unlocked_dimensions,
            "ENEMY_SPAWN": unlocked_enemy_spawn_upgrades,
            "GIANT_SPAWN": unlocked_giant_spawn_upgrades,
            "CRITICAL_UPGRADES": unlocked_critical_upgrades,
            "BOW_SOULS": unlocked_bow_soul_upgrades,
            "GIANT_SOULS": unlocked_giant_soul_upgrades,
            "RAGE_SOULS": unlocked_rage_soul_upgrades,
            "ENEMY_EVOLUTIONS": unlocked_enemies,
            "GIANT_EVOLUTIONS": unlocked_giants,
            "CURRENT_COINS": current_coins,
            "ARMORY_SELECTION": JSON.stringify(unlocked_armory),
            "STONE_SELECTION": JSON.stringify(unlocked_stones)
        },
    });
    fetchPromise.then(response => {
        return response.json();
    }).then(response => {
        calculate_map_values_active(response[0]);
        calculate_map_values_bow(response[1]);
        calculate_map_values_rage(response[2])
    });
}

async function get_dimensions() {
    const fetchPromise = fetch("http://127.0.0.1:5000/dimensions", {
        method: "GET",
        headers: {
            "CURRENT_COINS": current_coins,
        },
    });
    fetchPromise.then(response => {
        return response.json();
    }).then(response => {
        // console.log(response)
        create_table(["Hills", "Frozen Fields", "Jungle", "Modern City", "Haunted Castle", "Mystic Valley", "Factory", "Hot Desert"]);
        // create_table(response);
    });
}

async function get_armory() {
    const fetchPromise = fetch("http://127.0.0.1:5000/armory");
    fetchPromise.then(response => {
        return response.json();
    }).then(response => {
        armory_section(response[1], response[2], response[3], response[4]);
    });
}

async function get_stones() {
    const fetchPromise = fetch("http://127.0.0.1:5000/stones");
    fetchPromise.then(response => {
        return response.json();
    }).then(response => {
        stone_section(response[0], response[1]);
    });
}

async function get_random_boxes() {
    const fetchPromise = fetch("http://127.0.0.1:5000/randomBoxes", {
        method: "GET",
        headers: {
            "RANDOM_BOX": unlocked_random_box_upgrades,
        },
    });
    fetchPromise.then(response => {
        return response.json();
    }).then(response => {
        random_box_time.appendChild(update_spawn_times(response[0], response[1]));
    });
}

function armory_section(types, subtypes, options, levels) {
    types.forEach((item, index) => {
        armory_names.appendChild(create_armory_text(item));
        armory_list.appendChild(create_armory_dropdown(item, subtypes[item]));
        for (const subtype of subtypes[item]) {
            armory_options.appendChild(create_armory_options_dropdown(item, subtype, options[item][subtype]));
            armory_levels.appendChild(create_armory_levels(item, subtype, levels[item][subtype]));
        }
    });
}

function create_armory_text(name) {
    var textNode = document.createTextNode(name);

    var container = document.createElement("li");
    container.appendChild(textNode);
    return container;
}

function create_armory_dropdown(item, subtypes) {
    subtype_array = [...subtypes]

    var select = document.createElement("select");
    select.name = item;
    select.id = item;
    select.addEventListener('change', (event) => {
        enableOptions(select, item);
        enableLevels(select, item);
    });

    select.addEventListener('change', function () {
        var e = document.getElementById(select.id)
        var text = e.options[e.selectedIndex].text;
        unlocked_armory[select.name] = {}
        unlocked_armory[select.name][text] = {};
        // void get_table_values();
    });

    for (const val of subtype_array) {
        var subtype = document.createElement("option");
        subtype.value = val;
        subtype.text = val.charAt(0).toUpperCase() + val.slice(1);
        select.appendChild(subtype);
    }
    var label = document.createElement("label");
    label.innerHTML = "Choose your item: "
    label.htmlFor = "item";
    var container = document.createElement("li");
    return container.appendChild(label).appendChild(select);
}

function enableOptions(select, item) {
    Array.from(document.getElementsByClassName(item)).forEach((input) => {
        let id = input.id;
        document.getElementById(id).classList.add("hidden");
        if (id === item + select.value) {
            document.getElementById(id).classList.remove("hidden");
        }
    })
}

function create_armory_options_dropdown(item, subtype, options) {
    var select = document.createElement("select");
    select.name = subtype;
    select.id = item + subtype;
    select.classList.add(item)
    select.multiple = true;
    if (subtype !== "None") {
        select.classList.add("hidden");
    }
    select.addEventListener('change', function () {
        var result = [];
        var options = select && select.options;
        var opt;

        for (var i = 0, iLen = options.length; i < iLen; i++) {
            opt = options[i];

            if (opt.selected) {
                result.push(opt.text);
            }
        }
        unlocked_armory[item][subtype]["Option"] = result;
        // void get_table_values();
    });

    for (const val of options) {
        var option = document.createElement("option");
        option.value = val;
        option.text = val.charAt(0).toUpperCase() + val.slice(1);
        select.appendChild(option);
    }
    var label = document.createElement("label");
    label.innerHTML = "Choose your option: "
    label.htmlFor = "option";
    var container = document.createElement("li");
    return container.appendChild(label).appendChild(select);
}

function enableLevels(select, item) {
    Array.from(document.getElementsByClassName(item + item)).forEach((input) => {
        let id = input.id;
        document.getElementById(id).classList.add("hidden");
        if (id === item + select.value + select.value) {
            document.getElementById(id).classList.remove("hidden");
        }
    })
}

function create_armory_levels(item, subtype, levels) {
    levels_array = [...levels]

    var select = document.createElement("select");
    select.name = subtype;
    select.id = item + subtype + subtype;
    select.classList.add(item + item);
    if (subtype !== "None") {
        select.classList.add("hidden");
    }
    select.addEventListener('change', function () {
        var e = document.getElementById(select.id)
        unlocked_armory[item][select.name]["Level"] = e.options[e.selectedIndex].text.slice(1);
        // void get_table_values();
    });

    for (const val of levels_array) {
        var level = document.createElement("option");
        level.value = val;
        if (val !== "None") {
            level.text = "+" + val;
        } else {
            level.text = val;
        }
        select.appendChild(level);
    }
    var label = document.createElement("label");
    label.innerHTML = "Choose your level: "
    label.htmlFor = "item";
    var container = document.createElement("li");
    return container.appendChild(label).appendChild(select);
}

function stone_section(stones, levels) {
    stones.forEach((item, index) => {
        stone_names.appendChild(create_stone_text(item));
        stone_levels.appendChild(create_stone_levels(item, levels[item]));
    });
}

function create_stone_text(stone) {
    var textNode = document.createTextNode(stone);
    var container = document.createElement("li");
    container.appendChild(textNode);
    return container;
}

function create_stone_levels(stone, levels) {
    levels_array = [...levels]

    var select = document.createElement("select");
    select.name = stone;
    select.id = stone;
    select.addEventListener('change', function () {
        var e = document.getElementById(select.id)
        unlocked_stones[stone] = e.options[e.selectedIndex].text;
        // console.log(unlocked_stones)
        // void get_table_values();
    });

    for (const val of levels_array) {
        var level = document.createElement("option");
        level.value = val;
        level.text = val;
        select.appendChild(level);
    }
    var label = document.createElement("label");
    label.innerHTML = "USP selection: "
    label.htmlFor = "USP";
    var container = document.createElement("li");
    return container.appendChild(label).appendChild(select);
}

function update_spawn_times(lower_time, upper_time) {
    if (document.getElementById("remove")) {
        random_box_time.removeChild(document.getElementById("remove"))
    }
    let textNode = document.createTextNode("Random boxes will spawn every " + lower_time.toFixed(1) + "-" + upper_time.toFixed(1) + " seconds.");
    let container = document.createElement("label");
    container.id = "remove"
    container.appendChild(textNode);
    return container;
}