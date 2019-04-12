var scoreChart;
var pressureChart;

var $ = window.$;
var c = window.jQuery;

$(document).ready(function() {
    $('.select2').select2({
	    minimumResultsForSearch: Infinity
	});

	var scoreCanvas = $("#score-canvas");
	scoreChart = new Chart(scoreCanvas, {
	    type: 'line',
	    data: {
	    	// initialize empty for later loading via AJAX
			labels: [1,2,3,4],
			datasets: [[]]
		},
		options: {
			animation: {
	            duration: 0, // general animation time
	        },
	        responsiveAnimationDuration: 0, // animation duration after a resize
			responsive: true,
			tooltips: {
				mode: 'index',
				intersect: false,
			},
			hover: {
				mode: 'nearest',
				intersect: true,
				animationDuration: 0, // duration of animations when hovering an item
			},
			scales: {
				xAxes: [{
					display: true,
					scaleLabel: {
						display: true,
						labelString: 'Time'
					}
				}],
				yAxes: [{
					display: true,
					scaleLabel: {
						display: true,
						labelString: 'Score'
					}
				}]
			}
		}
	});

	var pressureCanvas = $("#pressure-canvas");
	pressureChart = new Chart(pressureCanvas, {
	    type: 'line',
	    data: {
	    	// initialize empty for later loading via AJAX
			labels: [],
			datasets: [[]]
		},
		options: {
			animation: {
	            duration: 0, // general animation time
	        },
	        responsiveAnimationDuration: 0, // animation duration after a resize
			responsive: true,
			tooltips: {
				mode: 'index',
				intersect: false,
			},
			hover: {
				mode: 'nearest',
				intersect: true,
				animationDuration: 0, // duration of animations when hovering an item
			},
			scales: {
				xAxes: [{
					display: true,
					scaleLabel: {
						display: true,
						labelString: 'Time'
					}
				}],
				yAxes: [{
					display: true,
					ticks: {
						beginAtZero: true,
					},
					scaleLabel: {
						display: true,
						labelString: 'Voltage'
					}
				}]
			}
		}
	});
	poll();
});

function poll() {
    var timeout = 1000;
    update();
    window.setTimeout(function() { poll(); }, timeout);
}

function update() {
	var minutes = $("#minutes-select").val();
	$.ajax("/data/", {
		datatype: 'json',
		data: 'minutes=' + minutes
	}).done(function(data) {

		var results = JSON.parse(data);
		if(results && results.latest) {

			latest = results.latest;
			average = results.average;

			labels = results.labels;
			
			backScoreData = results.back_score_data;
			seatScoreData = results.seat_score_data;
			
			backLeftData = results.back_left_data;
			backRightData = results.back_right_data;
			backBottomData = results.backBottom_data;
			seatLeftData = results.seat_left_data;
			seatRightData = results.seat_right_data;
			seatRearData = results.seatRear_data;

			updateText("cur", latest);
			
			updateText("avg", average);

			updateCharts(labels, backScoreData, seatScoreData, backLeftData, backRightData,
				backBottomData, seatLeftData, seatRightData, seatRearData);

		} else {
			// fill with 0 if no data
			updateText("cur", {
				"backScore": 0,
				"seatScore": 0,
				"classification": "_____",
				"feedback": "",
				"backLeft": 0,
				"backRight": 0,
				"backBottom": 0,
				"seatLeft": 0,
				"seatRight": 0,
				"seatRear": 0
			});
			updateText("avg", {
				"backScore": 0,
				"seatScore": 0,
				"classification": "_____",
				"feedback": "",
				"backLeft": 0,
				"backRight": 0,
				"backBottom": 0,
				"seatLeft": 0,
				"seatRight": 0,
				"seatRear": 0
			});
		}
	});
}

function updateText(type, dataset) {

	backScore = dataset.back_score;
	seatScore = dataset.seat_score;
	classification = dataset.classification;
	feedback = dataset.feedback;

	backLeft = dataset.back_left;
	backRight = dataset.back_right;
	backBottom = dataset.back_bottom;
	seatLeft = dataset.seat_left;
	seatRight = dataset.seat_right;
	seatRear = dataset.seat_rear;
	
	$("." + type + ".back-score").text(formatPressure(backScore));
	$("." + type + ".seat-score").text(formatPressure(seatScore));

	$("." + type + ".pressure.back-left-pressure").text(formatPressure((backLeft / 1023) * 100) + "%");
	$("." + type + ".pressure.back-right-pressure").text(formatPressure((backRight / 1023) * 100) + "%");
	$("." + type + ".pressure.back-bottom-pressure").text(formatPressure((backBottom / 1023) * 100) + "%");
	$("." + type + ".pressure.seat-left-pressure").text(formatPressure((seatLeft / 1023) * 100) + "%");
	$("." + type + ".pressure.seat-right-pressure").text(formatPressure((seatRight / 1023) * 100) + "%");
	$("." + type + ".pressure.seat-rear-pressure").text(formatPressure((seatRear / 1023) * 100) + "%");
	$("." + type + ".overall").text(classification);
	$("." + type + ".feedback").text(feedback);

	// remove existing styling, then replace with good/bad based on new value
	$("." + type + ".overall").removeClass("overall-bad");
	$("." + type + ".overall").removeClass("overall-good");
	
	if(classification.toLowerCase().includes("bad"))
		$("." + type + ".overall").addClass("overall-bad");
	else
		$("." + type + ".overall").addClass("overall-good");



	// var feedback = "N/A";

	// if (backScore > 0 && backScore < 30 && seatScore > 0 && seatScore < 30) {
	// 	feedback = "Looking Good!";
	// } else if (backScore > 0 && backScore < 30) {
	// 	if (seatLeft > 1.5 * seatRight)
	// 		feedback = "Your weight is unbalanced to the left of the seat.";
	// 	else if (seatRight > 1.5 * seatLeft)
	// 		feedback = "Your weight is unbalanced to the right of the seat.";
	// } else if (seatScore > 0 && seatScore < 30) {
	// 	if (backLeft > 1.5 * backBottom && backRight > 1.5 * backBottom)
	// 		feedback = "Your upper back is against the backrest but your lower back is not. Try not to arch your back.";
	// 	else if (backBottom > 1.5 * backLeft && backBottom > 1.5 * backRight)
	// 		feedback = "Your lower back is against the backrest but your upper back is not. Make sure to sit up straight.";
	// }
}

function formatPressure(pressure) {
	// if there's a decimal, cap the length at two past the decimal
	var str = "" + pressure;
	var decimal = str.indexOf(".");
	var res = decimal == -1 ? str : str.substring(0, decimal + 3);
	return Number(res);
}

function updateCharts(labels, bScore, sScore, bLeft, bRight, bBottom, sLeft, sRight, sRear) {

	scoreChart.data.labels = labels;
	scoreChart.data.datasets = [{
		label: "Backrest Score",
		backgroundColor: "red",
			borderColor: "red",
			data: bScore,
			fill: false
	}, {
		label: "Seat Score",
		backgroundColor: "blue",
			borderColor: "blue",
			data: sScore,
			fill: false
	}];

	scoreChart.update();

	pressureChart.data.labels = labels;
	pressureChart.data.datasets = [{
		label: "Back Left",
		backgroundColor: "red",
			borderColor: "red",
			data: bLeft,
			fill: false
	}, {
		label: "Back Right",
		backgroundColor: "blue",
			borderColor: "blue",
			data: bRight,
			fill: false
	}, {
		label: "Lower Back",
		backgroundColor: "green",
			borderColor: "green",
			data: bBottom,
			fill: false
	}, {
		label: "Seat Left",
		backgroundColor: "purple",
			borderColor: "purple",
			data: sLeft,
			fill: false
	}, {
		label: "Seat Right",
		backgroundColor: "brown",
			borderColor: "brown",
			data: sRight,
			fill: false
	}, {
		label: "Seat Rear",
		backgroundColor: "orange",
			borderColor: "orange",
			data: sRear,
			fill: false
	}];

	pressureChart.update();
}