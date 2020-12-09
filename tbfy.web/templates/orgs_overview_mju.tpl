## -*- coding: utf-8 -*-

<style type="text/css">
	.data_box {
		padding-left:40px;
	}
	.tender_head {
	    padding:20px;
	    background-color:#dadada;
	}
	.tender_row {
		padding:20px 0px 20px 20px;
		border-top:2px dashed #01488C;
	}
	.hide_show_tenders {
		display:none;
	}
	.tender_show_less {
		display:none;
	}
</style>

<link rel="stylesheet" type="text/css" href="/include/css/chart-scripts/donutchart.css"/>
<script type="text/javascript" src="/include/javascript/chart-scripts/donutchart.js"></script>

<script type="text/javascript">
	$( document ).ready(function()
	{
		$('.hide_show_tenders_click').click(function()
		{
			// expand tender list
			if($(this).hasClass('tender_show_more'))
			{
				$('.hide_show_tenders').show(400);
				$('.tender_show_more').hide();
				$('.tender_show_less').show();
			}
			// compress tender list
			if($(this).hasClass('tender_show_less'))
			{
				$('.hide_show_tenders').hide(400);
				$('.tender_show_more').show();
				$('.tender_show_less').hide();
			}
		});

		$('.awardsByValueChart').click(function()
		{
			drawPieChart('won');
		});
		$('.awardsByTenderNumChart').click(function()
		{
			drawPieChart('won', 'tenders_num');
		});
		$('.tendersByValueChart').click(function()
		{
			drawPieChart('issued');
		});
		$('.tendersByTenderNumChart').click(function()
		{
			drawPieChart('issued', 'tenders_num');
		});

		drawPieChart();
		drawPieChart('issued');
	});

	function drawPieChart(dataSet = 'won', dataType = '')
	{
		var selector;
		if(dataSet == 'issued')
			selector = 'chartIssued';
		else
			selector = 'chartLots';

		// clear chart container
		// clear chart container

		$('.' + selector).html('');

		// init dount chart
		// init dount chart

		var donut = donutChart()
			.width(960)
			.height(500)
			.cornerRadius(3) // sets how rounded the corners are on each slice
			.padAngle(0.015) // effectively dictates the gap between slices
			.variable('share')
			.category('company_name')
			.setDataTypes({'share':'per','abssum':'fin','Cur':'EUR'});

		// create dataset
		// create dataset

		if(dataSet == 'won')
		{
			if(dataType == 'tenders_num')
				data = returnWonDataByNumShare();
			else
				data = returnWonDataByValueShare();
		}
		else
		{
			if(dataType == 'tenders_num')
				data = returnIssuedDataByNumShare();
			else
				data = returnIssuedDataByValueShare();
		}

		// draw
		// draw

		d3.select('.' + selector)
			.datum(data) // bind data to the div
			.call(donut); // draw chart in div
	};

	function returnWonDataByValueShare()
	{
		data = [
			% if len(data['wonTendersChartData']['byValue']) > 0:
				<% i_max = len(data['wonTendersChartData']['byValue']) %>
				<% i = 1 %>
				%for id,tenderRow in data['wonTendersChartData']['byValue'].items():
					{
						'company_name': '${tenderRow["company_name"].replace("'", "\\'")}',
						'share': parseFloat(${tenderRow["share"]}),
						'abssum': parseFloat(${tenderRow["abssum"]})
					}
					% if i < i_max:
						,
					% endif
					<% i += 1 %>
				% endfor
			% endif
		];

		return data;
	};

	function returnWonDataByNumShare()
	{
		data = [
			% if len(data['wonTendersChartData']['byTenderNum']) > 0:
				<% i_max = len(data['wonTendersChartData']['byTenderNum']) %>
				<% i = 1 %>
				%for id,tenderRow in data['wonTendersChartData']['byTenderNum'].items():
					{
						'company_name': '${tenderRow["company_name"].replace("'", "\\'")}',
						'share': parseFloat(${tenderRow["share"]}),
						'abssum': parseFloat(${tenderRow["abssum"]})
					}
					% if i < i_max:
						,
					% endif
					<% i += 1 %>
				% endfor
			% endif
		];

		return data;
	};

	function returnIssuedDataByValueShare()
	{
		data = [
			% if len(data['issuedTendersChartData']['byValue']) > 0:
				<% i_max = len(data['issuedTendersChartData']['byValue']) %>
				<% i = 1 %>
				%for id,tenderRow in data['issuedTendersChartData']['byValue'].items():
					{
						'company_name': '${tenderRow["company_name"].replace("'", "\\'")}',
						'share': parseFloat(${tenderRow["share"]}),
						'abssum': parseFloat(${tenderRow["abssum"]})
					}
					% if i < i_max:
						,
					% endif
					<% i += 1 %>
				% endfor
			% endif
		];

		return data;
	};

	function returnIssuedDataByNumShare()
	{
		data = [
			% if len(data['issuedTendersChartData']['byTenderNum']) > 0:
				<% i_max = len(data['issuedTendersChartData']['byTenderNum']) %>
				<% i = 1 %>
				%for id,tenderRow in data['issuedTendersChartData']['byTenderNum'].items():
					{
						'company_name': '${tenderRow["company_name"].replace("'", "\\'")}',
						'share': parseFloat(${tenderRow["share"]}),
						'abssum': parseInt(${tenderRow["abssum"]})
					}
					% if i < i_max:
						,
					% endif
					<% i += 1 %>
				% endfor
			% endif
		];

		return data;
	};
</script>

<div class="main_landing">
	<br />
	<div class="container-fluid">

		<div class="text-center chartImage"></div>

		<!-- first, display company data -->

		<div class="text_150 text_title">Company profile</div>
		<br />

		<div class="data_box">
			% if len(data['companyProfileDict']) > 0:
				% if 'ponudnikorganizacija' in data['companyProfileDict']:
					${data['companyProfileDict']['ponudnikorganizacija']}
					<div class="visina5">&nbsp;</div>
					${data['companyProfileDict']['ponudniknaslov']}
					<div class="visina5">&nbsp;</div>
					${data['companyProfileDict']['ponudnikpostnastevilka']} ${data['companyProfileDict']['ponudnikkraj']}
					<div class="visina5">&nbsp;</div>
					${data['companyProfileDict']['ponudnikdrzava']}
					<div class="visina5">&nbsp;</div>
					ID number: ${data['companyProfileDict']['ponudnikmaticna']}
					<div class="visina5">&nbsp;</div>
					Tax number: ${data['companyProfileDict']['ponudnikdavcna']}
					<div class="visina5">&nbsp;</div>
					Size: ${data['companyProfileDict']['ponudnik_velik_eu']}
				% elif 'narocnikorganizacija' in data['companyProfileDict']:
					${data['companyProfileDict']['narocnikorganizacija']}
					<div class="visina5">&nbsp;</div>
					${data['companyProfileDict']['narocniknaslov']}
					<div class="visina5">&nbsp;</div>
					${data['companyProfileDict']['narocnikpostnastevilka']} ${data['companyProfileDict']['narocnikkraj']}
					<div class="visina5">&nbsp;</div>
					ID number: ${data['companyProfileDict']['narocnikmaticna']}
					<div class="visina5">&nbsp;</div>
					Tax number: ${data['companyProfileDict']['narocnikdavcna']}
					<div class="visina5">&nbsp;</div>
					Size: ${data['companyProfileDict']['narocnik_velik_eu']}
				% else:
					No company data available.
				% endif
			% else:
				No company data available.
			% endif
		</div>
		<br /><br />

		<div class="text_150">Tenders won (${len(data['wonTenders'])})</div>
		<br />

		% if len(data['wonTenders']) > 0:
			<div class="text-center">
				<a href="javascript:void(0);" class="awardsByValueChart">Tenders by value</a>
				&nbsp;|&nbsp;
				<a href="javascript:void(0);" class="awardsByTenderNumChart">Tenders by num</a>
				<br /><br />
				<div class="chartLots"></div>
			</div>
		% endif

		<div class="data_box">
			% if len(data['wonTenders']) > 0:
				<% tender_i_max = 1 %>
				<% tender_i = 0 %>
				%for idizpobrazca,tenderDict in data["wonTenders"].items():
					%if tender_i == tender_i_max:
						<div class="hide_show_tenders">
					%endif
				    <% tender_i += 1 %>
				    <% tender_lot_i = 0 %>
				    %for lotRow in tenderDict["tender"]:
				        <% tender_lot_i += 1 %>
				        %if tender_lot_i == 1:
				            <!-- print tender head -->
				            <% tender_id = 1 %>
                            <div class="tender_head">
                                Tender ID: <a href="${lotRow['wwwobjave']}" target="_blank">${lotRow['jnstevilka']}</a>
                            </div>
                        %endif

                        <% tender_row_css = 'border:0px;' if tender_lot_i == 1 else ''; %>
                        <div class="tender_row" style="${tender_row_css}">
                            <b>${lotRow['naslovnarocilanarocnik']}</b>
                            <div class="visina5">&nbsp;</div>
                            Buyer ID: ${lotRow['narocnikmaticna']}
                            <div class="visina5">&nbsp;</div>
                            Buyer name: ${lotRow['narocnikorganizacija']}
                            <div class="visina5">&nbsp;</div>
                            Estimated lot value budget: ${lotRow['ocenjenavrednost']} EUR
                            <div class="visina5">&nbsp;</div>
                            Final lot value: ${lotRow['koncnavrednost']} EUR
                            <div class="visina5">&nbsp;</div>
                            Lot winners:
                            <ul>
                                %for winner in tenderDict['winners']:
                                    %if str(winner['idizppriloge']) == str(lotRow['idizppriloge']):
                                        <li><a href="/?m=orgs&amp;a=source_mju&amp;id=${winner['ponudnikmaticna']}">${winner['ponudnikorganizacija']}, ${winner['ponudnikmaticna']}</a></li>
                                    %endif
                                %endfor
                            </ul>
                         </div>
                    %endfor
				%endfor
				%if tender_i > tender_i_max:
					</div>
					<br />
					<div class="hide_show_tenders_click tender_show_more text-center text_120 pointer">&darr; Show more &darr;</div>
					<div class="hide_show_tenders_click tender_show_less text-center text_120 pointer">&uarr; Show less &uarr;</div>
				%endif
			% else:
				No tenders won.
			% endif
		</div>
		<br /><br />

		<div class="text_150">Tenders issued (${len(data['issuedTenders'])})</div>
		<br />

		% if len(data['issuedTenders']) > 0:
			<div class="text-center">
				<a href="javascript:void(0);" class="tendersByValueChart">Tenders by value</a>
				&nbsp;|&nbsp;
				<a href="javascript:void(0);" class="tendersByTenderNumChart">Tenders by num</a>
				<br /><br />
				<div class="chartIssued"></div>
			</div>
		% endif

		<div class="data_box">
			% if len(data['issuedTenders']) > 0:
				<% tender_i_max = 2 %>
				<% tender_i = 0 %>
				%for idizpobrazca,tenderDict in data["issuedTenders"].items():
					%if tender_i == tender_i_max:
						<div class="hide_show_tenders">
					%endif
				    <% tender_i += 1 %>
				    <% tender_lot_i = 0 %>
				    %for lotRow in tenderDict["tender"]:
				        <% tender_lot_i += 1 %>
				        %if tender_lot_i == 1:
				            <!-- print tender head -->
				            <% tender_id = 1 %>
                            <div class="tender_head">
                                Tender ID: <a href="${lotRow['wwwobjave']}" target="_blank">${lotRow['jnstevilka']}</a>
                            </div>
                        %endif
                        <% tender_row_css = 'border:0px;' if tender_lot_i == 1 else ''; %>
                        <div class="tender_row" style="${tender_row_css}">
                            <b>${lotRow['naslovnarocilanarocnik']}</b>
                            <div class="visina5">&nbsp;</div>
                            Estimated lot value budget: ${lotRow['ocenjenavrednost']} EUR
                            <div class="visina5">&nbsp;</div>
                            Final lot value: ${lotRow['koncnavrednost']} EUR
                            <div class="visina5">&nbsp;</div>
                            Lot winners:
                            <ul>
                                %for winner in tenderDict['winners']:
                                    %if str(winner['idizppriloge']) == str(lotRow['idizppriloge']):
                                        <li><a href="/?m=orgs&amp;a=source_mju&amp;id=${winner['ponudnikmaticna']}">${winner['ponudnikorganizacija']}, ${winner['ponudnikmaticna']}</a></li>
                                    %endif
                                %endfor
                            </ul>

                         </div>
                    %endfor
				%endfor
				%if tender_i > tender_i_max:
					</div>
					<br />
					<div class="hide_show_tenders_click tender_show_more text-center text_120 pointer">&darr; Show more &darr;</div>
					<div class="hide_show_tenders_click tender_show_less text-center text_120 pointer">&uarr; Show less &uarr;</div>
				%endif
			% else:
				No issued tenders.
			% endif
		</div>
		<br /><br />

		<div class="text_150">Anomalies detected</div>
		<br />
		<div class="data_box">
			work in progress
		</div>
	</div>
	<br /><br />
</div>
