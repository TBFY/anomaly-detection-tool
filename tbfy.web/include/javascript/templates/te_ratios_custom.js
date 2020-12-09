
    /*
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
			returnHtml += '<div class="col-4 chart_meta_col">';
			returnHtml += d.buyerName;
			returnHtml += '<div class="text_90">[id:' + d.buyerId + ']</div>';
			returnHtml += '</div>';
			returnHtml += '<div class="col-4 chart_meta_col">';
			returnHtml += d.bidderName;
			returnHtml += '<div class="text_90">[id:' + d.bidderId + ']</div>';
			returnHtml += '</div>';
			returnHtml += '<div class="col-4 chart_meta_col chart_meta_col_r">[' + d.tender_amount + ' EUR] / [' + d.bidder_employees + ' employee(s)]</div>';

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
	*/