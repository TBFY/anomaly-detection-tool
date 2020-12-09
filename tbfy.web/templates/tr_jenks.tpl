## -*- coding: utf-8 -*-

<!-- Load histogram.js -->
<script type="text/javascript" src="/include/javascript/chart-scripts/histogram.js"></script>
<link rel="stylesheet" type="text/css" href="/include/css/chart-scripts/histogram.css" />
<!-- load meta data render function -->
<script type="text/javascript" src="/include/javascript/templates/tr_jenks.js"></script>

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
			.numBins(50)
			.width(980)
			.height(400)
			.xLabel('anomaly measure')
			.yLabel('num of companies')
			.valueFieldName('deviation')
			.metaHtmlElement('#histogram-plot-meta')
			.metaFunctionExternal('renderDataFormatAjpes');

		d3.tsv("${data['tsv_file_source']}?" + todayString).then(function(data)
		{
			// casting data
			// casting data

		    data.forEach(function(d) {
				d.deviation = parseFloat(d.deviation);
        	});

        	// data ready, draw chart
        	// data ready, draw chart

			d3.select('#histogram-plot')
				.datum(data) // bind data to the div
				.call(histogram); // draw chart in div
		});
	}
</script>

<div id="tr_jenks">
	<div class="pas_rumen text_title">
		1D CLUSTERING
	</div>
	<br />

	<div class="container-fluid">
		${data['transactionsMenu']}

		<br /><br />
		<div>
			The method organizes transaction sums into an optimal number of clusters and define deviations within each cluster separately. Therefore, this method performes data clustering in order to determine the best arrangement of values into different classes. The method is seeking to minimize each class’s average deviation from the class mean and at the same time it is maximizing each class’s deviation from the means of the other groups. So method cluster data in a manner that it reduces the variance within classes and maximize the variance between classes.
		</div>
		<br /><br />

		<form id="isciForma" method="get" action="">
			<input type="hidden" name="m" value="transactions" />
			<input type="hidden" name="a" value="jnks" />
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




