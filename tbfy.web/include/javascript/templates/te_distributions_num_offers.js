
	function renderDataFormatMJU(dataArray)
	{
		// create head
		// create head

		returnHtml = '<div class="row">';
		returnHtml += '<div class="col-6 chart_meta_col"><b>Bidder:</b></div>';
		returnHtml += '<div class="col-4 chart_meta_col"><b>Expected distribution /<br />Company distribution:</b></div>';
		returnHtml += '<div class="col-2 chart_meta_col chart_meta_col_r"><b>Awards num /<br /> Score:</b></div>';

		// add data
		// add data

		for (var i = 0; i < dataArray.length; i++)
		{
			d = dataArray[i];
			//console.log(d);
			returnHtml += '<div class="col-6 chart_meta_col"><a class="link_nepodcrtan" target="_blank" href="/?m=orgs&a=source_mju&id=' + d.bidder_id + '">';
			returnHtml += d.bidder_name;
			returnHtml += '<br /><span class="text_90">[id:' + d.bidder_id + ']</span>';
			returnHtml += '</a></div>';
			returnHtml += '<div class="col-4 chart_meta_col">[';
			returnHtml += common_distr.replace(/-/g, '%]-[');
			returnHtml += '%]<br />[';
			returnHtml += d.bidder_distr.replace(/-/g, '%]-[');
			returnHtml += '%]</div>';
			returnHtml += '<div class="col-2 chart_meta_col chart_meta_col_r">';
			returnHtml += d.occurence_num;
			returnHtml += '<br />';
			returnHtml += d.deltavalue;
			returnHtml += '</div>';
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