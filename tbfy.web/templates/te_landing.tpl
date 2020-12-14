## -*- coding: utf-8 -*-

<style type="text/css">
	.hide_show_anomaly_list {
		display:none;
	}
	.anomaly_list_show_less {
		display:none;
	}
</style>

<!-- Load histogram.js -->
<script type="text/javascript" src="/include/javascript/chart-scripts/histogram.js"></script>
<link rel="stylesheet" type="text/css" href="/include/css/chart-scripts/histogram.css" />
<!-- load meta data render function -->
<script type="text/javascript" src="/include/javascript/templates/te_common_anomaly.js"></script>

<script type="text/javascript">
	var dateObj = new Date();
	var todayString = dateObj.getFullYear()+'-'+(dateObj.getMonth()+1)+'-'+dateObj.getDate();

	$( document ).ready(function()
	{
		$('.hide_show_anomaly_list_click').click(function()
		{
			// expand tender list
			if($(this).hasClass('anomaly_list_show_more'))
			{
				$('.hide_show_anomaly_list').show(400);
				$('.anomaly_list_show_more').hide();
				$('.anomaly_list_show_less').show();
			}
			// compress tender list
			if($(this).hasClass('anomaly_list_show_less'))
			{
				$('.hide_show_anomaly_list').hide(400);
				$('.anomaly_list_show_more').show();
				$('.anomaly_list_show_less').hide();
			}
		});

		drawCommonAnomalyHistogram();
	});

	function drawCommonAnomalyHistogram()
	{
		console.log('common anomaly histogram');

		// reset chart box
		// reset chart box

        chartDrawStart()

		// create chart
		// create chart

		var histogram = histogramChart()
			.numBins(100)
			.width(960)
			.height(500)
			.xLabel('Common anomaly measure: higher value infers higher anomalous behaviour')
			.yLabel('Num of entities')
			.valueFieldName('common_anomaly_value')
			.metaHtmlElement('#chart-frame-meta')
			.metaFunctionExternal('renderDataFormatMJU');

		// draw chart
		// draw chart

		d3.tsv("${data['commonAnomalyRankFilePath']}?" + todayString).then(function(data)
		{
			var datalength = data.length;

			// filter data
			// filter data

			dataArray = [];
			var curObj;

			for (let i = 0; i < datalength; i++)
			{
				curObj = data[i];

				// cast data
				curObj.common_anomaly_value = parseFloat(curObj.common_anomaly_value);

				// accept only companies with anomaly > 0.5
				if(curObj.common_anomaly_value < 1.2)
				    continue;

				// add data to list
				dataArray.push(curObj);
			}

        	// data ready, draw chart
        	// data ready, draw chart

			d3.select('#chart-frame')
				.datum(dataArray) // bind data to the div
				.call(histogram); // draw chart in div
		});
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

<div class="te_landing">
	<div class="container-fluid">
		<div class="row no-gutters">
			<div class="col-sm-8"><div class="landing_tender_title_text">
				<h1 class="text_200 text_title">Analysis and visualisation of public procurements</h1>
				<br />
				<h3 class="text_120">
					Analysis of public procurement data in OCDS format.
				</h3>
			</div></div>
			<div class="col-sm-4"><div class="landing_tender_title_img">
				<img src="/images/te_lnd_main.png" class="img-fluid" alt="" />
			</div></div>
		</div>
	</div>
	<br /><br />

	<div class="pas_rumen text_title">
		COMMON ANOMALY RANK
	</div>
	<br /><br />

	<div class="container-fluid">
	    <div class="text-center loading_box"><img src="/images/loading.gif" /></div>
		<div id="chart-frame" class="chart-frame"></div>
		<br />
		<div id="chart-frame-meta"></div>
	</div>
	<br /><br />

	<div class="pas_rumen text_title">
		METHODOLOGY
	</div>
	<br /><br />

	<div class="container-fluid">
		Analysis of public procurement data could be done by several approaches:
		supervised, unsupervised and statistical analysis. We also developed
		support for StreamStory tool, which performs data analysis of temporal
		data (large multivariate event sequences).
		<br /><br />
		Unsupervised analysis is based on k-Means method. Supervised analysis is
		based on a decision tree analysis, and is used to get additional
		insights into the public procurement decision-making process.
		Statistical analysis is done in order to pursue a more intuitive and
		defined-in-advance goals. StreamStory tool is used to uncover, visualize
		and explain the inner structure within the data.
	</div>
	<br /><br />

	<div class="container-fluid">
		${data['tenderMenu']}
	</div>
	<br /><br />
</div>
