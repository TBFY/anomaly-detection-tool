


	function renderDataFormatAjpes(dataArray)
	{
		// create head
		// create head

		returnHtml = '<div class="row">';
		returnHtml += '<div class="col-9 chart_meta_col"><b>Bidder:</b></div>';
		returnHtml += '<div class="col-3 chart_meta_col chart_meta_col_r"><b>Score:</b></div>';

		// add data
		// add data

		for (var i = 0; i < dataArray.length; i++)
		{
			d = dataArray[i];
			//console.log(d);
			returnHtml += '<div class="col-9 chart_meta_col">';
			returnHtml += d.company_name;
			returnHtml += '<div class="text_90">[id:' + d.company_id + ']</div>';
			returnHtml += '</div>';
			returnHtml += '<div class="col-3 chart_meta_col chart_meta_col_r">';
			returnHtml += d.score;
			returnHtml += '</div>';
		}

		// close html
		// close html

		returnHtml += '</div>';

		// return html
		// return html

		return returnHtml;
	}
