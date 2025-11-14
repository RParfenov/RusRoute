const cities = [
    "Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань",
    "Нижний Новгород", "Челябинск", "Самара", "Омск", "Ростов-на-Дону",
    "Уфа", "Красноярск", "Воронеж", "Пермь", "Волгоград",
    "Саратов", "Краснодар", "Тольятти", "Ижевск", "Барнаул",
    "Ульяновск", "Иркутск", "Хабаровск", "Ярославль", "Владивосток",
    "Махачкала", "Томск", "Оренбург", "Кемерово", "Новокузнецк",
    "Рязань", "Астрахань", "Набережные Челны", "Пенза", "Липецк",
    "Киров", "Чебоксары", "Тула", "Калининград", "Курск",
    "Улан-Удэ", "Ставрополь", "Сочи", "Тверь", "Магнитогорск",
    "Иваново", "Брянск", "Севастополь", "Симферополь", "Великий Новгород",
    "Владимир", "Суздаль", "Кострома", "Смоленск", "Мурманск",
    "Архангельск", "Вологда", "Псков", "Петрозаводск", "Выборг",
    "Сергиев Посад", "Переславль-Залесский", "Ростов Великий", "Белгород", "Курган",
    "Орёл", "Калуга", "Сыктывкар", "Чита", "Южно-Сахалинск",
    "Анапа", "Геленджик", "Ялта", "Алушта", "Евпатория",
    "Феодосия", "Керчь", "Минеральные Воды", "Пятигорск", "Ессентуки",
    "Кисловодск", "Железноводск", "Дербент", "Элиста", "Нарьян-Мар",
    "Ханты-Мансийск", "Салехард", "Анадырь", "Петропавловск-Камчатский", "Благовещенск",
    "Якутск", "Нальчик", "Черкесск", "Майкоп", "Нижний Тагил",
    "Комсомольск-на-Амуре", "Орск", "Новороссийск", "Балашиха", "Подольск"
];

function autocomplete(inp, arr) {
    let currentFocus;

    inp.addEventListener("input", function(e) {
        let val = this.value;
        closeAllLists();
        if (!val) return false;
        currentFocus = -1;

        const a = document.createElement("DIV");
        a.style.width = "250px";
        a.style.whiteSpace = "nowrap";
        a.style.overflowX = "hidden";
        a.setAttribute("id", this.id + "-autocomplete-list");
        a.setAttribute("class", "autocomplete-items");
        this.parentNode.appendChild(a);

        for (let i = 0; i < arr.length; i++) {
            if (arr[i].substr(0, val.length).toUpperCase() === val.toUpperCase()) {
                const b = document.createElement("DIV");
                b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
                b.innerHTML += arr[i].substr(val.length);
                b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
                b.addEventListener("click", function(e) {
                    inp.value = this.getElementsByTagName("input")[0].value;
                    closeAllLists();
                });
                a.appendChild(b);
            }
        }
    });

    inp.addEventListener("keydown", function(e) {
        let x = document.getElementById(this.id + "-autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode === 40) { // Arrow Down
            currentFocus++;
            addActive(x);
        } else if (e.keyCode === 38) { // Arrow Up
            currentFocus--;
            addActive(x);
        } else if (e.keyCode === 13) { // Enter
            e.preventDefault();
            if (currentFocus > -1 && x) x[currentFocus].click();
        }
    });

    function addActive(x) {
        if (!x) return false;
        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (x.length - 1);
        x[currentFocus].classList.add("autocomplete-active");
    }

    function removeActive(x) {
        for (let i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }

    function closeAllLists(elmnt) {
        const x = document.getElementsByClassName("autocomplete-items");
        for (let i = 0; i < x.length; i++) {
            if (elmnt !== x[i] && elmnt !== inp) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }

    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });
}

document.addEventListener("DOMContentLoaded", function() {
    const city1Input = document.getElementById("extra-city1");
    const city2Input = document.getElementById("extra-city2");
    if (city1Input) autocomplete(city1Input, cities);
    if (city2Input) autocomplete(city2Input, cities);
});