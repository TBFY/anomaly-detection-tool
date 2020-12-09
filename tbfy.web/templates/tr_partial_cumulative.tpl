## -*- coding: utf-8 -*-

<!-- Load histogram.js -->
<script type="text/javascript" src="/include/javascript/chart-scripts/histogram.js"></script>
<link rel="stylesheet" type="text/css" href="/include/css/chart-scripts/histogram.css" />
<!-- load meta data render function -->
<script type="text/javascript" src="/include/javascript/templates/tr_partial_cumulative.js"></script>

<script type="text/javascript">
	var dateObj = new Date();
	var todayString = dateObj.getFullYear()+'-'+(dateObj.getMonth()+1)+'-'+dateObj.getDate();

	$( document ).ready(function()
	{
		$('.fileListSelect').change(function()
		{
			$('#isciForma').submit();
		});

		drawChart();
	});

	function drawChart()
	{
		// reset chart box
		// reset chart box

		console.log('plotting chart');

		// reset chart box
		// reset chart box

		$('#histogram-plot').html('');

		// create chart
		// create chart

		var histogram = histogramChart()
			.numBins(100)
			.width(980)
			.height(400)
			.xLabel('anomaly measure')
			.yLabel('num of companies')
			.valueFieldName('score')
			.metaHtmlElement('#histogram-plot-meta')
			.metaFunctionExternal('renderDataFormatAjpes');

		d3.tsv("${data['tsv_file_source']}?" + todayString).then(function(data)
		{
			// casting data
			// casting data

		    data.forEach(function(d) {
				d.score = parseInt(d.score);
        	});

        	// data ready, draw chart
        	// data ready, draw chart

			d3.select('#histogram-plot')
				.datum(data) // bind data to the div
				.call(histogram); // draw chart in div
		});
	}
</script>

<div id="tr_partial">
	<div class="pas_rumen text_title">
		PARTIAL CUMULATIVES
	</div>
	<br />

	<div class="container-fluid">
		${data['transactionsMenu']}

		<br /><br />
		<div>
			In this method's approach, we first define transaction sums for all related entities and normalize sums with the total transactions sum. In such way this method defines a comparison baseline. Then, it takes transactions between entities and sums them into a predefined number of periods. For each period partial sums weights are compared to the baseline weights and anomalies are identified. The more anomalous a company behaves the higher it ranks on the anomalous list. The purpose of the method is to identify the biggest changes within the series of accumulated periods.
		</div>
		<br /><br />

		<form id="isciForma" method="get" action="">
			<input type="hidden" name="m" value="transactions" />
			<input type="hidden" name="a" value="part" />
			<input type="hidden" name="t" value="${data['pageAddress']}" />

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
		<div id="histogram-plot" class="text-center"></div>
		<br />
		<div id="histogram-plot-meta" class="text-center">
			Select a bar.
		</div>
	</div>
	<br /><br />
</div>
