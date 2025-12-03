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

function autocomplete(inputElement, cityList) {
    let currentFocusIndex;

    inputElement.addEventListener("input", function(event) {
        let currentInputValue = this.value;
        closeAllLists();
        if (!currentInputValue) return false;
        currentFocusIndex = -1;

        const suggestionsContainer = document.createElement("DIV");
        suggestionsContainer.style.width = "250px";
        suggestionsContainer.style.whiteSpace = "nowrap";
        suggestionsContainer.style.overflowX = "hidden";
        suggestionsContainer.setAttribute("id", this.id + "-autocomplete-list");
        suggestionsContainer.setAttribute("class", "autocomplete-items");
        this.parentNode.appendChild(suggestionsContainer);

        for (let i = 0; i < cityList.length; i++) {
            if (cityList[i].substr(0, currentInputValue.length).toUpperCase() === currentInputValue.toUpperCase()) {
                const suggestionItem = document.createElement("DIV");
                suggestionItem.innerHTML = "<strong>" + cityList[i].substr(0, currentInputValue.length) + "</strong>";
                suggestionItem.innerHTML += cityList[i].substr(currentInputValue.length);
                suggestionItem.innerHTML += "<input type='hidden' value='" + cityList[i] + "'>";
                suggestionItem.addEventListener("click", function(event) {
                    inputElement.value = this.getElementsByTagName("input")[0].value;
                    closeAllLists();
                    inputElement.dispatchEvent(new Event('input', { bubbles: true}));
                });
                suggestionsContainer.appendChild(suggestionItem);
            }
        }
    });

    inputElement.addEventListener("keydown", function(event) {
        let suggestionsList = document.getElementById(this.id + "-autocomplete-list");
        if (suggestionsList) suggestionsList = suggestionsList.getElementsByTagName("div");
        if (event.keyCode === 40) { // Arrow Down
            currentFocusIndex++;
            addActive(suggestionsList);
        } else if (event.keyCode === 38) { // Arrow Up
            currentFocusIndex--;
            addActive(suggestionsList);
        } else if (event.keyCode === 13) { // Enter
            event.preventDefault();
            if (currentFocusIndex > -1 && suggestionsList) suggestionsList[currentFocusIndex].click();
        }
    });

    function addActive(items) {
        if (!items) return false;
        removeActive(items);
        if (currentFocusIndex >= items.length) currentFocusIndex = 0;
        if (currentFocusIndex < 0) currentFocusIndex = (items.length - 1);
        items[currentFocusIndex].classList.add("autocomplete-active");
    }

    function removeActive(items) {
        for (let i = 0; i < items.length; i++) {
            items[i].classList.remove("autocomplete-active");
        }
    }

    function closeAllLists(clickedElement) {
        const x = document.getElementsByClassName("autocomplete-items");
        for (let i = 0; i < x.length; i++) {
            if (clickedElement !== x[i] && clickedElement !== inputElement) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }

    document.addEventListener("click", function (event) {
        closeAllLists(event.target);
    });
}

document.addEventListener("DOMContentLoaded", function() {
    const city1Input = document.getElementById("extra-city1");
    const city2Input = document.getElementById("extra-city2");
    if (city1Input) autocomplete(city1Input, cities);
    if (city2Input) autocomplete(city2Input, cities);
});