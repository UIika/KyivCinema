resetCalendar();
let seats = document.querySelector(".all-seats");
for (var i = 0; i < 90; i++) {
    seats.insertAdjacentHTML(
        "beforeend",
        '<input type="checkbox" name="tickets" id="s' + i + '" />\
        <label for="s' + i + '" class="seat" id="label' + i + '"></label>'
    );
}


var amount = document.querySelector(".amount").innerHTML;
var price;

checkedTickets = new Set();
let tickets = seats.querySelectorAll("input[type=checkbox]");
tickets.forEach((ticket) => {
    ticket.addEventListener("change", () => {
        let amount = document.querySelector(".amount").innerHTML;
        let count = document.querySelector(".count").innerHTML;
        amount = Number(amount);
        count = Number(count);
        
        if (ticket.checked) {
            count += 1;
            amount += price;
            checkedTickets.add(ticket.id);
            ticket.checked = true;
        } else {
            count -= 1;
            amount -= price;
            checkedTickets.delete(ticket.id);
            ticket.checked = false;
        }
        document.querySelectorAll(".amount")[0].innerHTML = amount;
        document.querySelectorAll(".amount")[1].innerHTML = amount;
        document.querySelector(".count").innerHTML = count;
    });
});

function getSelectedRadio() {
    var form = document.getElementById('timeForm');
    var radios = form.elements['time'];
    var selectedRadio;
    for (var i = 0; i < radios.length; i++) {
        if (radios[i].checked) {
            selectedRadio = radios[i];
            break;
        }
    }
    return selectedRadio;
}

var time;
var date;
var movie_id;

function resetCalendar() {
    var tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    var tomorrowISOString = tomorrow.toISOString().substring(0, 10);
    document.getElementById("date").value = tomorrowISOString;
    document.getElementById("date").setAttribute("min", document.getElementById("date").value);
    date = tomorrowISOString;
}

function updateSeats() {
    document.querySelector(".amount").innerHTML = 0;
    document.querySelector(".count").innerHTML = 0;
    checkedTickets = new Set();
    date = document.getElementById("date").value;
    if (date == "") {
        resetCalendar();
    }
    time = getSelectedRadio().value;
    switch (time){
        case "11:00:00":
            price = 140;
            break;
        case "14:30:00":
            price = 160;
            break;
        case "18:00:00":
            price = 200;
            break;
        case "21:30:00":
            price = 180;
            break;
    }
    movie_id = document.head.querySelector("[property~=movieId][content]").content;
    $.ajax({
        url: `/getCurrentSession/${movie_id}/${date}_${time}/`,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            for (var i = 0; i < 90; i++) {
                if (data[i] == 1) {
                    $(document.getElementById(`label${i}`)).addClass("booked");
                    document.getElementById(`s${i}`).checked = true;
                } else
                    $(document.getElementById(`label${i}`)).removeClass("booked");
                document.getElementById(`s${i}`).checked = false;

            }
        },
        error: function (xhr, status, error) {

            console.error(error);
        }
    });
}

$(document).ready(function () {
    $('#date').change(updateSeats); // Срабатывание при изменении даты
    $('#buyButton').click(updateSeats); // Срабатывание при нажатии на другую кнопку
    $('input[name="time"]').change(updateSeats); // Срабатывание при изменении значения радиокнопки
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

paymentSubmitButton = document.getElementById("paymentSubmitButton");

paymentSubmitButton.addEventListener("click", () => {
    $.ajax({
        type: "POST",
        url: `/buyTickets/${movie_id}/${date}_${time}/`,
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: {
            'data': Array.from(checkedTickets),
        },
        success: function (response) {
            location.reload();
        },
    });
});

const outputElement = document.getElementById('liveSearchResults')

jQuery(document).ready(function ($) {
	$('.live-search-list li').each(function () {
		$(this).attr('data-search-term', $(this).text().toLowerCase())
	})

	$('.live-search-box').on('keyup', function () {
		var searchTerm = $(this).val().toLowerCase()
		var visibleItems = 0

		$('.live-search-list li').each(function () {
			var text = $(this).attr('data-search-term')
			if (text.indexOf(searchTerm) !== -1 || searchTerm.length < 1) {
				outputElement.hidden = false
				if (visibleItems < 5) {
					$(this).show()
					visibleItems++
				} else {
					$(this).hide()
				}
			} else {
				$(this).hide()
			}
		})
		$('#liveSearchResults').each(function () {
			if (searchTerm.length < 1) {
				outputElement.hidden = true
			}
		})
	})
})