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

		var avgBackScore = 0;
		var avgSeatScore = 0;

		var avgBackLeft = 0;
		var avgBackRight = 0;
		var avgBackBottom = 0;
		var avgSeatLeft = 0;
		var avgSeatRight = 0;
		var avgSeatRear = 0;

		var labels = [];

		var backScoreData = [];
		var seatScoreData = [];

		var backLeftData = [];
		var backRightData = [];
		var backBottomData = [];
		var seatLeftData = [];
		var seatRightData = [];
		var seatRearData = [];

		// this isn't actually an array for some reason, but works similarly
		var rs = JSON.parse(data);
		var len = rs.length;
		
		if(rs != null && rs.length > 0) {
			// set the current values
			var latest = rs[0];
			updateText("cur", latest.back_score, latest.seat_score, latest.back_left, latest.back_right,
				latest.back_bottom, latest.seat_left, latest.seat_right, latest.seat_rear);

			// calculate averages and populate charts
			for(var i = 0; i < len; i++) {
				var element = rs[i];

				avgBackScore += element.back_score / len;
				avgSeatScore += element.seat_score / len;

				avgBackLeft += element.back_left / len;
				avgBackRight += element.back_right / len;
				avgBackBottom += element.back_bottom / len;
				avgSeatLeft += element.seat_left / len;
				avgSeatRight += element.seat_right / len;
				avgSeatRear += element.seat_rear / len;

				labels.push(element.timestamp);

				backScoreData.push(element.back_score);
				seatScoreData.push(element.seat_score);

				backLeftData.push(element.back_left);
				backRightData.push(element.back_right);
				backBottomData.push(element.back_bottom);
				seatLeftData.push(element.seat_left);
				seatRightData.push(element.seat_right);
				seatRearData.push(element.seat_rear);
			}
			
			updateText("avg", avgBackScore, avgSeatScore, avgBackLeft, avgBackRight, avgBackBottom, avgSeatLeft, avgSeatRight, avgSeatRear);

			updateCharts(labels, backScoreData, seatScoreData, backLeftData, backRightData,
				backBottomData, seatLeftData, seatRightData, seatRearData);

		} else {
			updateText("cur", 0, 0, 0, 0, 0, 0, 0, 0);
			updateText("avg", 0, 0, 0, 0, 0, 0, 0, 0);
		}
	});
}

function updateText(type, backScore, seatScore, backLeft, backRight, backBottom, seatLeft, seatRight, seatRear) {
	$("." + type + ".back-score").text(formatPressure(backScore));
	$("." + type + ".seat-score").text(formatPressure(seatScore));

	$("." + type + ".pressure.back-left-pressure").text(formatPressure(backLeft));
	$("." + type + ".pressure.back-right-pressure").text(formatPressure(backRight));
	$("." + type + ".pressure.back-bottom-pressure").text(formatPressure(backBottom));
	$("." + type + ".pressure.seat-left-pressure").text(formatPressure(seatLeft));
	$("." + type + ".pressure.seat-right-pressure").text(formatPressure(seatRight));
	$("." + type + ".pressure.seat-rear-pressure").text(formatPressure(seatRear));
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
		label: "",
		backgroundColor: "red",
			borderColor: "red",
			data: bLeft,
			fill: false
	}, {
		label: "",
		backgroundColor: "blue",
			borderColor: "blue",
			data: bRight,
			fill: false
	}, {
		label: "",
		backgroundColor: "green",
			borderColor: "green",
			data: bBottom,
			fill: false
	}, {
		label: "",
		backgroundColor: "purple",
			borderColor: "purple",
			data: sLeft,
			fill: false
	}, {
		label: "",
		backgroundColor: "#003f5c",
			borderColor: "#003f5c",
			data: sRight,
			fill: false
	}, {
		label: "",
		backgroundColor: "orange",
			borderColor: "orange",
			data: sRear,
			fill: false
	}];

	pressureChart.update();
}