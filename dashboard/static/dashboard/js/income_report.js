window.onload = function() {	var ctx = document.getElementById('canvas').getContext('2d');	var monS1 = document.getElementById('_labels').value;	var x2 = document.getElementById('_x2').value;	var x1 = document.getElementById('_x1').value;	var res = x2.split("[");	var res = res[1].split("]");	var res = res[0].split(",");	var x3 =[]	for (i = 0; i < res.length; i++) {	 x3[i] = parseFloat(res[i]) 	}		var res = x1.split("[");	var res = res[1].split("]");	var res = res[0].split(",");	var x4 =[]	for (i = 0; i < res.length; i++) {	 x4[i] = parseFloat(res[i])	}			var res = monS1.split("[");	var res = res[1].split("]");	var res = res[0].split(",");	var monS =[]	for (i = 0; i < res.length; i++) {	 monS[i] = res[i]     var monS2 = monS[i].split("'")	 monS[i] = monS2[1]	 	}		//alert(x3)	//alert(x4)	//alert(monS)		var myLineChart = new Chart(ctx, {		type: 'line',		data: {			labels: monS,			datasets: [{				label: 'Income',				data:x4,				showLine: true,								borderColor: window.chartColors.gray,			    backgroundColor: window.chartColors.gray,				fill: true,				borderWidth: 1,							},{				label: 'Expenses',				data:x3,				borderDash: [10,10],				borderColor: window.chartColors.red,				backgroundColor: window.chartColors.red,				fill: false,				borderWidth: 2						}]		},		options: {			responsive: true,			animation: {				duration: 10 // general animation time			},			interaction: {				mode: 'index'			},			stacked: true,			plugins: {				title: {					display: true,					text: 'Chart.js Line Chart - Multi Axis'				}			},			scales: {					xAxes: [{						type: 'category',						//labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'jul','Aug','Sep','Oct','Nov','Dec' ]						labels: monS					}]				}		}	});};		