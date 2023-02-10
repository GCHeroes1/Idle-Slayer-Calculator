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

const endpoint = "https://idle-slayer-calculator.com/"
// const endpoint = "http://127.0.0.1:5000/"

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

const delete_checkboxes = (value) => {
    Array.from(document.getElementsByClassName("checkbox")).forEach((input) => {
        input.remove()
    })
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

const update_table_sort = (table) => {
    //find header indicating sort
    const headers = table.querySelectorAll("th");
    let idx = 0;
    let header_idx = -1;
    let sort_dir = SortDirection.des;
    for (const header of headers) {
        if (header.nodeType === 1) {
            if (header.classList.contains(sort_direction_to_string(SortDirection.des))) {
                sort_dir = SortDirection.des;
                header_idx = idx;
                break;
            }
            if (header.classList.contains(sort_direction_to_string(SortDirection.asc))) {
                sort_dir = SortDirection.asc;
                header_idx = idx;
                break;
            }
            idx++;
        }
    }
    const t_body = table.querySelector("tbody");
    if (t_body === null || header_idx === -1) {
        return;
    }
    sort_table_inner(t_body, header_idx, sort_dir);
};

function setup() {
    void get_evolution_names();
    void get_giant_names();
    void get_upgrade_names();
    void get_random_boxes();
}

function update_tables() {
    delete_table();
    create_table(unlocked_dimensions);
    void get_table_values();
}

document.addEventListener("DOMContentLoaded", () => {
    void create_table(unlocked_dimensions);
    void get_random_box_odds();
    void setup();
    void get_armory();
    void get_stones();
    void get_table_values();

    const sortable_headers = document.querySelectorAll(".sortable");
    for (const header of sortable_headers) {
        header.addEventListener("click", change_table_sort);
    }
    // handle clicks on check/uncheck all
    document.getElementById("checkAll").addEventListener("click", () => {
        setAllCheckboxes(true);
        setTimeout(update_tables(), 1000);
    });
    document.getElementById("unCheckAll").addEventListener("click", () => {
        setAllCheckboxes(false);
        setTimeout(update_tables(), 1000);
    });
    // handle clicks on collapse/uncollapse all
    document.getElementById("collapseAll").addEventListener("click", () => {
        setAllCollapse(false);
    });
    document.getElementById("uncollapseAll").addEventListener("click", () => {
        setAllCollapse(true);
    });
    // document.getElementById("updateTables").addEventListener("click", () => {
    //     update_tables();
    // });
    document.getElementById("toggleNotation").addEventListener("click", () => {
        setAllCheckboxes(false);
        delete_checkboxes();
        if (scientific !== 2) {
            void setup();
            scientific = 2;
        } else {
            void setup();
            scientific = 1;
        }
        update_tables();
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

const random_box_options_area = document.getElementById("randomBoxOptionsArea");
const random_box_results_table = document.getElementById("randomBoxResultsTable");
const random_box_upgrades_area = document.getElementById("randomBoxSpawn");
const random_box_time = document.getElementById("randomBoxTime");

const dimension_options_area = document.getElementById("mapValueDimensions");
const enemy_spawn_options_area = document.getElementById("mapValueEnemySpawnRateList");
const giant_spawn_options_area = document.getElementById("mapValueGiantSpawnRateList");
const boost_soul_options_area = document.getElementById("mapValueBoostSouls");
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
const USP_allocation = document.getElementById("mapValueUSPAllocation");
const stone_names = document.getElementById("mapValueStoneNames");
const stone_levels = document.getElementById("mapValueStoneLevels");
const active_results_table = document.getElementById("mapValuesResultsTableActive");
const bow_results_table = document.getElementById("mapValuesResultsTableBow");
const current_bow_souls = document.getElementById("mapValueCurrentBowSouls");
const rage_results_table = document.getElementById("mapValuesResultsTableRage");
const current_rage_souls = document.getElementById("mapValueCurrentRageSouls");

let unlocked_dimensions = ["Hills", "Frozen Fields", "Jungle", "Modern City", "Haunted Castle"];
let unlocked_enemies = [];
let unlocked_giants = [];
let unlocked_enemy_spawn_upgrades = [];
let unlocked_giant_spawn_upgrades = [];
let unlocked_boost_soul_upgrades = [];
let unlocked_bow_soul_upgrades = [];
let unlocked_giant_soul_upgrades = [];
let unlocked_rage_soul_upgrades = [];
let unlocked_critical_upgrades = [];
let unlocked_random_box_upgrades = [];
let unlocked_random_box_options = [];
let unlocked_armory = {};
let unlocked_stones = {};
let map_active_value_result_cells = {};
const map_bow_value_result_cells = {};
const map_rage_value_result_cells = {};

let scientific = 2;
let total_USP = 0;

function enemy_checkboxes(list) {
    for (const [key, enemy] of Object.entries(list)) {
        const enemy_name = enemy[0]
        const enemy_cost = enemy[[enemy.length - scientific]]; // -1 for standard, maybe a global variable that gets +1 -1 in value
        evolutions_list.appendChild(create_checkbox(enemy_name, enemy_cost, unlocked_enemies));
    }
}

function giant_checkboxes(list) {
    for (const [key, giant] of Object.entries(list)) {
        const giant_name = giant[0];
        const giant_cost = giant[[giant.length - scientific]];
        giants_list.appendChild(create_checkbox(giant_name, giant_cost, unlocked_giants));
    }
}

function upgrade_checkboxes(list) {
    for (const [key, upgrade] of Object.entries(list[0])) {
        boost_soul_options_area.appendChild(create_checkbox(upgrade[0], upgrade[[upgrade.length - scientific]], unlocked_boost_soul_upgrades));
    }
    for (const [key, upgrade] of Object.entries(list[1])) {
        bow_soul_options_area.appendChild(create_checkbox(upgrade[0], upgrade[[upgrade.length - scientific]], unlocked_bow_soul_upgrades));
    }
    for (const [key, upgrade] of Object.entries(list[2])) {
        giant_soul_options_area.appendChild(create_checkbox(upgrade[0], upgrade[[upgrade.length - scientific]], unlocked_giant_soul_upgrades));
    }
    for (const [key, upgrade] of Object.entries(list[3])) {
        rage_soul_options_area.appendChild(create_checkbox(upgrade[0], upgrade[[upgrade.length - scientific]], unlocked_rage_soul_upgrades));
    }
    for (const [key, upgrade] of Object.entries(list[4])) {
        enemy_spawn_options_area.appendChild(create_checkbox(upgrade[0], upgrade[[upgrade.length - scientific]], unlocked_enemy_spawn_upgrades));
    }
    for (const [key, upgrade] of Object.entries(list[5])) {
        giant_spawn_options_area.appendChild(create_checkbox(upgrade[0], upgrade[[upgrade.length - scientific]], unlocked_giant_spawn_upgrades));
    }
    for (const [key, upgrade] of Object.entries(list[6])) {
        critical_options_area.appendChild(create_checkbox(upgrade[0], upgrade[[upgrade.length - scientific]], unlocked_critical_upgrades));
    }
    for (const [key, upgrade] of Object.entries(list[7])) {
        random_box_upgrades_area.appendChild(create_checkbox(upgrade[0], upgrade[[upgrade.length - scientific]], unlocked_random_box_upgrades));
    }
    for (const [key, upgrade] of Object.entries(list[8])) {
        dimension_options_area.appendChild(create_checkbox(upgrade[0], upgrade[[upgrade.length - scientific]], unlocked_dimensions));
    }
    for (const [key, upgrade] of Object.entries(list[9])) {
        random_box_options_area.appendChild(create_checkbox(upgrade[0], upgrade[[upgrade.length - scientific]], unlocked_random_box_options));
    }
}

function create_checkbox(name, cost, unlocked_array) {
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
        if (unlocked_array === unlocked_random_box_upgrades) {
            void get_random_boxes();
        } else if (unlocked_array === unlocked_random_box_options) {
            void get_random_box_odds();
        } else {
            update_tables();
        }
        // console.log(unlocked_array);
    });

    var label = document.createElement("label")
    cost = cost.toString().replace("+", "")
    label.textContent = name + " [" + cost + "]";
    label.htmlFor = name;

    var container = document.createElement("li");
    container.appendChild(checkbox);
    container.appendChild(label);
    container.classList.add("checkbox")
    return container;
}

function calculate_map_values_active(active_souls) {
    for (const [key, value] of Object.entries(active_souls)) {
        map_active_value_result_cells[key]["coins"].innerText = String((value["Coins"]).toFixed(2));
        map_active_value_result_cells[key]["souls"].innerText = String((value["Souls"]).toFixed(2));
    }
    const active_table = (_a = document.querySelector("#mapValuesResultsTableActive")) === null || _a === void 0 ? void 0 : _a.closest("table");
    update_table_sort(active_table);
}

function calculate_map_values_bow(bow_souls) {
    for (const [key, value] of Object.entries(bow_souls)) {
        map_bow_value_result_cells[key]["coins"].innerText = String((value["Coins"]).toFixed(2));
        map_bow_value_result_cells[key]["souls"].innerText = String((value["Souls"]).toFixed(2));
    }
    const bow_table = (_a = document.querySelector("#mapValuesResultsTableBow")) === null || _a === void 0 ? void 0 : _a.closest("table");
    update_table_sort(bow_table);

}

function calculate_map_values_rage(rage_souls) {
    for (const [key, value] of Object.entries(rage_souls)) {
        map_rage_value_result_cells[key]["coins"].innerText = String((value["Coins"]).toFixed(2));
        map_rage_value_result_cells[key]["souls"].innerText = String((value["Souls"]).toFixed(2));
    }
    const rage_table = (_a = document.querySelector("#mapValuesResultsTableRage")) === null || _a === void 0 ? void 0 : _a.closest("table");
    update_table_sort(rage_table);

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
    map_row.classList.add("souls_table");
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
    Array.from(document.getElementsByClassName("souls_table")).forEach((input) => {
        input.remove()
    })
}

async function get_evolution_names() {
    const fetchPromise = fetch(endpoint + "evolutionNames");
    fetchPromise.then(response => {
        return response.json();
    }).then(response => {
        enemy_checkboxes(response);
        return true;
    });
}

async function get_giant_names() {
    const fetchPromise = fetch(endpoint + "giantNames");
    fetchPromise.then(response => {
        return response.json();
    }).then(response => {
        giant_checkboxes(response);
        return true;
    });
}

async function get_upgrade_names() {
    const fetchPromise = fetch(endpoint + "upgradeNames");
    fetchPromise.then(response => {
        return response.json();
    }).then(response => {
        upgrade_checkboxes(response);
        return true;
    });
}

async function get_random_boxes() {
    body_data = JSON.stringify({
        "RANDOM_BOX": unlocked_random_box_upgrades
    })
    const fetchPromise = fetch(endpoint + "randomBoxes", {
        method: "POST",
        body: body_data
    });
    fetchPromise.then(response => {
        return response.json();
    }).then(response => {
        random_box_time.appendChild(update_spawn_times(response[0], response[1]));
        return true;
    });
}

async function get_table_values() {
    body_data = JSON.stringify({
        "DIMENSIONS": unlocked_dimensions,
        "ENEMY_SPAWN": unlocked_enemy_spawn_upgrades,
        "GIANT_SPAWN": unlocked_giant_spawn_upgrades,
        "CRITICAL_UPGRADES": unlocked_critical_upgrades,
        "BOOST_SOULS": unlocked_boost_soul_upgrades,
        "BOW_SOULS": unlocked_bow_soul_upgrades,
        "GIANT_SOULS": unlocked_giant_soul_upgrades,
        "RAGE_SOULS": unlocked_rage_soul_upgrades,
        "ENEMY_EVOLUTIONS": unlocked_enemies,
        "GIANT_EVOLUTIONS": unlocked_giants,
        "ARMORY_SELECTION": JSON.stringify(unlocked_armory),
        "STONE_SELECTION": JSON.stringify(unlocked_stones)
    })
    console.log(JSON.stringify(unlocked_armory));
    const fetchPromise = fetch(endpoint + "calculateStats", {
        method: "POST",
        body: body_data
    });
    fetchPromise.then(response => {
        return response.json();
    }).then(response => {
        calculate_map_values_active(response[0]);
        calculate_map_values_bow(response[1]);
        calculate_map_values_rage(response[2])
        current_bow_souls.appendChild(create_multiplier_text(current_bow_souls, "Bow", response[3]))
        current_rage_souls.appendChild(create_multiplier_text(current_rage_souls, "Rage", response[4]))
        return true;
    });
}

async function get_armory() {
    const fetchPromise = fetch(endpoint + "armory");
    fetchPromise.then(response => {
        return response.json();
    }).then(response => {
        armory_section(response[1], response[2], response[3], response[4]);
        return true;
    });
}

async function get_stones() {
    const fetchPromise = fetch(endpoint + "stones");
    fetchPromise.then(response => {
        return response.json();
    }).then(response => {
        stone_section(response[0], response[1]);
        USP_allocation.appendChild(create_usp_allocation(total_USP))
        return true;
    });
}

async function get_random_box_odds() {
    body_data = JSON.stringify({
        "RANDOM_BOX_OPTIONS": unlocked_random_box_options
    })
    const fetchPromise = fetch(endpoint + "calculateRandomBoxes", {
        method: "POST",
        body: body_data
    });
    fetchPromise.then(response => {
        return response.json();
    }).then(response => {
        setup_random_box_simulation(response)
        return true;
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
        update_tables();
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
        update_tables();
        // void get_table_values();
    });

    for (const val of options) {
        var option = document.createElement("option");
        option.value = val;
        option.text = val;
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
        update_tables();
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
        let total_USP = 0
        for (const [key, value] of Object.entries(unlocked_stones)) {
            total_USP += Number(value)
        }
        USP_allocation.appendChild(create_usp_allocation(total_USP));
        // console.log(unlocked_stones)
        update_tables();
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

function create_usp_allocation(USP) {
    if (document.getElementById("usp_remove")) {
        USP_allocation.removeChild(document.getElementById("usp_remove"))
    }
    let textNode = document.createTextNode("Currently allocated " + USP + " USP");
    let container = document.createElement("label");
    container.id = "usp_remove"
    container.appendChild(textNode);
    return container;
}

function update_spawn_times(lower_time, upper_time) {
    if (document.getElementById("box_remove")) {
        random_box_time.removeChild(document.getElementById("box_remove"))
    }
    let textNode = document.createTextNode("Random boxes will spawn every " + lower_time.toFixed(1) + "-" + upper_time.toFixed(1) + " seconds.");
    let container = document.createElement("label");
    container.id = "box_remove"
    container.appendChild(textNode);
    return container;
}

function create_multiplier_text(element, text, stat) {
    if (document.getElementById(text + "_remove")) {
        element.removeChild(document.getElementById(text + "_remove"))
    }
    let textNode = document.createTextNode("Current " + text + " Souls multiplier: " + stat.toFixed(1) + "x");
    let container = document.createElement("label");
    container.id = text + "_remove"
    container.appendChild(textNode);
    return container;
}

function setup_random_box_simulation(list_of_events) {
    Array.from(document.getElementsByClassName("random_box_table")).forEach((input) => {
        input.remove()
    })
    const random_box_result_cells = {};
    for (const [bonus, chance] of Object.entries(list_of_events)) {
        const bonus_row = document.createElement("tr");
        bonus_row.classList.add("random_box_table");

        const bonus_cell = document.createElement("td");
        const chance_cell = document.createElement("td");
        const average_cell = document.createElement("td");
        chance_cell.style.textAlign = "center"
        average_cell.style.textAlign = "center"
        bonus_cell.textContent = bonus;
        random_box_result_cells[bonus] = chance_cell;
        chance_cell.textContent = String((chance * 100).toFixed(2) + "%");
        let text = ""
        if (chance !== 0) {
            text = String((1 / chance).toFixed(2));
        }
        average_cell.textContent = text
        bonus_row.appendChild(bonus_cell);
        bonus_row.appendChild(chance_cell);
        bonus_row.appendChild(average_cell);
        random_box_results_table.appendChild(bonus_row);
        sort_random_box_table();
    }
}

function sort_random_box_table() {
    if (random_box_results_table === null) {
        return;
    }
    const store = [];
    for (let i = 0, len = random_box_results_table.rows.length; i < len; i++) {
        const row = random_box_results_table.rows[i];
        if (row.cells[1].textContent === null) {
            continue;
        }
        const sort_value = parseFloat(row.cells[1].textContent);
        store.push([sort_value, row]);
    }
    store.sort((a, b) => b[0] - a[0]);
    for (const [_, row] of store) {
        random_box_results_table.appendChild(row);
    }
}

setTimeout(update_tables, 1000);
