## -*- coding: utf-8 -*-

<!-- Load histogram.js -->
<script type="text/javascript" src="/include/javascript/chart-scripts/histogram.js"></script>
<link rel="stylesheet" type="text/css" href="/include/css/chart-scripts/histogram.css" />
<!-- load meta data render function -->
<script type="text/javascript" src="/include/javascript/templates/te_dependencies.js"></script>

<script type="text/javascript">
	var dateObj = new Date();
	var todayString = dateObj.getFullYear()+'-'+(dateObj.getMonth()+1)+'-'+dateObj.getDate();

	$( document ).ready(function()
	{
		$('.fileListSelect').change(function()
		{
			$('#isciForma').submit();
		});

		$('.read-more').click(function()
		{
			if($('.explanation-chart-all').is(":visible"))
			{
				$('.read-more-all').hide();
				$('.read-less-all').show();
				$('.read-more-div-all').show(100);
			}
		});
		$('.read-less').click(function()
		{
			if($('.explanation-chart-all').is(":visible"))
			{
				$('.read-more-all').show();
				$('.read-less-all').hide();
				$('.read-more-div-all').hide(100);
			}
		});

		drawDependencyChart();
	});

	function drawDependencyChart()
	{
		console.log('all data');

		// reset chart box
		// reset chart box

		$('#chart-frame').html('');

		// create chart
		// create chart

		var renderFunction = 'renderDataFormatKG';
		if('${data["dataSourceLstSelected"]}' == 'si-ministry')
			renderFunction = 'renderDataFormatMJU';

		var histogram = histogramChart()
			.numBins(100)
			.width(960)
			.height(500)
			.xLabel('Anomaly measure: the closer the value to 1.0, the more company exhibits unwanted behaviour')
			.yLabel('Number of companies')
			.valueFieldName('share')
			.metaHtmlElement('#chart-frame-meta')
			.metaFunctionExternal(renderFunction);

		// draw chart
		// draw chart

		d3.tsv("${data['tsvDependenicesFilePath']}?" + todayString).then(function(data)
		{
			var datalength = data.length;

			// filter data
			// filter data

			dataArray = [];
			var curObj;
			var data_i = 0;

			for (let i = 0; i < datalength; i++)
			{
				curObj = data[i];

				// cast data
				curObj.y_value = parseFloat(curObj.y_value);

				// add data to list
				dataArray.push(curObj);
				//if(data_i == max_i) break;
				//else data_i++;
			}

			// data ready, draw chart
			// data ready, draw chart

			d3.select('#chart-frame')
				.datum(dataArray) // bind data to the div
				.call(histogram); // draw chart in div
		});
	}
</script>

<div id="te_statistical_approach">

	<div class="pas_rumen text_title">
		TENDERS, STATISTICAL APPROACH
	</div>
	<br />
	${data['tenderMenu']}
	<br />

	<div class="container-fluid">
		This visualizaton shows the dependency of either a contracting authority towards a economic operator or vice vesa. It is an unwanted behavior because one would expect a greater diversity in distribution between tenders won by a particular economic operator.
		<br /><br /><br />
		<div>${data['dependencieDescHTML']}</div>
		<br /><br />

		<div id="chart-frame" class="chart-frame"></div>
		<br />
		<div id="chart-frame-meta">Select a bar.</div>
	</div>
	<br /><br />
</div>
