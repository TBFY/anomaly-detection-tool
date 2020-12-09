## -*- coding: utf-8 -*-

<link rel="stylesheet" type="text/css" href="/include/css/chart-scripts/donutchart.css"/>
<script type="text/javascript" src="/include/javascript/chart-scripts/donutchart.js"></script>
<script type="text/javascript">
	var dateObj = new Date();
	var todayString = dateObj.getFullYear()+'-'+(dateObj.getMonth()+1)+'-'+dateObj.getDate();

	$( document ).ready(function()
	{
		$('.publicEntityListId').change(function()
		{
			$('#isciForma').submit();
		});

		drawGraph();
	});

	function drawGraph()
	{
		var donut = donutChart()
			.width(960)
			.height(500)
			.cornerRadius(3) // sets how rounded the corners are on each slice
			.padAngle(0.015) // effectively dictates the gap between slices
			.variable('Delež')
			.category('Naziv')
			.setDataTypes({'Delež':'per','Vsota':'fin','Cur':'EUR'});

		console.log(donut);

		//d3.tsv("/dataBox/data/test.tsv").then(function(data) {
		d3.tsv("${data["urlDataFile"]}?" + todayString).then(function(data) {
			d3.select('.chartImage')
				.datum(data) // bind data to the div
				.call(donut); // draw chart in div
			console.log(data);
		});

	}
</script>

<div class="search_box">
	<form id="isciForma" method="get" action="">
		<input type="hidden" name="m" value="search" />
		<input type="hidden" name="a" value="towners" />

		<select name="id" class="publicEntityListId">
			<option value="0">Select entity</option>
			%for row in data["tenderContractees"]:
			<option value="${row['NarocnikMaticna']}" ${'selected="selected"' if data["id"] == int(row['NarocnikMaticna']) else ''}>${row['NarocnikOrganizacija']}</option>
			%endfor
		</select>
		<br /><br />

		<div class="text-center chartImage"></div>
		<br />

		%if len(data["tenderContractorsValues"])>0:
			%for id, totalSum in data["tenderContractorsValues"].items():
				${"{:,.2f}".format(data["tenderContractorsShare"][id])}% ::
				${"{:,.2f}".format(totalSum)} EUR
				<br />
				[${id}] ${data.get('tenderContractorsNames').get(id)}
				<br />
				------------
				<br />
			%endfor
		%else:
			<div style="margin-left:40px;"><h4> &#8679 Please, select an entity</h4></div>
		%endif
	</form>
	<br /><br />
</div>
