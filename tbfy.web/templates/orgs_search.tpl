## -*- coding: utf-8 -*-

<style type="text/css">
    .searchbox_field {
        -webkit-border-radius: 15px;
        -moz-border-radius: 15px;
        border-radius: 15px;
        width:75%
    }
	.company_row {
		padding:20px 0px;
		margin-left:30px;
		border-top:2px dashed #01488C;
	}
</style>

<script type="text/javascript">
	$( document ).ready(function()
	{
	});
</script>

<div id="organizations_search">
	<div class="pas_rumen text_title">
		ENTITY SEARCH
	</div>
	<br /><br />

	<div class="container-fluid">
	    <div class="row no-gutters">
	        <div class="col-sm-8 offset-sm-2 text-center">
	            <form>
                    <input type="hidden" name="m" value="orgs" />
                    <input type="hidden" name="a" value="search" />
					<input  class="searchbox_field" type="text" name="q" value="${data['q']}" />
					<input type="submit" name="Search" value="Search" class="btn-moder" style="width:auto; display:inline;" />
                </form>
	        </div>
	    </div>
	    <br /><br />

		<div class="text_140">Search results:</div>
		<br /><br />

		% if len(data['companyList']) == 0:
		    No companies found.
		% else:
		    % for company_id, row in data['companyList'].items():
		        <div class="row no-gutters company_row">
		            <div class="col-3"><a href="/?m=orgs&amp;a=source_mju&amp;id=${row['company_id']}" target="_blank">${row['company_id']}</a></div>
		            <div class="col-9"><a href="/?m=orgs&amp;a=source_mju&amp;id=${row['company_id']}" target="_blank">${row['company_name']}</a></div>
		        </div>
		    % endfor
		    <div class="row no-gutters company_row">&nbsp;</div>
		% endif
	</div>
	<br /><br />
</div>