## -*- coding: utf-8 -*-

<script type="text/javascript">
	$( document ).ready(function()
	{
		$('.fileListSelect').change(function()
		{
			$('#isciForma').submit();
		});
	});
</script>

<div class="search_box">
	<form id="isciForma" method="get" action="">
		<input type="hidden" name="m" value="analysis" />
		<input type="hidden" name="a" value="transactions" />
		<input type="hidden" name="t" value="${data['pageAddress']}" />

		<br />
		<h2>${data['templateTitle']}</h2>

		<br />
		<select name="idfile" class="fileListSelect">
			<option>izberi datoteko</option>
			%for classificator in data["fileList"]:
				<option value="${classificator}" ${'selected="selected"' if data["idfile"] == classificator else ''}>${data["fileList"][classificator]}</option>
			%endfor
		</select>
		<br /><br />
		<h5>Highest deviations:</h5>
		<br />
		%if len(data["companyList"]) > 0:
			%for row in data["companyList"]:
				<div>${row['company_id']} :: ${row['company_name']} (${row['deviation']})</div>
			%endfor
		%else:
			no data available
		%endif
	</form>
</div>
