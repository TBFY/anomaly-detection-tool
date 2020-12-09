## -*- coding: utf-8 -*-

<style type="text/css">
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
		<div class="text_140">Entity search</div>
		<br /><br />

		% if len(data['id_company']) > 0:
			<div>
    			No tender data found for company with id ${data['id_company']} in the database. Please retry your search.
			</div>
			<br /><br />
		% endif

		<form method="get" action="">
			<input type="hidden" name="m" value="orgs" />
			<input type="hidden" name="a" value="source_mju" />
			<div class="row">
				<div class="col-3 text-right" style="padding-top:5px;">Enter company Id: </div>
				<div class="col-9">
					<input type="text" name="id" />
					<input type="submit" name="Search" value="Search" />
				</div>

			</div>
		</form>
	</div>
	<br /><br />
</div>