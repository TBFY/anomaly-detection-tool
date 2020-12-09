## -*- coding: utf-8 -*-

<script src="/include/javascript/d3.v3/d3.v3.min.js"></script>
<script src="/include/javascript/chart-scripts/decision_tree.js"></script>
<link rel="stylesheet" type="text/css" href="/include/css/chart-scripts/decision_tree.css" />

<script type="text/javascript">
	var dateObj = new Date();
	var todayString = dateObj.getFullYear()+'-'+(dateObj.getMonth()+1)+'-'+dateObj.getDate();

	$(document).ready(function()
	{
		$('.tree-custom-link').click(function()
		{
			if($('.tree-custom-create').is(":visible"))
			{
				$('.tree-custom-container').slideDown(500);
				$('.tree-custom-loading').hide();
				$('.tree-custom-create').slideUp(500);
				$('.tree-custom-link').removeClass('switch_menu_active');
				$('.tree-custom-link').addClass('switch_menu_passive');
			}
			else
			{
				$('.tree-custom-container').slideUp(500);
				$('.tree-custom-loading').hide();
				$('.tree-custom-create').slideDown(500);
				$('.tree-custom-link').removeClass('switch_menu_passive');
				$('.tree-custom-link').addClass('switch_menu_active');
			}
		});

		$('.tree-custom-generate').click(function()
		{
			treeDataDict = getSelectedTreeData();
			if(treeDataDict.length < 2)
			{
				// show errors
				updateDataErrors(1);
				return;
			}
			else
			{
				// hide shown errors
				updateDataErrors(0);
			}

			treeDepth = $('#dtparam-depth').val();

			$('.tree-custom-create').hide();
			$('.tree-custom-container').hide();
			$('.tree-custom-link').hide();
			$('.tree-custom-loading').show();

			$.ajax({
				url: "/ajaxScript.py",
				type: "post",
				datatype:"json",
				data: {'action':'dTree','parameters':treeDataDict,'treeDepth':treeDepth},
				success: function(response)
				{
					// console.log(JSON.stringify(response));

					imageUrl = '${data['filePath']}' + response.fileNameImage
					$("#dtree-img").attr("src", imageUrl)
					$("#dtree-img-link").attr("href", imageUrl)

                    jsonUrl = '${data['filePath']}' + response.fileNameBase + '.json';
                    renderChart(jsonUrl);

					$('.tree-custom-create').hide();
					$('.tree-custom-loading').hide();
					$('.tree-custom-link').show();
					$('.tree-custom-container').show();
				},
				error: function (xhr, ajaxOptions, thrownError) {
					alert(xhr.status + " :: " + thrownError);
				}
			});
		});

		// function shows data related errors
		// function shows data related errors

		function updateDataErrors(errorFlag)
		{
			if(errorFlag == 0)
			{
				// remove errors
				$('#errorBoxMsg').hide();
				$('#parameters_instruction_text').removeClass('text_red');

			}
			else
			{
				// show errors
				$('#errorBoxMsg').show();
				$('#parameters_instruction_text').addClass('text_red');
			}
		}

		// function returns selected parameters for tree generation
		// function returns selected parameters for tree generation

		function getSelectedTreeData()
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

		// tree feature selector
		// tree feature selector

		$('.btn_parameter').click(function()
		{
			var id = $(this).attr('id');

			var selectedClass = 'btn-secondary';
			var unselectedClass = 'btn-outline-secondary';
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

        // draw decision tree
        // draw decision tree

		renderChart("${data['filePath']}/dt_schema.json");
	});

	// render decision tree chart
	// render decision tree chart

    function renderChart(dataFileName)
    {
        // first, empty bin
        // first, empty bin

        $('.tree-custom-container-chart').html('');

        // create chart
        // create chart

	    var dTreeChart = decisionTreeChart();

		//d3.json("${data['filePath']}/dt_schema.json?" + todayString, function(error, flare)
		//d3.json("${data['filePath']}/dt_schema.json").then(function(data)

		d3.json(dataFileName + "?" + todayString, function(error, data)
		{
		    if (error) throw error;

        	// data ready, draw chart
        	// data ready, draw chart

			d3.select('.tree-custom-container-chart')
                    .datum(data) // bind data to the div
                    .call(dTreeChart); // draw chart in div
		});
	};
</script>

<style type="text/css">
	#te_decision_tree .span_btn {
		margin:0px 5px 5px 0px;
		display:inline-block;
	}

	#te_decision_tree .tree-custom-container {
	    overflow:scroll;
	}
    #te_decision_tree .tree-custom-container::-webkit-scrollbar {
        -webkit-appearance: none;
    }
    #te_decision_tree .tree-custom-container::-webkit-scrollbar:vertical {
        width: 11px;
    }
    #te_decision_tree .tree-custom-container::-webkit-scrollbar:horizontal {
        height: 11px;
    }
    #te_decision_tree .tree-custom-container::-webkit-scrollbar-thumb {
        border-radius: 8px;
        border: 2px solid white; /* should match background, can't be transparent */
        background-color: rgba(0, 0, 0, .5);
    }
    #te_decision_tree .tree-custom-container::-webkit-scrollbar-track {
        background-color: #fff;
        border-radius: 8px;
    }
</style>

<div id="te_decision_tree">
	<div class="pas_rumen">
		TENDERS, CLUSTERING
	</div>
	<br />

	<div class="container-fluid">
		${data['tenderMenu']}
		<br /><br />

		<div class="text-center">
			<a href="javascript:void(0);" class="tree-custom-link switch_menu_passive">Customize tree</a>
		</div>
		<br /><br />

		<div>
			Decision tree learning is a predictive modelling approach, which uses a
			predictive model to go from observations about an item to conclusions
			about the item's target value. In other words, a decision tree shows us
			a model of decisions and their possible consequences.
			<br /><br />
			You can select fields from public procurement database that should be
			analysed, and depth of decision tree model. Platform then computes
			decision tree model and presents it on the screen.
		</div>
	</div>
	<br /><br />

	<div class="container-fluid">
		<div class="tree-custom-create" style="display:none;">
			<div class="row">
				<div class="col-sm-3">
					<span id="parameters_instruction_text">Select fields to be analysed:</span>
				</div>
				<div class="col-sm-9">
					%for baseKey in data["dTreeParams"]:
						<span class="span_btn"><button type="button" id="${data["dTreeParams"][baseKey]["dataFieldKey"]}" class="btn btn-outline-secondary btn_parameter">${data["dTreeParams"][baseKey]["humanText"]}</button></span>
					%endfor
				</div>
			</div>

			<div class="row">
				<div class="col-sm-3">
					Select tree depth:
				</div>
				<div class="col-sm-9">
					<select id="dtparam-depth" style="width:auto;">
						%for value in data["dTreeDepth"]:
							<option value="${value}" ${'selected="selected"' if value == '4' else ''}>
								${data["dTreeDepth"][value]}
							</option>
						%endfor
					</select>
					<br />
					<div id="errorBoxMsg" class="text_red" style="display:none;">
						<br />
						Please, select at least two parameters to include into decision tree.
					</div>
					<br />
					<div class="tree-custom-generate btn btn-primary">Go, get my tree!</div>
				</div>
			</div>
		</div>
	</div>

    <div class="container-fluid">
        <div class="tree-custom-container">
            <script type="text/javascript">
                document.write("<a href=\"${data['filePath']}${data['fileName']}?" + todayString + "\" id=\"dtree-img-link\" target=\"_blank\" class=\"text_90 float-right\">view png &raquo;</a>");
            </script>
            <div class="clearfix"></div>
            <div class="tree-custom-container-chart"></div>
        </div>
    </div>

	<div class="tree-custom-loading text-center" style="display:none;">
		<div>
			Our concierge is on its way to pick a decision tree graph for you.
			<br />
			Please, be patient as this might take a while...
		</div>
		<img src="/images/loading-monkey.gif" alt="loading" style="position:relative; top:-120px; z-index:-1;" />
	</div>
	<br /><br />
</div>

