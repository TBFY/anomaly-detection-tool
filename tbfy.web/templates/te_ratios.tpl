## -*- coding: utf-8 -*-

<!-- Load line.js -->
<script type="text/javascript" src="/include/javascript/chart-scripts/linechart.js?v=1"></script>
<link rel="stylesheet" type="text/css" href="/include/css/chart-scripts/linechart.css?v=1" />
<!-- Load histogram.js -->
<script type="text/javascript" src="/include/javascript/chart-scripts/histogram.js"></script>
<link rel="stylesheet" type="text/css" href="/include/css/chart-scripts/histogram.css" />
<!-- load meta data render function -->
<script type="text/javascript" src="/include/javascript/templates/${data['jsMetaDataRenderFunction']}"></script>

<script type="text/javascript">
	var dateObj = new Date();
	var todayString = dateObj.getFullYear()+'-'+(dateObj.getMonth()+1)+'-'+dateObj.getDate();

	$( document ).ready(function()
	{
		$('.switch_tab').click(function()
		{
			$('.switch_tab').removeClass('tab_active');
			$('.switch_tab').addClass('tab_passive');
			$(this).removeClass('tab_passive');
			$(this).addClass('tab_active');
			$('#chart-frame-meta').html('Select a bar.');

			// add graph
			var tid = $(this).attr('id');
			if(tid == 'graph_tab')
			{
				drawAllRatioChart();
				$('.explanation-chart').hide();
				$('.explanation-chart-all').show();
				$('#chart-frame-meta').html('');
			}
			else if(tid == 'positives_tab')
			{
				drawPosDevChart();
				$('.explanation-chart').hide();
				$('.explanation-chart-pos').show();
			}
			else if(tid == 'negatives_tab')
			{
				drawNegDevChart();
				$('.explanation-chart').hide();
				$('.explanation-chart-neg').show();
			}
		});

		$('.dataarraylimit').focusout(function()
		{
			if($(this).hasClass('dataarraylimit-neg'))
				drawNegDevChart();
			if($(this).hasClass('dataarraylimit-pos'))
				drawPosDevChart();
		});

		$('.cpvcode').focusout(function()
		{
			if($('.dataarraylimit-neg').is(":visible"))
				drawNegDevChart();
			if($('.dataarraylimit-pos').is(":visible"))
				drawPosDevChart();
		});

		$('.datasource').change(function()
		{
			$('#datasourceform').submit();
		});

		$('.read-more').click(function()
		{
			if($('.explanation-chart-all').is(":visible"))
			{
				$('.read-more-all').hide();
				$('.read-less-all').show();
				$('.read-more-div-all').show(100);
			}
			if($('.explanation-chart-pos').is(":visible"))
			{
				$('.read-more-pos').hide();
				$('.read-less-pos').show();
				$('.read-more-div-pos').show(100);
			}
			if($('.explanation-chart-neg').is(":visible"))
			{
				$('.read-more-neg').hide();
				$('.read-less-neg').show();
				$('.read-more-div-neg').show(100);
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
			if($('.explanation-chart-pos').is(":visible"))
			{
				$('.read-more-pos').show();
				$('.read-less-pos').hide();
				$('.read-more-div-pos').hide(100);
			}
			if($('.explanation-chart-neg').is(":visible"))
			{
				$('.read-more-neg').show();
				$('.read-less-neg').hide();
				$('.read-more-div-neg').hide(100);
			}
		});

		drawAllRatioChart();
	});

	function setChartCpvFilter()
	{
		$('.cpvcode').show();
		$('.cpvcode-text').show();
	}

	function drawPosDevChart()
	{
		console.log('pos dev plotting');
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
			.xLabel('Anomaly measure: higher values infers higher anomaly')
			.yLabel('Num of companies')
			.valueFieldName('y_value')
			.metaHtmlElement('#chart-frame-meta')
			.metaFunctionExternal(renderFunction);

		// draw chart
		// draw chart

		d3.tsv("${data['tsvPosDevPointsFilePath']}?" + todayString).then(function(data)
		{
			var datalength = data.length;

			// set cpv filter
			// set cpv filter

			setChartCpvFilter();
			cpvCode = $('.cpvcode').val();
			cpvCodeLength = cpvCode.length;

        	// setting data limit box
        	// setting data limit box

			$('.dataarraylimit-text').show();
        	$('.dataarraylimit-neg').hide();
        	$('.dataarraylimit-pos').show();

        	if($('.dataarraylimit-pos').val() == '')
        		$('.dataarraylimit-pos').val(datalength);

        	if ($('.dataarraylimit-pos').val() > datalength)
        		max_i = datalength;
        	else
        		max_i = $('.dataarraylimit-pos').val();

        	if(max_i > 10000) max_i = 10000;

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

				// filter data by cpv code
				if(cpvCodeLength > 0)
				{
					if(cpvCode != curObj.cpv.substr(0, cpvCodeLength))
						continue;
				}

				// add data to list
				dataArray.push(curObj);
				if(data_i == max_i) break;
				else data_i++;
			}

        	// data ready, draw chart
        	// data ready, draw chart

			d3.select('#chart-frame')
				.datum(dataArray) // bind data to the div
				.call(histogram); // draw chart in div
		});
	}

	function drawNegDevChart()
	{
		console.log('neg dev plotting');

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
			.xLabel('Anomaly measure: lower values infers higher anomaly')
			.yLabel('Num of companies')
			.valueFieldName('y_value')
			.metaHtmlElement('#chart-frame-meta')
			.metaFunctionExternal(renderFunction);

		d3.tsv("${data['tsvNegDevPointsFilePath']}?" + todayString).then(function(data)
		{
			var datalength = data.length;

        	// setting data limit box
        	// setting data limit box

			$('.dataarraylimit-text').show();
        	$('.dataarraylimit-pos').hide();
        	$('.dataarraylimit-neg').show();

        	if($('.dataarraylimit-neg').val() == '')
        		$('.dataarraylimit-neg').val(datalength);

        	if ($('.dataarraylimit-neg').val() > datalength)
        		max_i = datalength;
        	else
        		max_i = $('.dataarraylimit-neg').val();

        	if(max_i > 10000) max_i = 10000;

			// casting data
			// casting data

			dataArray = [];
			var curObj;
			for (let i = 0; i < max_i; i++)
			{
				curObj = data[datalength - i - 1];
				curObj.y_value = parseFloat(curObj.y_value);
				dataArray.push(curObj);
			}
        	// data ready, draw chart
        	// data ready, draw chart

			d3.select('#chart-frame')
				.datum(dataArray) // bind data to the div
				.call(histogram); // draw chart in div
		});
	}

	function drawAllRatioChart()
	{
		// reset chart box
		// reset chart box

		$('#chart-frame').html('');

		// init chart
		// init chart

		var lineChartObj = lineChart()
			.width(960)
			.height(500)
			.xLabel('Tenders sorted by ratio')
			.yLabel('Ratio, log scale')
			.xValueFieldName('x_value')
			.yValueFieldName('y_value');
			//.metaHtmlElement('#histogram-plot-meta')
			//.metaFunctionExternal('renderDataFormat');

		d3.tsv("${data['tsvAllRatioPointsFilePath']}?" + todayString).then(function(data)
		{
			// casting data
			// casting data

		    data.forEach(function(d) {
				d.x_value = parseInt(d.x_value);
				d.y_value = parseFloat(d.y_value);
        	});

        	// set cpv filter
        	// set cpv filter

        	$('.cpvcode').hide();
			$('.cpvcode-text').hide();

        	// setting data limit box
        	// setting data limit box

        	$('.dataarraylimit').hide();
        	$('.dataarraylimit-text').hide();

        	// data ready, draw chart
        	// data ready, draw chart

			d3.select('#chart-frame')
				.datum(data) // bind data to the div
				.call(lineChartObj); // draw chart in div
		});
	}
</script>

<style type="text/css">
	#te_statistical_approach .tab_positive_devs, #te_statistical_approach .tab_negative_devs {
		display:none;
	}
	#te_statistical_approach .dataarraylimit, .cpvcode {
		width:80px;
		float:left;
		text-align:right;
		padding:5px;
	}
	#te_statistical_approach .dataarraylimit-text, .cpvcode-text {
		float:left;
		padding: 5px 5px 0px 25px;
		display:inline-block;
	}
	#te_statistical_approach .chart-frame {
		padding-top:8px;
	}
</style>


<div id="te_statistical_approach">

	<div class="pas_rumen text_title">
		TENDERS, STATISTICAL APPROACH
	</div>
	<br />
	${data['tenderMenu']}
	<br />

	<div class="container-fluid">
        % if data['ratioCategoryDir'] == 'budgetAssessment':
            Implemented statistical analysis method is showing a visual presentation of interdependence between estimated tender value and final tender value.
        % else:
            Implemented statistical analysis method is showing a visual presentation of interdependence between tender value and number of employees of bidder.
        % endif
		<br /><br /><br />
	</div>

	<div class="tab_section">
		<div class="container-fluid">
			<div id="graph_tab" class="tab_common tab_active switch_tab" style="border-right:none;">Graph</div>
			<div id="negatives_tab" class="tab_common tab_passive switch_tab" style="border-right:none;">Negative devs</div>
			<div id="positives_tab" class="tab_common tab_passive switch_tab">Positive devs</div>
			<div class="clearfix"></div>
		</div>
	</div>
	<br />

	<div class="container-fluid">
		<div>${data['ratioDescHTML']}</div>
		<br /><br />

		<div class="float-left">
			<form method="get" name="datasourceform" id="datasourceform" action="">
				<input type="hidden" name="m" value="tenders" />
				<input type="hidden" name="a" value="ratios" />
				<input type="hidden" name="t" value="rev_per_employee" />
				Dataset: <select name="datasource" class="datasource" style="width:auto;">
					%for countryName in data["dataSourceLst"]:
						<option value="${countryName}" ${'selected="selected"' if data["dataSourceLstSelected"] == countryName else ''}>
							${countryName}
						</option>
					%endfor
				</select>
			</form>
		</div>
		<span class="dataarraylimit-text">Sample size:</span>
		<input type="text" name="dataarraylimit" class="dataarraylimit dataarraylimit-pos" value="" />
		<input type="text" name="dataarraylimit" class="dataarraylimit dataarraylimit-neg" value="" />
		<span class="cpvcode-text">CPV:</span>
		<input type="text" name="cpvcode" class="cpvcode" value="" />
		<div class="clearfix"></div>

		<div id="chart-frame" class="chart-frame"></div>
		<br />
		<div id="chart-frame-meta"></div>
	</div>
	<br /><br />
</div>
