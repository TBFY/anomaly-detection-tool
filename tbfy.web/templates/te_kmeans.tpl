## -*- coding: utf-8 -*-

<!-- Load line.js -->
<script type="text/javascript" src="/include/javascript/chart-scripts/linechart.js?v=1"></script>
<link rel="stylesheet" type="text/css" href="/include/css/chart-scripts/linechart.css?v=1" />

<!-- Load 4D.js -->
<script type="text/javascript" src="/include/javascript/chart-scripts/lib/colorbar.js?v=2"></script>
<script type="text/javascript" src="/include/javascript/chart-scripts/lib/sizebar.js?v=2"></script>
<script type="text/javascript" src="/include/javascript/chart-scripts/4Dchart.js?v=2"></script>
<!-- load meta data render function -->
<script type="text/javascript" src="/include/javascript/templates/te_clusters.js?v=2"></script>

<script type="text/javascript">
	var dateObj = new Date();
	var todayString = dateObj.getFullYear()+'-'+(dateObj.getMonth()+1)+'-'+dateObj.getDate();

    // vars defining how cluster chart is drawn
    // vars defining how cluster chart is drawn

    var valueKeyArray = ${data["valueKeyMaps"]};
	var fileAppendix = '${data["fileAppendix"]}';
	var dataSourceLstSelected = '${data["dataSourceLstSelected"]}-';
	var numOfCentroids = ${data["numOfCentroids"]};
	var x_projection_val = '${data["defaultXLabel"]}';
	var y_projection_val = '${data["defaultYLabel"]}';
    var axisKeyValuePairsAll = {
        %for key, value in data["allowedAxisLabelsDict"].items():
           "${key}":"${value}",
        %endfor
        0:0
    };
    delete axisKeyValuePairsAll[0]

    var axisKeyValuePairs = axisKeyValuePairsAll;

    var cookieVarName = 'customclusters';

	$( document ).ready(function()
	{
		$('.switch_tab').click(function()
		{
			$('.switch_tab').removeClass('tab_active');
			$('.switch_tab').addClass('tab_passive');
			$(this).removeClass('tab_passive');
			$(this).addClass('tab_active');

			var tid = $(this).attr('id');
			$('.tab_content').hide();
			$('#' + tid + '_content').show();

			var tid = $(this).attr('id');
			if(tid == 'methodology_tab')
			{
			    drawMethodologyChart();
			}
			else if(tid == 'deviations_tab')
			{
			    drawClustersChart();
			}
		});

		// change data source
		// change data source

		$('.datasource').change(function()
		{
			$('#datasourceform').submit();
		});

        // change cluster projection
        // change cluster projection

		$('.projectionlabel').change(function()
		{
		    x_projection_val = $("#x_projection").val();
		    y_projection_val = $("#y_projection").val();
		    drawClustersChart();
		});

		// generate custom cluster set
		// generate custom cluster set

        $('.clusters-custom-link').click(function()
        {
            if($('.clusters-custom-create').is(":visible"))
            {
                // hide tools for creatng custom clusters
                $('.clusters-custom-create').slideUp(500);
                $('.clusters-custom-link').removeClass('switch_menu_active');
                $('.clusters-custom-link').addClass('switch_menu_passive');
                $('.clusters-custom-loading').hide();
                $('.clusters-custom-container').slideDown(500);
            }
            else
            {
                // show tools for creatng custom clusters
                $('.clusters-custom-create').slideDown(500);
                $('.clusters-custom-link').removeClass('switch_menu_passive');
                $('.clusters-custom-link').addClass('switch_menu_active');
                $('.clusters-custom-loading').hide();
                $('.clusters-custom-container').slideUp(500);
            }
        });

        $('.clusters-custom-loading-close').click(function()
        {
            $('.clusters-custom-create').hide();
            $('.clusters-custom-loading').hide(300);
            $('.clusters-custom-link').show();
            $('.clusters-custom-link').removeClass('switch_menu_active');
            $('.clusters-custom-link').addClass('switch_menu_passive');
            $('.clusters-custom-container').show(300);
        });

        // functions to handle custom clusters generation
        // functions to handle custom clusters generation

		// cluster features selector
		// cluster features selector

		$('.btn_parameter').click(function()
		{
			var id = $(this).attr('id');

			var selectedClass = 'btn-moder';
			var unselectedClass = 'btn-bel';
			if($('#' + id).hasClass(unselectedClass))
			{
				// btn is selected
				$('#' + id).removeClass(unselectedClass);
				$('#' + id).addClass(selectedClass);
			}
			else
			{
				// btn is unselected
				$('#' + id).removeClass(selectedClass);
				$('#' + id).addClass(unselectedClass);
			}
		});

		$('.clusters-custom-generate').click(function()
		{
		    // get analysis params
		    // get analysis params

			paramsDataDict = getSelectedClusterParamsData();
			clustersNum = $('#num_of_clusters').val();
			var selectedDataset = $('.datasource').val();

			// check for errors
			// check for errors

			// first hide error msgs
			// first hide error msgs

			updateDataErrors(0);

            // check num of params
            // check num of params

			if(paramsDataDict.length < 2)
			{
				// show errors
				updateDataErrors(1);
				return;
			}

			// all good, visually adapt page
			// all good, visually adapt page

			$('.clusters-custom-create').hide();
			$('.clusters-custom-container').hide();
			//$('.clusters-custom-link').hide();
			$('.clusters-custom-loading').show();

			$.ajax({
				url: "/ajaxScript.py",
				type: "post",
				datatype:"json",
				data: {'action':'clustering-id','parameters':paramsDataDict,'clusterNum':clustersNum,'selectedDataset':selectedDataset},
				timeout:0,
				success: function(response)
				{
				    saveClusterId2Cookie(response['clusterID']);
				    appendCustomClusterBtn(response['clusterID']);
				    createCustomClusters(clustersNum, paramsDataDict, selectedDataset);
				},
				error: function (xhr, ajaxOptions, thrownError) {
					alert(xhr.status + " :: " + thrownError);
					//Gateway Timeout
				}
			});
		});

		// show available custom clusters
		// show available custom clusters

		showCustomClustersBtns();

        // draw default chart
        // draw default chart

		drawClustersChart();
	});

    /**************** START CUSTOM CLUSTERING FUNCTIONS ****************/
    /**************** START CUSTOM CLUSTERING FUNCTIONS ****************/
    /**************** START CUSTOM CLUSTERING FUNCTIONS ****************/

    /**
     * cookie functions handling custom clusters
     */

    function saveClusterId2Cookie(clusterIDString)
    {
        var cookieCCValue = getCookie(cookieVarName);
        var cookieCCValueNew = '';
        var cookieLastHours = 0;

        // get new cookie value
        // get new cookie value

        if(cookieCCValue == null)
        {
            cookieCCValueNew = clusterIDString;
        }
        else
        {
            var ccArray = cookieCCValue.split("-");
            if(!inArray(clusterIDString, ccArray))
            {
                ccArray.push(clusterIDString);
            }
            cookieCCValueNew = ccArray.join('-');
        }

        // get cookie duration in hours - custom clusters are resetted at 1am, leave cookie until 5am (to approx cover potential time zones)
        // get cookie duration in hours - custom clusters are resetted at 1am, leave cookie until 5am (to approx cover potential time zones)

        var d = new Date();
        // cooke lasts until 5 am
        cookieLastHours = (24 - parseInt(d.getHours())) + 5;

        // save new value 2 cookie variable
        // save new value 2 cookie variable

        setCookie(cookieVarName, cookieCCValueNew, cookieLastHours);
        return;
    }

    function showCustomClustersBtns()
    {
        var cookieCCValue = getCookie(cookieVarName);
        if(cookieCCValue == null) return;

        var ccArray = cookieCCValue.split("-");
        for(var i = 0; i < ccArray.length; i++)
        {
            appendCustomClusterBtn(ccArray[i]);
        }
    }

    /**
     * function appends button-link notification for a user (and saves data to cookie)
     */

	function appendCustomClusterBtn(clusterID)
	{
	    var url = '?m=tenders&a=cluster&cid=' + clusterID;
	    var appendHtml = '';

	    appendHtml += '<span id="' + clusterID + '" class="text_90 custom_cluster_status custom_cluster_status_loading">';
	    appendHtml += '<a href="' + url + '">cid: ' + clusterID.substr(0, 10) + '</a>';
	    appendHtml += '<img src="/images/loading.gif" alt="loading" />';
	    appendHtml += '</span>';

        $(".current-custom-clusters-list").append(appendHtml);

        // periodically check whether clusters have been created
        updateClusterBtnStatus(clusterID);
    }

    /**
     * function checks whether the clusters with clusterID exist
     */

	function updateClusterBtnStatus(clusterID)
	{
	    // status already "ready"
	    // status already "ready"

	    if($('#' + clusterID).hasClass('custom_cluster_status_ready')) return;

	    // status still "loading"
	    // status still "loading"

        $.ajax({
            url: "/ajaxScript.py",
            type: "post",
            datatype:"json",
            data: {'action':'clustering-id-exists','clusterID':clusterID},
            timeout:0,
            success: function(response) {
                if (parseInt(response['clusterExists']) == 1)
                    setClusterBtn2Ready(clusterID);
                else
                    setTimeout( function(){ updateClusterBtnStatus(clusterID); }, 15000);
            },
            error: function (xhr, ajaxOptions, thrownError) {
                //alert(xhr.status + " :: " + thrownError);
                //Gateway Timeout
            }
        });

        return;
	}

    /**
     * function visually turns turns button from loading to ready
     */

	function setClusterBtn2Ready(clusterID)
	{
        $('#' + clusterID).removeClass('custom_cluster_status_loading');
        $('#' + clusterID).addClass('custom_cluster_status_ready');
        $('#' + clusterID + ' img').hide();
	}

    /**
     * function starts custom cluster creation
     */

	function createCustomClusters(clustersNum, paramsDataDict, selectedDataset)
	{
        $.ajax({
            url: "/ajaxScript.py",
            type: "post",
            datatype:"json",
            data: {'action':'clustering','parameters':paramsDataDict,'clusterNum':clustersNum,'selectedDataset':selectedDataset},
            timeout:0,
            success: function(response) {
                // due to timeout, no success reaction
            },
            error: function (xhr, ajaxOptions, thrownError) {
                //alert(xhr.status + " :: " + thrownError);
                //Gateway Timeout
            }
        });
    }

    /**************** END CUSTOM CLUSTERING FUNCTIONS ****************/
    /**************** END CUSTOM CLUSTERING FUNCTIONS ****************/
    /**************** END CUSTOM CLUSTERING FUNCTIONS ****************/

	function chartBuildStart()
	{
	    $('#chart-frame').html('');
	    $('#chart-frame-loading').show();
	    // select correct projections vars
	    $('#x_projection option[value="' + x_projection_val + '"]').attr('selected', 'selected');
	    $('#y_projection option[value="' + y_projection_val + '"]').attr('selected', 'selected');
	}
	function chartBuildStop()
	{
	    $('#chart-frame-loading').hide();
	}

	function drawMethodologyChart()
	{
		// reset chart box
		// reset chart box

        $(".chartmanipulation").hide();
		chartBuildStart();

		// init chart
		// init chart

		var lineChartObj = lineChart()
			.width(960)
			.height(500)
			.xLabel('Number of clusters')
			.yLabel('Cluster gain, log scale')
			.xValueFieldName('n_clusters')
			.yValueFieldName('gain');

		// append external line
		// append external line

        var lineData = {
            "coordinates": {"x1": 8, "y1": "min", "x2": 8, "y2": "max", "xscale":true, "yscale":false},
            "css": {"lwidth": 4, "stroke":"#FACB00", "fill":"#FACB00"},
            "legend": {"title": "Optimal cluster n", "position":{"px": 16, "py": 'max', "xscale":true, "yscale":false}}
        }
		lineChartObj.appendLine(lineData);

		d3.tsv("${data['gainDataFilePath']}?" + todayString).then(function(data)
		{
			// casting data
			// casting data

		    data.forEach(function(d) {
				d.n_clusters = parseInt(d.n_clusters);
				d.gain = parseFloat(d.gain);
        	});

        	// data ready, draw chart
        	// data ready, draw chart

			d3.select('#chart-frame')
				.datum(data) // bind data to the div
				.call(lineChartObj); // draw chart in div
		});

		// end char build
		// end char build

		chartBuildStop();
	}

    function drawClustersChart()
    {
        // init drawing
        // init drawing

        $(".chartmanipulation").show();
        chartBuildStart();

        // get variable x, y label
        // get variable x, y label

        var xLabel = x_projection_val;
        var yLabel = y_projection_val;
        var rLabel = 'num_of_elements';
        var centroidLabel = 'centroid_n';
        // this variable is generated from centroidLabel value
        var cLabel = 'centroidColor';

        // define deviations data source file name
        // define deviations data source file name

        var deviationsFileName = '';
        if(fileAppendix.length > 0)
            deviationsFileName = 'IDCLUSTER-cluster-closest-deviations-' + fileAppendix + '.tsv';
        else
            deviationsFileName = dataSourceLstSelected + 'IDCLUSTER-cluster-closest-deviations.tsv';

        var metaFunctionExternalName = '';
        if(dataSourceLstSelected == 'si-ministry-')
            metaFunctionExternalName = 'renderDataFormatMJU';
        else
            metaFunctionExternalName = 'renderDataFormatKG';

        var chart4DObj = chart4D()
            .xLabel(axisKeyValuePairs[xLabel])
            .yLabel(axisKeyValuePairs[yLabel])
            .cLabel('Distinctive cluster color')
            .rLabel('Cluster size')
            .cLabelDisplay(false)
            .rLabelDisplay(true)
            .xFieldName(xLabel)
            .yFieldName(yLabel)
            .rFieldName(rLabel)
            .cFieldName(cLabel)
            .nSizeMarkers(10)
            .metaHtmlElement('#chart-frame-details')
			.metaFunctionExternal(metaFunctionExternalName)
			.metaDataSourceExternal(deviationsFileName);

        // identify file source
        // identify file source

        if(fileAppendix.length > 0) fileName = "centroids-coordinates-" + fileAppendix + ".tsv";
        else fileName = dataSourceLstSelected + "centroids-coordinates.tsv?" + todayString;

        dataSourceFileName = "${data['centroidsDataFileDir']}" + fileName;
        d3.tsv(dataSourceFileName).then(function(data)
        {
            // format data if needed
            // format data if needed

            dataArray = [];
            var curObj;
            for (let i = 0; i < data.length; i++)
            {
                curObj = data[i];
                // data in tsv are strings, needed to be casted to float
                eval("curObj." + xLabel + " = parseFloat(curObj." + xLabel + ");");
                eval("curObj." + yLabel + " = parseFloat(curObj." + yLabel + ");");
                eval("curObj." + rLabel + " = parseFloat(curObj." + rLabel + ");");
                eval("curObj." + centroidLabel + " = parseFloat(curObj." + centroidLabel + ");");
                eval("curObj." + cLabel + " = curObj." + centroidLabel + " / numOfCentroids;");

                // add data to list
                dataArray.push(curObj);
            };

            // draw chart
            // draw chart

            d3.select('#chart-frame')
                .datum(dataArray) // bind data to the div
                .call(chart4DObj); // draw chart in div
        });

        // stop drawing
        // stop drawing

        chartBuildStop();
    }

    // functions to handle custom clusters generation
    // functions to handle custom clusters generation

    // function shows data related errors
    // function shows data related errors

    function updateDataErrors(errorFlag)
    {
        if(errorFlag == 0)
        {
            // remove errors
            $('.errorBoxMsg').hide();
            $('#parameters_instruction_text').removeClass('text_rdec');
        }
        else
        {
            // show errors
            $('.errorBoxMsg').show();
            $('#parameters_instruction_text').addClass('text_rdec');
        }
    }

    // function returns selected parameters to be included into analysis
    // function returns selected parameters to be included into analysis

    function getSelectedClusterParamsData()
    {
        var params = []
        $(".btn-secondary").each(function(index) {
            if($(this).hasClass('btn_parameter'))
            {
                params.push($(this).attr('id'))
            }
        });

        return params;
    };

    // function updates select option element for cluster projections
    // function updates select option element for cluster projections

    function updateSelectProjectionValues(id_element, paramsDataDict)
    {
        // find select object
        // find select object

        var selectObject = $('#' + id_element).get(0);

        // remove existing options
        // remove existing options

        while (selectObject.options.length > 0)
        {
            selectObject.remove(selectObject.options.length - 1);
        }

        // add new options
        // add new options

        for (const [key, value] of Object.entries(axisKeyValuePairsAll))
        {
            if(!paramsDataDict.includes(key)) continue;

            // create new option
            var opt = document.createElement('option');
            opt.text = value;
            opt.value = key;

            // append option to select object
            selectObject.add(opt, null);
        }

        return;
    };
</script>

<style type="text/css">
    @media only screen and (max-width : 570px) {
        #te_clustering div .custom_l
        {
            text-align:left;
            padding-left:0px;
            padding-bottom:10px;
        }
        #te_clustering div .custom_r
        {
            padding-left:0px;
        }
    }

	#te_clustering .methodology_tab_content, #te_clustering .tab_negative_devs {
		display:none;
	}

	#te_clustering .chartmanipulation {
	    padding-left:25px;
	    margin-bottom:15px;
	    text-align:right;
	}

	#te_clustering .custom_l
	{
	    text-align:right;
	}
	#te_clustering .custom_r
	{
	    padding-left:15px;
	}
	#te_clustering .custom_field
	{
	    padding-bottom:10px;
	}
	#te_clustering .span_btn {
		margin:0px 5px 5px 0px;
		display:inline-block;
	}
	#te_clustering .errorBoxMsg {
	    padding-top:10px;
	    padding-bottom:20px;
	}

    #te_clustering .custom_cluster_status {
        -webkit-border-radius: 5px;
        -moz-border-radius: 5px;
        border-radius: 5px;
        padding:8px 10px;
        margin-right:8px;
        display: inline-block;
        vertical-align:top;
        margin-bottom:8px;
    }
    #te_clustering .custom_cluster_status img {
        width:18px;
        position: relative;
        top:-2px;
        margin-left:4px;
    }
	#te_clustering .custom_cluster_status_loading {
	    border:2px solid #ffaa00;
	}
	#te_clustering .custom_cluster_status_ready {
        border:2px solid #009619;
	}
</style>

<div id="te_clustering">
	<div class="pas_rumen text_title">
		TENDERS, CLUSTERING
	</div>
	<br />

	<div class="container-fluid">
		${data['tenderMenu']}
		<br /><br />
	</div>

	<div class="tab_section">
		<div class="container-fluid">
			<div id="deviations_tab" class="tab_common tab_active switch_tab" style="border-right:none;">Deviations</div>
			<div id="methodology_tab" class="tab_common tab_passive switch_tab">Methodology</div>
			<div class="clearfix"></div>
		</div>
	</div>
	<br />

	<div class="container-fluid">
		<div id="deviations_tab_content" class="tab_content deviations_tab_content">
            Unsupervised analysis is looking for previously undetected patterns in a
            data, usually those, we are not aware of. Our method is grouping the
            data into a clusters with k-Means method. This approach helps us to
            identify commonalities in the data, and finally helps us detect
            anomalous data points that do not fit into previous identified clusters.
		</div>
		<div id="methodology_tab_content" class="tab_content methodology_tab_content">
		    The optimal number of clusters is calculated as the intersection of two linear curves: the first line is a linear regression of initial gain logarithmic values, the second line is a linear regression of last logarithmic gain values.
		</div>
		<br /><br />

		<div class="text-center">
			<a href="javascript:void(0);" class="clusters-custom-link switch_menu_passive">Customize clusters</a>
		</div>
		<br /><br />

		<div class="current-custom-clusters-list">
		    <!--
		    <span id="cidx" class="custom_cluster_status custom_cluster_status_loading">
		        <a href="">cid: ffushm435mg</a> <img src="/images/loading.gif" alt="loading" />
		    </span>
		    <span id="cidx" class="custom_cluster_status custom_cluster_status_ready">
		        <a href="">cid: sdf89ugvir</a>
		    </span>
		    -->
		</div>
		<br /><br />

        <div class="clusters-custom-create" style="display:none;">
            <div class="row">
                <div class="col-sm-3 custom_l">Number of clusters:</div>
                <div class="col-sm-9 custom_field custom_r">
                    <% clusterNums = [n for n in range(3,19)] %>
                    <select id="num_of_clusters" name="num_of_clusters" style="width:auto;">
                        <option value="-1">optimal number</option>
                        %for i in clusterNums:
                            <option value="${i}">${i}</option>
                        %endfor
                    </select>
                </div>

                <div class="col-sm-3 custom_field custom_l">
                    <span id="parameters_instruction_text">Include fields:</span>
                </div>
                <div class="col-sm-9 custom_field custom_r">
                    %for key, value in data["allowedAxisLabelsDict"].items():
						<span class="span_btn">
						    <button type="button" id="${key}" class="btn btn-bel btn_parameter">${value}</button>
						</span>
                    %endfor
                </div>

                <div class="col-sm-3 custom_field custom_l errorBoxMsg" style="display:none;">&nbsp;</div>
                <div class="col-sm-9 custom_field custom_r errorBoxMsg text_rdec" style="display:none;">
                    Please, select at least 2 parameters to be included into clustering analysis.
                </div>

                <div class="col-sm-3 custom_field custom_l">&nbsp;</div>
                <div class="col-sm-9 custom_field custom_r">
                    <div class="clusters-custom-generate btn btn-rumen">Go, cluster</div>
                </div>
            </div>
        </div>

        <div class="clusters-custom-container">
            <div class="row">
                <div class="col-sm-4 col-xs-12 text_80">
                    <form method="get" name="datasourceform" id="datasourceform" action="">
                        <input type="hidden" name="m" value="tenders" />
                        <input type="hidden" name="a" value="cluster" />
                        Dataset: <select name="datasource" class="datasource" style="width:auto;">
                            %for countryName in data["dataSourceLst"]:
                                <option value="${countryName}" ${'selected="selected"' if data["dataSourceLstSelected"] == countryName.lower() else ''}>
                                    ${countryName}
                                </option>
                            %endfor
                        </select>
                    </form>
                </div>
                <div class="col-sm-8 col-xs-12 text_80 chartmanipulation">
                    y dimension:
                    <select id="y_projection" class="projectionlabel" style="width:auto;">
                        %for key, value in data["finalAxesDict"].items():
                            <option value="${key}">${value}</option>
                        %endfor
                    </select>
                    &nbsp;&nbsp;&nbsp;
                    x dimension:
                    <select id="x_projection" class="projectionlabel" style="width:auto;">
                        %for key, value in data["finalAxesDict"].items():
                            <option value="${key}">${value}</option>
                        %endfor
                    </select>
                </div>
            </div>

            <div id="chart-frame" class="chart-frame"></div>
            <br />
            <div id="chart-frame-details"></div>
            <div id="chart-frame-loading" class="text-center" style="display:none;"><img src="/images/loading.gif" alt="loading" /></div>
        </div>
	</div>

	<div class="clusters-custom-loading" style="display:none;">
	    <div class="container-fluid">
            <img src="/images/arrow_up.png" alt="loading" class="float-left" style="position:relative; top:-40px; width:200px;" />
            <br /><br />
            <div class="float-left">
                Clusters are being created. Once process is over, the yellow link will turn to green.
                <br /><br />
                <button type="button" class="clusters-custom-loading-close btn btn-outline btn_parameter">Ok, return to chart</button>
            </div>
        </div>
	</div>
	<br /><br />
</div>


