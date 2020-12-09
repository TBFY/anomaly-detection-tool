
	function renderDataFormatMJU(dataArray)
	{
		// create head
		// create head

		returnHtml = '<div class="row">';
		returnHtml += '<div class="col-2 chart_meta_col"><b>Anomaly:</b></div>';
		returnHtml += '<div class="col-2 chart_meta_col"><b>Company Id:</b></div>';
		returnHtml += '<div class="col-8 chart_meta_col chart_meta_col_r">Company Name</b></div>';

		// add data
		// add data

		for (var i = 0; i < dataArray.length; i++)
		{
			d = dataArray[i];
			//renderFunctionParams = ['bidderId', 'buyerId', 'bidderName', 'buyerName', 'bidder_employees', 'tender_amount'];
			returnHtml += '<div class="col-2 chart_meta_col">';
			returnHtml += d.common_anomaly_value.toFixed(2);
			returnHtml += '</div>';
			returnHtml += '<div class="col-2 chart_meta_col"><a class="link_nepodcrtan" target="_blank" href="/?m=orgs&a=source_mju&id=' + d.company_id + '">';
			returnHtml += d.company_id;
			returnHtml += '</a></div>';
			returnHtml += '<div class="col-8 chart_meta_col chart_meta_col_r"><a class="link_nepodcrtan" target="_blank" href="/?m=orgs&a=source_mju&id=' + d.company_id + '">';
			returnHtml += d.company_name;
			returnHtml += '</a></div>';
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
