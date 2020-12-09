## -*- coding: utf-8 -*-


<!-- Load line.js -->
<script type="text/javascript" src="/include/javascript/chart-scripts/linechart.js"></script>
<link rel="stylesheet" type="text/css" href="/include/css/chart-scripts/linechart-line.css" />
<!-- Load histogram.js -->
<script type="text/javascript" src="/include/javascript/chart-scripts/histogram.js"></script>
<link rel="stylesheet" type="text/css" href="/include/css/chart-scripts/histogram.css" />
<!-- load meta data render function -->
<script type="text/javascript" src="/include/javascript/templates/tr_periods.js"></script>

<script type="text/javascript">
	var dateObj = new Date();
	var todayString = dateObj.getFullYear()+'-'+(dateObj.getMonth()+1)+'-'+dateObj.getDate();

	$( document ).ready(function()
	{
		$('.fileListSelect').change(function()
		{
			$('#isciForma').submit();
		});

		$('.draw-histogram-chart').click(function()
		{
			handleTabs('histogram');
			drawHistogram();
		});
		$('.draw-line-chart').click(function()
		{
			handleTabs('line');
			drawLineChart();
		});

		drawLineChart();
	});

	function handleTabs(type)
	{
		$('.switch_tab').removeClass('tab_active');
		$('.switch_tab').addClass('tab_passive');
		$('.draw-' + type + '-chart').removeClass('tab_passive');
		$('.draw-' + type + '-chart').addClass('tab_active');
	}

	function drawLineChart()
	{
		console.log('plotting line chart');

		// reset chart box
		// reset chart box

		$('#chart-plot').html('');
		$('#chart-plot-meta').html('Select a bar.');

		// init chart
		// init chart

		var lineChartObj = lineChart()
			.width(960)
			.height(500)
			.xLabel('Date')
			.yLabel('Anomalies, cumulative number')
			.xValueFieldName('date')
			.yValueFieldName('value')
			.xScaleType('time');
			//.metaHtmlElement('#chart-plot-meta')
			//.metaFunctionExternal('renderDataFormat');

		d3.tsv("${data['tsv_file_timeline']}?" + todayString).then(function(data)
		{
			// casting data
			// casting data

			//var alldata = [];
		    data.forEach(function(d) {
				d.value = parseInt(d.value);
				dateArray = d.date.split('-');
				year = parseInt(dateArray[0])
				month = parseInt(dateArray[1])
				d.date = new Date(year, month, 01)
				//if(d.value > 0)
				//	alldata.push(d);
        	});
        	//data = alldata;

        	// data ready, draw chart
        	// data ready, draw chart

			d3.select('#chart-plot')
				.datum(data) // bind data to the div
				.call(lineChartObj); // draw chart in div
		});
	}

	function drawHistogram()
	{
		console.log('plotting histogram');

		// reset chart box
		// reset chart box

		$('#chart-plot').html('');
		$('#chart-plot-meta').html('Select a bar.');

		// create chart
		// create chart

		var histogram = histogramChart()
			.numBins(50)
			.width(980)
			.height(400)
			.xLabel('anomaly measure')
			.yLabel('num of companies')
			.valueFieldName('score')
			.metaHtmlElement('#chart-plot-meta')
			.metaFunctionExternal('renderDataFormatAjpes');

		d3.tsv("${data['tsv_file_companies']}?" + todayString).then(function(data)
		{
			// casting data
			// casting data

		    data.forEach(function(d) {
				d.score = parseFloat(d.score);
        	});

        	// data ready, draw chart
        	// data ready, draw chart

			d3.select('#chart-plot')
				.datum(data) // bind data to the div
				.call(histogram); // draw chart in div
		});
	}
</script>

<div id="tr_periods">
	<div class="pas_rumen text_title">
		PERIOD MARGIN
	</div>
	<br />

	<div class="container-fluid">
		${data['transactionsMenu']}

		<br /><br />
		<div>
			Here we are defining a financial transaction as a base relation between two entities (public sector entity and business entity). Based on this, we detect relation periods (when relation started or ended) and accumulate starting/ending periods on a timeline. Based on cumulative relation period extremes, we identify deviations and list entities as part of identified extremes.
		</div>
	</div>
	<br /><br />

	<div class="tab_section">
		<div class="container-fluid">
			<div class="draw-line-chart tab_common tab_active switch_tab">Timeline</div>
			<div class="draw-histogram-chart tab_common tab_passive switch_tab">Anomalies</div>
			<div class="clearfix"></div>
		</div>
	</div>
	<br />

	<div class="container-fluid">
		<form id="isciForma" method="get" action="">
			<input type="hidden" name="m" value="transactions" />
			<input type="hidden" name="a" value="periods" />

			<select name="idfile" class="fileListSelect">
				<option value="">Select classificator</option>
				%for classificator in data["skdDict"]:
					<option value="${classificator}" ${'selected="selected"' if data["idfile"] == classificator else ''}>
						[${classificator}]
						${data["skdDict"][classificator]}
					</option>
				%endfor
			</select>
		</form>
		<br /><br /><br />

		<!-- Create a div where the graph will take place -->
		<div id="chart-plot" class="text-center"></div>
		<br />
		<div id="chart-plot-meta" class="text-center">
			Select a bar.
		</div>
	</div>
	<br /><br />
</div>
