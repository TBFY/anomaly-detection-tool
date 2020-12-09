
	function renderDataFormatMJU(dataArray, cluster_n, xKey, xValue, yKey, yValue)
	{
	    xKeyLw = xKey.toLowerCase();
	    yKeyLw = yKey.toLowerCase();

		// create head
		// create head

		returnHtml = '<div class="row">';
		returnHtml += '<div class="col-1 chart_meta_col"><b>n</b></div>';
		returnHtml += '<div class="col-3 chart_meta_col"><b>Buyer</b></div>';
		returnHtml += '<div class="col-4 chart_meta_col"><b>Bidder</b></div>';
		returnHtml += '<div class="col-2 chart_meta_col"><b>' + yValue + '</b></div>';
		returnHtml += '<div class="col-2 chart_meta_col chart_meta_col_r"><b>' + xValue + '</b></div>';

        var param1 = '';
        var param2 = '';
        var d;
        for (var i = 0; i < dataArray.length; i++)
        {
            d = dataArray[i];
            param1 = eval("d." + yKey);
            param2 = eval("d." + xKey);

            if(yKeyLw in valueKeyArray)
            {
                param1 = parseInt(param1);
                param1 = valueKeyArray[yKeyLw][param1];
            }
            if(xKeyLw in valueKeyArray)
            {
                param2 = parseInt(param2);
                param2 = valueKeyArray[xKeyLw][param2];
            }

            returnHtml += '<div class="col-1 chart_meta_col">';
            returnHtml += cluster_n;
            returnHtml += '</div>';
            returnHtml += '<div class="col-3 chart_meta_col"><a class="link_nepodcrtan" target="_blank" href="/?m=orgs&a=source_mju&id=' + d.NarocnikMaticna + '">'
            returnHtml += d.NarocnikNaziv;
            returnHtml += '<br /><span class="text_90">[id:' + d.NarocnikMaticna + ']</span>';
            returnHtml += '</a></div>';
            returnHtml += '<div class="col-4 chart_meta_col"><a class="link_nepodcrtan" target="_blank" href="/?m=orgs&a=source_mju&id=' + d.PonudnikMaticna + '">'
            returnHtml += d.PonudnikNaziv;
            returnHtml += '<br /><span class="text_90">[id:' + d.PonudnikMaticna + ']</span>';
            returnHtml += '</a></div>';
            returnHtml += '<div class="col-2 chart_meta_col">';
            returnHtml += param1;
            returnHtml += '</a></div>';
            returnHtml += '<div class="col-2 chart_meta_col chart_meta_col_r">'
            returnHtml += param2;
            returnHtml += '</div>';
        }

		// close html
		// close html

		returnHtml += '</div>';

		// return html
		// return html

		return returnHtml;
	}

	function renderDataFormatKG(dataArray, cluster_n, xKey, xValue, yKey, yValue)
	{

	    xKeyLw = xKey.toLowerCase();
	    yKeyLw = yKey.toLowerCase();

	    console.log(xKeyLw);

		// create head
		// create head

		returnHtml = '<div class="row">';
		returnHtml += '<div class="col-1 chart_meta_col"><b>n</b></div>';
		returnHtml += '<div class="col-5 chart_meta_col"><b>Tender details</b></div>';
		returnHtml += '<div class="col-3 chart_meta_col"><b>' + yValue + '</b></div>';
		returnHtml += '<div class="col-3 chart_meta_col chart_meta_col_r"><b>' + xValue + '</b></div>';

        for (var i = 0; i < dataArray.length; i++)
        {
            d = dataArray[i];
            param1 = eval("d." + xKey);
            param2 = eval("d." + yKey);

            returnHtml += '<div class="col-1 chart_meta_col"><b>n</b></div>';
            returnHtml += '<div class="col-5 chart_meta_col"><b>' + d.ocid + '</b></div>';
            returnHtml += '<div class="col-3 chart_meta_col"><b>' + param2 + '</b></div>';
            returnHtml += '<div class="col-3 chart_meta_col chart_meta_col_r"><b>' + param1 + '</b></div>';
        }

		// close html
		// close html

		returnHtml += '</div>';

		// return html
		// return html

		return returnHtml;
	}