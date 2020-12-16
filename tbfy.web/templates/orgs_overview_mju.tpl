## -*- coding: utf-8 -*-

<style type="text/css">
    .tab_content {
        padding:30px 10px 0px 10px;
    }
	.tender_box {
	    border-top:3px dashed #FACB01;
	    padding:25px 0px;
	}
	.tender_head {
	    padding:10px 10px 10px 0px;
	    margin-bottom:0px;
	}
	.tender_row {
		padding:20px 0px;
		margin-left:30px;
		border-top:2px dashed #01488C;
	}
	.hide_show_tenders {
		display:none;
	}
	.tender_show_less {
		display:none;
	}

	.tender_chart_cell_left {
	    border-right:2px solid #01488C;
	}
	.tender_chart_bar {
	    background-color:#FACB01;
	    height:4px line-height:4px;
	    margin-top:0.1em;
	}
</style>

<link rel="stylesheet" type="text/css" href="/include/css/chart-scripts/donutchart.css"/>
<script type="text/javascript" src="/include/javascript/chart-scripts/donutchart.js"></script>

<script type="text/javascript">
	$( document ).ready(function()
	{
	    // tab menu
		$('.switch_tab').click(function()
		{
			$('.switch_tab').removeClass('tab_active');
			$('.switch_tab').addClass('tab_passive');
			$(this).removeClass('tab_passive');
			$(this).addClass('tab_active');

            // load content
            $('.tab_content').hide();
			var tid = $(this).attr('id');
			if(tid == 'tenders_won')
			{
				$('#tenders_won_content').show();
			}
			else if(tid == 'tenders_issued')
			{
				$('#tenders_issued_content').show();
            }
			else if(tid == 'anomalies_detected')
			{
				$('#anomalies_detected_content').show();
            }
		});

		$('.tender_chart_type').click(function()
		{
		    var id = $(this).attr('id');

		    if(id == 'tenders_won_value')
		    {
		        $('.tenders_won_num_chart').hide();
		        $('.tenders_won_value_chart').show();
		    }
		    else if(id == 'tenders_won_num')
		    {
		        $('.tenders_won_value_chart').hide();
		        $('.tenders_won_num_chart').show();
		    }
		    else if(id == 'tenders_issued_num')
		    {
		        $('.tenders_issued_value_chart').hide();
		        $('.tenders_issued_num_chart').show();
		    }
		    else if(id == 'tenders_issued_value')
		    {
		        $('.tenders_issued_num_chart').hide();
		        $('.tenders_issued_value_chart').show();
		    }
		});

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

	    % if len(data['wonTenders']) == 0 and len(data['issuedTenders']) > 0:
	        $('#tenders_issued').click();
        %endif

	});

    /*

    // draw pie chart
    // draw pie chart

	drawPieChart();
	drawPieChart('issued');

	// functions enabling pie chart to be drawn
	// functions enabling pie chart to be drawn

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
	*/
</script>

<div class="main_landing">
	<div class="pas_rumen" style="text-align:left;">
	    <div class="container-fluid">
		    Tenders / Company
		</div>
	</div>
	<br /><br />

	<div class="container-fluid">
		<!-- company data -->
		<!-- company data -->

        % if len(data['companyProfileDict']) > 0:
            <div  class="row">
                % if 'ponudnikorganizacija' in data['companyProfileDict']:
                    <div class="col-sm-3 col-6">
                        <b>${data['companyProfileDict']['ponudnikorganizacija']}</b>
                        <div class="visina5">&nbsp;</div>
                        <b>${data['companyProfileDict']['ponudniknaslov']}</b>
                        <div class="visina5">&nbsp;</div>
                        <b>${data['companyProfileDict']['ponudnikpostnastevilka']} ${data['companyProfileDict']['ponudnikkraj']}</b>
                        <div class="visina5">&nbsp;</div>
                        <b>${data['companyProfileDict']['ponudnikdrzava']}</b>
                        <br /><br /><br />
                    </div>
                    <div class="col-sm-3 col-6">
                        <div class="row no-gutters">
                            <div class="col-3">ID</div>
                            <div class="col-9"><b>${data['companyProfileDict']['ponudnikmaticna']}</b></div>
                        </div>
                        <div class="visina5">&nbsp;</div>
                        <div  class="row no-gutters">
                            <div class="col-3">Tax</div>
                            <div class="col-9"><b>${data['companyProfileDict']['ponudnikdavcna']}</b></div>
                        </div>
                        <div class="visina5">&nbsp;</div>
                        <div  class="row no-gutters">
                            <div class="col-3">Size</div>
                            <div class="col-9"><b>${data['companyProfileDict']['ponudnik_velik_eu']}</b></div>
                        </div>
                        <br /><br /><br />
                    </div>
                % elif 'narocnikorganizacija' in data['companyProfileDict']:
                    <div class="col-sm-3 col-6">
                        <b>${data['companyProfileDict']['narocnikorganizacija']}</b>
                        <div class="visina5">&nbsp;</div>
                        <b>${data['companyProfileDict']['narocniknaslov']}</b>
                        <div class="visina5">&nbsp;</div>
                        <b>${data['companyProfileDict']['narocnikpostnastevilka']} ${data['companyProfileDict']['narocnikkraj']}</b>
                        <br /><br /><br />
                    </div>
                    <div class="col-sm-3 col-6">
                        <div class="row no-gutters">
                            <div class="col-3">ID</div>
                            <div class="col-9"><b>${data['companyProfileDict']['narocnikmaticna']}</b></div>
                        </div>
                        <div class="visina5">&nbsp;</div>
                        <div  class="row no-gutters">
                            <div class="col-3">Tax</div>
                            <div class="col-9"><b>${data['companyProfileDict']['narocnikdavcna']}</b></div>
                        </div>
                        <div class="visina5">&nbsp;</div>
                        <div  class="row no-gutters">
                            <div class="col-3">Size</div>
                            <div class="col-9"><b>${data['companyProfileDict']['narocnik_velik_eu']}</b></div>
                        </div>
                        <br /><br /><br />
                    </div>
                % else:
                    No company data available.
                % endif
                <div class="col-sm-3 col-6">
                    <div  class="row no-gutters">
                        <div class="col-9">Tenders won</div>
                        <div class="col-3"><b>${len(data['wonTenders'])}</b></div>
                    </div>
                    <div class="visina5">&nbsp;</div>
                    <div  class="row no-gutters">
                        <div class="col-9">Tenders issued</div>
                        <div class="col-3"><b>${len(data['issuedTenders'])}</b></div>
                    </div>
                    <div class="visina5">&nbsp;</div>
                    <div  class="row no-gutters">
                        <div class="col-9">Anomalies found</div>
                        <div class="col-3"><b>${data['numOfAnomalies']}</b></div>
                    </div>
                    <br /><br /><br />
                </div>
                <div class="col-sm-3 col-6">
                    External links
                    <div class="visina5">&nbsp;</div>
                    &bull; &nbsp; <b><a href="https://www.ajpes.si/podjetje/${data['companyProfileDict']['ajpesnaziv']}" target="_blank">Ajpes</a></b>
                    <div class="visina5">&nbsp;</div>
                    &bull; &nbsp; <b><a href="https://erar.si/prejemnik/${data['companyProfileDict']['erardavcna']}/#transakcije" target="_blank">Erar</a></b>
                    <br /><br /><br />
                </div>
            </div>
        % else:
            No company data available.
        % endif
     </div>

    <div class="tab_section">
        <div class="container-fluid" style="padding:0;">
            <span class="tab_common tab_active switch_tab" id="tenders_won" style="border-right:none;">
                Tenders won (${len(data['wonTenders'])})
            </span>
            <span class="tab_common tab_passive switch_tab" id="tenders_issued" style="border-right:none;">
                Tenders issued (${len(data['issuedTenders'])})
            </span>
            <span class="tab_common tab_passive switch_tab" id="anomalies_detected" style="display:inline-block;">
                Anomalies (${data['numOfAnomalies']})
            </span>
            <div class="clearfix"></div>
        </div>
    </div>

	<div class="container-fluid">
	    <div id="tenders_won_content" class="tab_content">
	        <!-- tenders won content -->
	        <!-- tenders won content -->


            % if len(data['wonTenders']) > 0:
                <div class="row no-gutters">
                    <div class="col-5 text-right tender_chart_cell_left">
                        <a href="javascript:void(0);" id="tenders_won_value" class="tender_chart_type">Tenders by value</a> &nbsp;
                    </div>
                    <div class="col-7">
                        &nbsp; <a href="javascript:void(0);" id="tenders_won_num" class="tender_chart_type">Tenders by num</a>
                    </div>
                </div>
                <br />

                <div class="tenders_won_value_chart">
                    %for company_id,companyDict in data["wonTendersChartData"]['byValue'].items():
                        <% curr_share = int(round(float(companyDict['share']) * 100, 0)) %>
                        % if curr_share > 0:
                            <div class="row no-gutters">
                                <div class="col-5 tender_chart_cell_left">
                                    <div class="text-right" style="padding-right:10px;">${companyDict['company_name']} [${curr_share}%]</div>
                                    <div class="visina5">&nbsp;</div>
                                </div>
                                <div class="col-7">
                                    <div class="tender_chart_bar" style="width:${curr_share}%;">&nbsp;${curr_share}%</div>
                                </div>
                            </div>
                        %endif
                    %endfor
                </div>
                <div class="tenders_won_num_chart" style="display:none;">
                    %for company_id,companyDict in data["wonTendersChartData"]['byTenderNum'].items():
                        <% curr_share = int(round(float(companyDict['share']) * 100, 0)) %>
                        % if curr_share > 0:
                            <div class="row no-gutters">
                                <div class="col-5 tender_chart_cell_left">
                                    <div class="text-right" style="padding-right:10px;">${companyDict['company_name']} [${companyDict['abssum']} lots]</div>
                                    <div class="visina5">&nbsp;</div>
                                </div>
                                <div class="col-7">
                                    <div class="tender_chart_bar" style="width:${curr_share}%;">&nbsp;${curr_share}%</div>
                                </div>
                            </div>
                        %endif
                    %endfor
                </div>
                <br /><br />
            % endif

            % if len(data['wonTenders']) > 0:
                <% tender_i_max = 6 %>
                <% tender_i = 0 %>
                %for idizpobrazca,tenderDict in data["wonTenders"].items():
                    %if tender_i == tender_i_max:
                        <div class="hide_show_tenders">
                    %endif
                    <div class="tender_box">
                        <% tender_i += 1 %>
                        <% tender_lot_i = 0 %>
                        %for lotRow in tenderDict["tender"]:
                            <% tender_lot_i += 1 %>
                            %if tender_lot_i == 1:
                                <!-- print tender head -->
                                <% tender_id = 1 %>
                                <div class="tender_head">
                                    <b>${lotRow['naslovnarocilanarocnik']}</b>
                                    <div class="visina5">&nbsp;</div>
                                    <b>Tender ID: <a href="${lotRow['wwwobjave']}" target="_blank">${lotRow['jnstevilka']}</a></b>
                                </div>
                            %endif

                            <% tender_row_css = 'border:0px;' if tender_lot_i == 1 else ''; %>
                            <div class="tender_row" style="${tender_row_css}">
                                <div class="row no-gutters">
                                    <div class="col-12 col-sm-6">
                                        <div class="row no-gutters">
                                            <div class="col-4">Buyer</div>
                                            <div class="col-8">${lotRow['narocnikorganizacija']}</div>
                                            <div class="col-4">ID</div>
                                            <div class="col-8">${lotRow['narocnikmaticna']}</div>
                                            <div class="col-4">Estimated budget</div>
                                            <div class="col-8">${lotRow['ocenjenavrednost']}</div>
                                            <div class="col-4">Final budget</div>
                                            <div class="col-8">${lotRow['koncnavrednost']}</div>
                                        </div>
                                    </div>
                                    <div class="col-12 col-sm-6">
                                        Lot winners:
                                        <ul style="list-style:disc;">
                                            %for winner in tenderDict['winners']:
                                                %if str(winner['idizppriloge']) == str(lotRow['idizppriloge']):
                                                    <li><a href="/?m=orgs&amp;a=source_mju&amp;id=${winner['ponudnikmaticna']}">${winner['ponudnikorganizacija']}, ${winner['ponudnikmaticna']}</a></li>
                                                %endif
                                            %endfor
                                        </ul>
                                    </div>
                                </div>
                             </div>
                        %endfor
                    </div>
                %endfor
                %if tender_i > tender_i_max:
                    </div>
                    <br />
                    <div class="hide_show_tenders_click tender_show_more text-center text_120 pointer">&darr; Show more &darr;</div>
                    <div class="hide_show_tenders_click tender_show_less text-center text_120 pointer">&uarr; Show less &uarr;</div>
                %endif
            % else:
                Company hasn't won any tenders.
            % endif
	    </div>
	    <div id="tenders_issued_content" class="tab_content" style="display:none;">
	        <!-- tenders issued content -->
	        <!-- tenders issued content -->

           % if len(data['issuedTenders']) > 0:
                <div class="row no-gutters">
                    <div class="col-5 text-right tender_chart_cell_left">
                        <a href="javascript:void(0);" id="tenders_issued_value" class="tender_chart_type">Tenders by value</a> &nbsp;
                    </div>
                    <div class="col-7">
                        &nbsp; <a href="javascript:void(0);" id="tenders_issued_num" class="tender_chart_type">Tenders by num</a>
                    </div>
                </div>
                <br />

                <div class="tenders_issued_value_chart">
                    %for company_id,companyDict in data["issuedTendersChartData"]['byValue'].items():
                        <% curr_share = int(round(float(companyDict['share']) * 100, 0)) %>
                        <div class="row no-gutters">
                            <div class="col-5 tender_chart_cell_left">
                                <div class="text-right" style="padding-right:10px;">${companyDict['company_name']} [${curr_share}%]</div>
                                <div class="visina5">&nbsp;</div>
                            </div>
                            <div class="col-7">
                                <div class="tender_chart_bar" style="width:${curr_share}%;">&nbsp;</div>
                            </div>
                        </div>
                    %endfor
                </div>
                <div class="tenders_issued_num_chart" style="display:none;">
                    %for company_id,companyDict in data["issuedTendersChartData"]['byTenderNum'].items():
                        <% curr_share = int(round(float(companyDict['share']) * 100, 0)) %>
                        <div class="row no-gutters">
                            <div class="col-5 tender_chart_cell_left">
                                <div class="text-right" style="padding-right:10px;">${companyDict['company_name']} [${companyDict['abssum']} lots]</div>
                                <div class="visina5">&nbsp;</div>
                            </div>
                            <div class="col-7">
                                <div class="tender_chart_bar" style="width:${curr_share}%;">&nbsp;</div>
                            </div>
                        </div>
                    %endfor
                </div>
                <br /><br />
            % endif

            <div class="data_box">
                % if len(data['issuedTenders']) > 0:
                    <% tender_i_max = 6 %>
                    <% tender_i = 0 %>
                    %for idizpobrazca,tenderDict in data["issuedTenders"].items():
                        %if tender_i == tender_i_max:
                            <div class="hide_show_tenders">
                        %endif
                        <div class="tender_box">

                            <% tender_i += 1 %>
                            <% tender_lot_i = 0 %>
                            %for lotRow in tenderDict["tender"]:
                                <% tender_lot_i += 1 %>
                                %if tender_lot_i == 1:
                                    <!-- print tender head -->
                                    <% tender_id = 1 %>
                                    <div class="tender_head">
                                        <b>${lotRow['naslovnarocilanarocnik']}</b>
                                        <div class="visina5">&nbsp;</div>
                                        <b>Tender ID: <a href="${lotRow['wwwobjave']}" target="_blank">${lotRow['jnstevilka']}</a></b>
                                    </div>
                                %endif
                                <% tender_row_css = 'border:0px;' if tender_lot_i == 1 else ''; %>
                                <div class="tender_row" style="${tender_row_css}">
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
                        </div>
                    %endfor
                    %if tender_i > tender_i_max:
                        </div>
                        <br />
                        <div class="hide_show_tenders_click tender_show_more text-center text_120 pointer">&darr; Show more &darr;</div>
                        <div class="hide_show_tenders_click tender_show_less text-center text_120 pointer">&uarr; Show less &uarr;</div>
                    %endif
                % else:
                    Company hasn't issued any tenders.
                % endif
            </div>
	    </div>
	    <div id="anomalies_detected_content" class="tab_content" style="display:none;">
	        <!-- anomalies detected content -->
	        <!-- anomalies detected content -->

            <div>
                % if len(data['anomaliesDict']) == 0:
                    No anomalies found.
                % else:
                    <% i = 0 %>
                    % for anomalyType,rowList in data['anomaliesDict'].items():
                        <% tender_box_class = '' if i == 0 else 'tender_box' %>
                        <div class="${tender_box_class}">
                            % if anomalyType == 'distribution-offersnum':
                                <b><a href="/?m=tenders&a=distributions&t=num_of_offers" class="link_nepodcrtan">Number of competitive offers distribution</a></b>
                                <br /><br />
                                ${data['companyProfileDict']['ponudnikorganizacija']} is on average winning tenders within a <b>LESS competitive</b> environment as an average company does.
                                In comparison to other companies, ${data['companyProfileDict']['ponudnikorganizacija']} can be found <a href="/?m=tenders&a=distributions&t=num_of_offers">here</a> having a score of ${rowList['anomaly'][0]}.
                                <br /><br />
                                <div class="row no-gutters">
                                    <div class="col-4" style="padding-right:20px;">
                                        <% distrList = rowList['anomaly'][2].split('-') %>
                                        Current company's competition for won tenders:
                                        <div class="visina5">&nbsp;</div>
                                        <div class="visina5">&nbsp;</div>
                                        <div class="row no-gutters">
                                            <div class="col-9">No competitor</div>
                                            <div class="col-3 text-right"><b>${distrList[0]}%</b></div>
                                            <div class="col-9">One competitor</div>
                                            <div class="col-3 text-right"><b>${distrList[1]}%</b></div>
                                            <div class="col-9">2+ competitors</div>
                                            <div class="col-3 text-right"><b>${distrList[2]}%</b></div>
                                        </div>
                                    </div>
                                    <div class="col-4" style="padding-right:20px;">
                                        <% cmnDistrList = rowList['avgdistr']['data'][0][0].split('-') %>
                                        Average competition for companies tender winners:
                                        <div class="visina5">&nbsp;</div>
                                        <div class="visina5">&nbsp;</div>
                                        <div class="row no-gutters" style="padding-right:15px;">
                                            <div class="col-9">No competitor</div>
                                            <div class="col-3 text-right"><b>${cmnDistrList[0]}%</b></div>
                                            <div class="col-9">One competitor</div>
                                            <div class="col-3 text-right"><b>${cmnDistrList[1]}%</b></div>
                                            <div class="col-9">2+ competitors</div>
                                            <div class="col-3 text-right"><b>${cmnDistrList[2]}%</b></div>
                                        </div>
                                    </div>
                                    <div class="col-4">
                                        <% cpvDistrList = rowList['cpvdistr']['data'][0][0].split('-') %>
                                        Average competition for tenders winners (CPV = ${rowList['cpv']}):
                                        <div class="visina5">&nbsp;</div>
                                        <div class="visina5">&nbsp;</div>
                                        <div class="row no-gutters" style="padding-right:15px;">
                                            <div class="col-9">No competitor</div>
                                            <div class="col-3 text-right"><b>${cpvDistrList[0]}%</b></div>
                                            <div class="col-9">One competitor</div>
                                            <div class="col-3 text-right"><b>${cpvDistrList[1]}%</b></div>
                                            <div class="col-9">2+ competitors</div>
                                            <div class="col-3 text-right"><b>${cpvDistrList[2]}%</b></div>
                                        </div>
                                    </div>
                                </div>
                                <br /><br />
                            % elif anomalyType == 'distribution-bdgasses':
                                <b><a href="/?m=tenders&a=distributions&t=budget_assessment" class="link_nepodcrtan">Assesed budget vs final budget</a></b>
                                <br /><br />
                                <% anomaly_value = abs(float(rowList['anomaly'][0])) %>
                                % if anomaly_value < 0.9:
                                    Assesed tender values for ${data['companyProfileDict']['ponudnikorganizacija']} are <b>unusually</b> close to final tender values.
                                % else:
                                    Assesed tender values for ${data['companyProfileDict']['ponudnikorganizacija']} are <b>HIGHLY unusual</b> close to final tender values.
                                %endif
                                <br /><br />
                            % elif anomalyType == 'ratio-rev-per-employee-pos':
                                ${data['companyProfileDict']['ponudnikorganizacija']} appears to have an <b>unusually HIGH</b> tender-related revenues regarding its employee size.
                                <br />
                                % if 'bidders' in rowList and len(rowList['bidders']) > 0:
                                    <br />
                                    Tender revenues, where company appears as bidder:
                                    <div class="visina5">&nbsp;</div>
                                    <div class="visina5">&nbsp;</div>
                                    <ul>
                                    % for currRow in rowList['bidders']:
                                        <% tmp_value = round(float(currRow[4]) / float(currRow[5]), 2) %>
                                        <li>${tmp_value} EUR / employee</li>
                                        <div class="visina5">&nbsp;</div>
                                    % endfor
                                    </ul>
                                % endif
                                % if 'buyers' in rowList and len(rowList['buyers']) > 0:
                                    <br />
                                    Tender revenues, where company appears as bidder:
                                    <div class="visina5">&nbsp;</div>
                                    <div class="visina5">&nbsp;</div>
                                    <ul>
                                    % for currRow in rowList['buyers']:
                                        <% tmp_value = round(float(currRow[4]) / float(currRow[5]), 2) %>
                                        <li>${tmp_value} EUR / employee</li>
                                        <div class="visina5">&nbsp;</div>
                                    % endfor
                                    </ul>
                                % endif

                            % elif anomalyType == 'ratio-rev-per-employee-neg':
                                ${data['companyProfileDict']['ponudnikorganizacija']} appears to have an <b>unusually LOW</b> tender-related revenues regarding its employee size.
                                <br />
                                % if 'bidders' in rowList and len(rowList['bidders']) > 0:
                                    <br />
                                    Tender revenues, where company appears as bidder:
                                    <div class="visina5">&nbsp;</div>
                                    <div class="visina5">&nbsp;</div>
                                    <ul>
                                    % for currRow in rowList['bidders']:
                                        <% tmp_value = round(float(currRow[4]) / float(currRow[5]), 2) %>
                                        <li>${tmp_value} EUR / employee</li>
                                        <div class="visina5">&nbsp;</div>
                                    % endfor
                                    </ul>
                                % endif
                                % if 'buyers' in rowList and len(rowList['buyers']) > 0:
                                    <br />
                                    Tender revenues, where company appears as buyer:
                                    <div class="visina5">&nbsp;</div>
                                    <div class="visina5">&nbsp;</div>
                                    <ul>
                                    % for currRow in rowList['buyers']:
                                        <% tmp_value = round(float(currRow[4]) / float(currRow[5]), 2) %>
                                        <li>${tmp_value} EUR / employee</li>
                                        <div class="visina5">&nbsp;</div>
                                    % endfor
                                    </ul>
                                % endif

                            % elif anomalyType == 'ratio-assessed-final-bdg-neg':
                                ${data['companyProfileDict']['ponudnikorganizacija']} appears to have an <b>unusually LOW</b> assessed value compared to final tender value.
                                <br />
                                % if 'bidders' in rowList and len(rowList['bidders']) > 0:
                                    <br />
                                    Tender revenues, where company appears as bidder:
                                    <div class="visina5">&nbsp;</div>
                                    <div class="visina5">&nbsp;</div>
                                    <div class="row no-gutters">
                                        <div class="col-6 col-sm-3"><b>Assessed tender value</b></div>
                                        <div class="col-6 col-sm-3"><b>Final tender value</b></div>
                                    </div>
                                    % for currRow in rowList['bidders']:
                                        <div class="row no-gutters">
                                            <div class="col-6 col-sm-3">EUR ${round(float(currRow[4]),2)}</div>
                                            <div class="col-6 col-sm-9">EUR ${round(float(currRow[5]),2)}</div>
                                        </div>
                                    % endfor
                                % endif
                                % if 'buyers' in rowList and len(rowList['buyers']) > 0:
                                    <br />
                                    Tender revenues, where company appears as buyer:
                                    <div class="visina5">&nbsp;</div>
                                    <div class="visina5">&nbsp;</div>
                                    <div class="row no-gutters">
                                        <div class="col-6 col-sm-3"><b>Assessed tender value</b></div>
                                        <div class="col-6 col-sm-3"><b>Final tender value</b></div>
                                    </div>
                                    % for currRow in rowList['buyers']:
                                        <div class="row no-gutters">
                                            <div class="col-6 col-sm-3">EUR ${round(float(currRow[4]),2)}</div>
                                            <div class="col-6 col-sm-9">EUR ${round(float(currRow[5]),2)}</div>
                                        </div>
                                    % endfor
                                % endif

                            % elif anomalyType == 'ratio-assessed-final-bdg-pos':
                                ${data['companyProfileDict']['ponudnikorganizacija']} appears to have an <b>unusually HIGH</b> assessed value compared to final tender value.
                                <br />
                                % if 'bidders' in rowList and len(rowList['bidders']) > 0:
                                    <br />
                                    Tender revenues, where company appears as bidder:
                                    <div class="visina5">&nbsp;</div>
                                    <div class="visina5">&nbsp;</div>
                                    <div class="row no-gutters">
                                        <div class="col-6 col-sm-3"><b>Assessed tender value</b></div>
                                        <div class="col-6 col-sm-3"><b>Final tender value</b></div>
                                    </div>
                                    % for currRow in rowList['bidders']:
                                        <div class="row no-gutters">
                                            <div class="col-6 col-sm-3">EUR ${round(float(currRow[4]),2)}</div>
                                            <div class="col-6 col-sm-9">EUR ${round(float(currRow[5]),2)}</div>
                                        </div>
                                    % endfor
                                % endif
                                % if 'buyers' in rowList and len(rowList['buyers']) > 0:
                                    <br />
                                    Tender revenues, where company appears as buyer:
                                    <div class="visina5">&nbsp;</div>
                                    <div class="visina5">&nbsp;</div>
                                    <div class="row no-gutters">
                                        <div class="col-6 col-sm-3"><b>Assessed tender value</b></div>
                                        <div class="col-6 col-sm-3"><b>Final tender value</b></div>
                                    </div>
                                    % for currRow in rowList['buyers']:
                                        <div class="row no-gutters">
                                            <div class="col-6 col-sm-3">EUR ${round(float(currRow[4]),2)}</div>
                                            <div class="col-6 col-sm-9">EUR ${round(float(currRow[5]),2)}</div>
                                        </div>
                                    % endfor
                                % endif

                            % elif anomalyType == 'dependency-bidder2buyer' or anomalyType == 'dependency-buyer2bidder' or anomalyType == 'dependency-mutual':
                                ${data['companyProfileDict']['ponudnikorganizacija']} seems to be highly dependent on some other companies.
                                <br />
                                % if 'bidders' in rowList and len(rowList['bidders']) > 0:
                                    <br />
                                    As a bidder, company depends on buyers:
                                    <div class="visina5">&nbsp;</div>
                                    <div class="visina5">&nbsp;</div>
                                    <div class="row no-gutters">
                                        <div class="col-3"><b>Dependence share</b></div>
                                        <div class="col-9"><b>Buyer name</b></div>
                                    </div>
                                    % for currRow in rowList['bidders']:
                                        <div class="row no-gutters">
                                            <div class="col-3">${round(100.0*float(currRow[2]),2)}%</div>
                                            <div class="col-9">${currRow[5]}</div>
                                        </div>
                                    % endfor
                                % endif
                                % if 'buyers' in rowList and len(rowList['buyers']) > 0:
                                    <br />
                                    As a buyer, company depends on bidders:
                                    <div class="visina5">&nbsp;</div>
                                    <div class="visina5">&nbsp;</div>
                                    <div class="row no-gutters">
                                        <div class="col-3"><b>Dependence share</b></div>
                                        <div class="col-9"><b>Bidder name</b></div>
                                    </div>
                                    % for currRow in rowList['buyers']:
                                        <div class="row no-gutters">
                                            <div class="col-3">${round(100.0*float(currRow[2]),2)}%</div>
                                            <div class="col-9">${currRow[4]}</div>
                                        </div>
                                    % endfor
                                % endif

                            % else:
                                Error: unknown anomaly detected.
                            % endif
                            <% i += 1 %>
                        </div>
                    % endfor
                % endif
            </div>
	    </div>
	</div>
	<br /><br />
</div>
