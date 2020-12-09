
	function renderDataFormatMJU(dataArray)
	{
		// create head
		// create head

		returnHtml = '<div class="row">';
		returnHtml += '<div class="col-4 chart_meta_col"><b>Buyer:</b></div>';
		returnHtml += '<div class="col-4 chart_meta_col"><b>Bidder:</b></div>';
		returnHtml += '<div class="col-4 chart_meta_col chart_meta_col_r"><b>Tender amount / Employee num.</b></div>';

		// add data
		// add data

		for (var i = 0; i < dataArray.length; i++)
		{
			d = dataArray[i];
			//renderFunctionParams = ['bidderId', 'buyerId', 'bidderName', 'buyerName', 'bidder_employees', 'tender_amount'];
			returnHtml += '<div class="col-4 chart_meta_col"><a class="link_nepodcrtan" target="_blank" href="/?m=orgs&a=source_mju&id=' + d.buyerId + '">';
			returnHtml += d.buyerName;
			returnHtml += '<br /><span class="text_90">[id:' + d.buyerId + ']</span>';
			returnHtml += '</a></div>';
			returnHtml += '<div class="col-4 chart_meta_col"><a class="link_nepodcrtan" target="_blank" href="/?m=orgs&a=source_mju&id=' + d.bidderId + '">';
			returnHtml += d.bidderName;
			returnHtml += '<br /><span  class="text_90">[id:' + d.bidderId + ']</span >';
			returnHtml += '</a></div>';
			returnHtml += '<div class="col-4 chart_meta_col chart_meta_col_r">[' + d.tender_amount + ' EUR] / [' + d.bidder_employees + ' employee(s)]</div>';
		}

		// close html
		// close html

		returnHtml += '</div>';

		// return html
		// return html

		return returnHtml;
	}

	function renderDataFormatKG(dataArray)
	{
		// create head
		// create head

		returnHtml = '<div class="row">';
		returnHtml += '<div class="col-4 chart_meta_col"><b>Buyer:</b></div>';
		returnHtml += '<div class="col-4 chart_meta_col"><b>Bidder:</b></div>';
		returnHtml += '<div class="col-4 chart_meta_col chart_meta_col_r"><b>Tender amount / Employee num.</b></div>';

		for (var i = 0; i < dataArray.length; i++)
		{
			d = dataArray[i];
			//renderFunctionParams = [x_val, y_value, buyerId, bidderId, tender_amount, bidder_employees, cpv, ocid, currency, award_id];
			returnHtml += '<div class="col-4 chart_meta_col"><a href="http://tbfy.librairy.linkeddata.es/kg-api/organisation/' + d.buyerId + '" target="_blank">';
			returnHtml += d.buyerId;
			returnHtml += '<br /><span class="text_90">[id:' + d.buyerId + ']</span>';
			returnHtml += '</a></div>';
			returnHtml += '<div class="col-4 chart_meta_col"><a href="http://tbfy.librairy.linkeddata.es/kg-api/organisation/' + d.supplier_jurisdiction + '-' + d.bidderId + '" target="_blank">';
			returnHtml += d.bidderId;
			returnHtml += '<br /><span  class="text_90">[id:' + d.bidderId + ']</span >';
			returnHtml += '</a></div>';
			returnHtml += '<div class="col-4 chart_meta_col chart_meta_col_r"><a href="http://tbfy.librairy.linkeddata.es/kg-api/award/' + d.ocid + '_' + d.award_id + '" target="_blank">';
			returnHtml += '[' + d.tender_amount + ' <span style="text-transform:uppercase;">' + d.currency_name + '</span>] / [' + d.bidder_employees + ' employee(s)]';
			returnHtml += '</a></div>';
		}

		// close html
		// close html

		returnHtml += '</div>';

		// return html
		// return html

		return returnHtml;
	}