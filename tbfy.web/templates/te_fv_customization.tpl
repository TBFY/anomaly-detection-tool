## -*- coding: utf-8 -*-

<script type="text/javascript">
	$(document).ready(function()
	{
		$('.fv-custom-link').click(function()
		{
			if($('.fv-custom-create').is(":visible"))
			{
				$('.fv-custom-create').slideUp(500);
				$('.fv-custom-link').removeClass('switch_menu_active');
				$('.fv-custom-link').addClass('switch_menu_passive');
			}
			else
			{
				$('.fv-custom-create').slideDown(500);
				$('.fv-custom-link').removeClass('switch_menu_passive');
				$('.fv-custom-link').addClass('switch_menu_active');
			}
		});

		$('.buyerg_select').change(function() {
			var groupName = $('.buyerg_select').find(":selected").val();

			$.ajax({
				url: "/ajaxScript.py",
				type: "post",
				datatype:"json",
				data: {
					'action':'retunFFGorupIds',
					'groupName':groupName
				},
				success: function(response)
				{
					// alert(JSON.stringify(response));
					// alert(response.ids);
					$('#buyerId').val(response.ids)

				},
				error: function (xhr, ajaxOptions, thrownError) {
					alert(xhr.status + " :: " + thrownError);
				}
			});
		});

		$('.selectby').click(function() {
			alert('ok')
		});
	});
</script>

<style type="text/css">
	#ffcustom .ccolumn {
		margin-bottom:12px;
	}
	#ffcustom textarea {
		width:100%;
		height:80px;
	}
	#ffcustom .fv-custom-create {
		display:none;
	}
</style>

<div id="ffcustom">
	<div class="pas_rumen text_title">
		TENDERS, STREAMS
	</div>
	<br />

	<div class="container-fluid">
		${data['tenderMenu']}
		<br /><br />

		<div class="text-center">
			<a href="javascript:void(0);" class="fv-custom-link switch_menu_passive">Get feature vectors</a>
		</div>
		<br /><br />

		<div class="fv-custom-create">
			<form method="get" action="">
				<input type="hidden" name="m" value="tenders" />
				<input type="hidden" name="a" value="stream_story" />
				<input type="hidden" name="t" value="dlff_file" />

				<div class="row">
					<div class="col-sm-3 ccolumn">
						Select buyer groups:
					</div>
					<div class="col-sm-9 ccolumn">
						<select class="buyerg_select">
							<option value="0">no group selected</option>
							%for groupValue, groupName in data["buyerGroups"].items():
								<option value="${groupValue}">
									${groupName}
								</option>
							%endfor
						</select>
					</div>

					<div class="col-sm-3 ccolumn">
						Enter buyer IDs:
					</div>
					<div class="col-sm-9 ccolumn">
						<textarea name="buyerId" id="buyerId" value=""></textarea>
					</div>

					<div class="col-sm-3 ccolumn">
						Enter bidder IDs:
					</div>
					<div class="col-sm-9 ccolumn">
						<textarea name="bidderId" id="bidderId" value=""></textarea>
					</div>

					<div class="col-sm-3 ccolumn">
						Strictly numeric data:
					</div>
					<div class="col-sm-9 ccolumn">
						<input type="checkbox" checked="checked" name="strictly_numeric" value="1" style="margin:6px;" />
					</div>

					<div class="col-sm-3 ccolumn">
						Download data file:
					</div>
					<div class="col-sm-9 ccolumn">
						<input type="submit" name="Get data!" value="Get data!" />
					</div>
				</div>
			</form>
			<br /><br />
		</div>

		<div>
			StreamStory is a tool, which which can extract a structure and
			regularities within the data. It can show the state of the monitored
			process, activity and could be also used as anomaly detection tool.
			StreamStory could be accessed on <a href="http://streamstory.ijs.si">http://streamstory.ijs.si</a>.
			<br /><br />
			StreamStory can help you interpret temporal data of different kinds. It
			is useful for the analysis and exploration of large multivariate time
			series. StreamStory has several mechanisms to uncover and in particular
			explain the structure within the data. These mechanisms are visual
			(hierarchical Markov chain, charts, decision trees, parallel
			coordinates) and also a textual narrative explaining/summarizing states
			and patterns within the data.
			<br /><br />
			StreamStory uses sparse feature vectors as its input. with our tool you
			can transform the dynamic network into a sparse feature vectors. Input
			data for a StremStory tool could be in numeric or categorical form, and
			you can choose to export data in strictly numeric form or with text
			labels. Using labels is recommended, since StreamStory tool can use
			these labels as a textual narrative explaining or summarizing states and
			patterns within the data. This makes users to much easily uncover the
			dynamic of the public spending and to spot regularities and anomalies in
			public spending data.
			<br /><br />
			Through the web interface, you can select public procurement data for
			one or more buyers or one or more bidders. Also, a group of specific
			buyers and bidders (who had the “relationship”, i. e. bidders who won
			the contracts for specific buyers) could be selected.
		</div>
		<br /><br />
	</div>
</div>

