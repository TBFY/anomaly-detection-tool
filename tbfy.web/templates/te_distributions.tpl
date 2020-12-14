## -*- coding: utf-8 -*-

<!-- Load histogram.js -->
<script type="text/javascript" src="/include/javascript/chart-scripts/histogram.js"></script>
<link rel="stylesheet" type="text/css" href="/include/css/chart-scripts/histogram.css" />
<!-- load meta data render function -->
<script type="text/javascript" src="/include/javascript/templates/${data['jsMetaDataRenderFunction']}"></script>

<script type="text/javascript">
	var dateObj = new Date();
	var todayString = dateObj.getFullYear()+'-'+(dateObj.getMonth()+1)+'-'+dateObj.getDate();

	var common_distr = "${data["common_distr"]}";

	$( document ).ready(function()
	{
		$('.fileListSelect').change(function()
		{
			$('#isciForma').submit();
		});

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

	function drawAllRatioChart()
	{
		// reset chart box
		// reset chart box

		chartDrawStart();

		// create chart
		// create chart

		var renderFunction = 'renderDataFormatKG';
		if('${data["dataSourceLstSelected"]}' == 'si-ministry')
			renderFunction = 'renderDataFormatMJU';

        var x_label = '';
        % if data["query_t"] == 'num_of_offers':
    		x_label = 'Anomaly measure: the further the value from 0, the more company/tender exhibits unwanted behaviour';
    	% else:
    	    x_label = 'Anomaly measure: the closer to 1.0 the more behavior is anomalous';
    	% endif

		var histogram = histogramChart()
			.numBins(100)
			.width(960)
			.height(500)
			.xLabel(x_label)
			.yLabel('Num of companies')
			.valueFieldName('deltavalue')
			.metaHtmlElement('#chart-frame-meta')
			.metaFunctionExternal(renderFunction);

		// draw chart
		// draw chart

		d3.tsv("${data['tsvAllDistrPointsFilePath']}?" + todayString).then(function(data)
		{
			var datalength = data.length;

			/*
			// filter area

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
			*/

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

				/*
				// filter data by cpv code
				if(cpvCodeLength > 0)
				{
					if(cpvCode != curObj.cpv.substr(0, cpvCodeLength))
						continue;
				}
				*/

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

	function drawPosDevChart()
	{
		// reset chart box
		// reset chart box

		chartDrawStart();

		// create chart
		// create chart

		var renderFunction = 'renderDataFormatKG';
		if('${data["dataSourceLstSelected"]}' == 'si-ministry')
			renderFunction = 'renderDataFormatMJU';

        var x_label = '';
        % if data["query_t"] == 'num_of_offers':
    		x_label = 'Anomaly measure: the higher the value, the more company behaviour is perceived as healthy';
    	% else:
    	    x_label = 'Anomaly measure: the more the value positive, the more company exhibits unwanted behaviour';
    	% endif

		var histogram = histogramChart()
			.numBins(100)
			.width(960)
			.height(500)
			.xLabel(x_label)
			.yLabel('Num of companies')
			.valueFieldName('deltavalue')
			.metaHtmlElement('#chart-frame-meta')
			.metaFunctionExternal(renderFunction);

		// draw chart
		// draw chart

		d3.tsv("${data['tsvPosDevPointsFilePath']}?" + todayString).then(function(data)
		{
			var datalength = data.length;

			/*
			// filter area

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
			*/

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

				/*
				// filter data by cpv code
				if(cpvCodeLength > 0)
				{
					if(cpvCode != curObj.cpv.substr(0, cpvCodeLength))
						continue;
				}
				*/

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

	function drawNegDevChart()
	{
		// reset chart box
		// reset chart box

		chartDrawStart();

		// create chart
		// create chart

		var renderFunction = 'renderDataFormatKG';
		if('${data["dataSourceLstSelected"]}' == 'si-ministry')
			renderFunction = 'renderDataFormatMJU';

		var histogram = histogramChart()
			.numBins(100)
			.width(960)
			.height(500)
			.xLabel('Anomaly measure: the lower the value, the more company exhibits unwanted behaviour')
			.yLabel('Num of companies')
			.valueFieldName('deltavalue')
			.metaHtmlElement('#chart-frame-meta')
			.metaFunctionExternal(renderFunction);

		// draw chart
		// draw chart

		d3.tsv("${data['tsvNegDevPointsFilePath']}?" + todayString).then(function(data)
		{
			var datalength = data.length;

			/*
			// filter area

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
			*/

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

				/*
				// filter data by cpv code
				if(cpvCodeLength > 0)
				{
					if(cpvCode != curObj.cpv.substr(0, cpvCodeLength))
						continue;
				}
				*/

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

	function noneRenderFunction(dataArray)
	{
		return '';
	}

	function chartDrawStart()
	{
	    $('#chart-frame').html('');
	    $('.loading_box').show();
	    loadUntilChartAvailable();
	}
	function loadUntilChartAvailable()
	{
	    var chartHTML = $('#chart-frame').html();

	    if(chartHTML.length == 0)
	    {
	        setTimeout(function(){ loadUntilChartAvailable(); }, 100);
	    }
	    else
	    {
	        $('.loading_box').hide();
	        console.log('hide load');
	    }
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
		Implemented statistical analysis method is showing a visual presentation of interdependence between tender value and number of employees of bidder.
		<br /><br /><br />
	</div>

	<div class="tab_section">
		<div class="container-fluid" tyle="padding:0;">
			<div id="graph_tab" class="tab_common tab_active switch_tab" style="border-right:none;">Graph</div>
			<div id="negatives_tab" class="tab_common tab_passive switch_tab" style="border-right:none;">Negative devs</div>
			<div id="positives_tab" class="tab_common tab_passive switch_tab">Positive devs</div>
			<div class="clearfix"></div>
		</div>
	</div>
	<br />

	<div class="container-fluid">
		<div>${data['distributionDescHTML']}</div>
		<br /><br />

		<form id="isciForma" method="get" action="">
			<input type="hidden" name="m" value="tenders" />
			<input type="hidden" name="a" value="distributions" />
			<input type="hidden" name="t" value="${data['query_t']}" />

			<select name="idfile" class="fileListSelect">
				<option value="">Select CPV</option>
				%for classificator in data["cpvDict"]:
					<option value="${classificator}" ${'selected="selected"' if data["idfile"] == classificator else ''}>
						[${classificator}]
						${data["cpvDict"][classificator]}
					</option>
				%endfor
			</select>
		</form>
		<br /><br /><br />

        <div class="text-center loading_box"><img src="/images/loading.gif" /></div>
		<div id="chart-frame" class="chart-frame"></div>
		<br />
		<div id="chart-frame-meta">Select a bar.</div>
	</div>
	<br /><br />
</div>
