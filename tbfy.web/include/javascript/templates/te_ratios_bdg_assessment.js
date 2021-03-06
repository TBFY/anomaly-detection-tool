
	function renderDataFormatMJU(dataArray)
	{
		// create head
		// create head

		returnHtml = '<div class="row">';
		returnHtml += '<div class="col-4 chart_meta_col"><b>Buyer:</b></div>';
		returnHtml += '<div class="col-4 chart_meta_col"><b>Bidder:</b></div>';
		returnHtml += '<div class="col-4 chart_meta_col chart_meta_col_r"><b>Assessed value / Final value</b></div>';

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
			returnHtml += '<br /><span class="text_90">[id:' + d.bidderId + ']</span>';
			returnHtml += '</a></div>';
			returnHtml += '<div class="col-4 chart_meta_col chart_meta_col_r">[' + d.tender_assessed + ' EUR] / [' + d.tender_amount + ' EUR]</div>';

		}

		// close html
		// close html

		returnHtml += '</div>';

		// return html
		// return html

		return returnHtml;
	}

	function renderDataFormatKG(bidderId, buyerId, bidder_employees, tender_amount, ocid)
	{
		/*
		var renderFunctionParams = ['bidderId', 'buyerId', 'bidder_employees', 'tender_amount', 'ocid']
		if('${data["dataSourceLstSelected"]}' == 'si-ministry')
		{
			renderFunction = 'renderDataFormatMJU';
			renderFunctionParams = ['bidderId', 'buyerId', 'bidderName', 'buyerName', 'bidder_employees', 'tender_amount'];
		}
		*/

		returnHtml = '';

		returnHtml += '<div style="border-bottom:1px solid #000; padding:5px 0px;">';
		returnHtml += "<a href='http://tbfy.librairy.linkeddata.es/kg-api/award/" + ocid + "' target='_blank'>";
		returnHtml += "bidder id: " + bidderId + ", employees: " + bidder_employees + ", receives: " + tender_amount;
		returnHtml += "<br />";
		returnHtml += "buyerId: " + buyerId;
		returnHtml += "</a>";
		returnHtml += '</div>';

		return returnHtml;
	}