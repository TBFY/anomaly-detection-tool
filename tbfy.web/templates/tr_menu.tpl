## -*- coding: utf-8 -*-

<div class="tr_menu">
	<div class="row no-gutters justify-content-center">
		<div class="col-lg-2 col-sm-3 col-6">
			<a class="method_menu ${'method_menu_active' if data['query_a'] == 'jnks' else ''}" href="?m=transactions&amp;a=jnks">
				<img src="/images/icon_pie.png" alt="Tree" class="img-fluid" style="width:70%;" />
				<span class="method_menu_text">CLUSTERS</span>
			</a>
		</div>
		<div class="col-lg-2 col-sm-3 col-6">
			<a class="method_menu ${'method_menu_active' if data['query_a'] == 'periods' else ''}" href="?m=transactions&amp;a=periods">
				<img src="/images/icon_nodes.png" alt="Tree" class="img-fluid" style="width:70%;" />
				<span class="method_menu_text">PERIODS</span>
			</a>
		</div>
		<div class="col-lg-2 col-sm-3 col-6">
			<a class="method_menu ${'method_menu_active' if data['query_a'] == 'deriv' else ''}" href="?m=transactions&amp;a=deriv">
				<img src="/images/icon_bar.png" alt="Tree" class="img-fluid" style="width:70%;" />
				<span class="method_menu_text">DERIVATIVES</span>
			</a>
		</div>
		<div class="col-lg-2 col-sm-3 col-6">
			<a class="method_menu ${'method_menu_active' if data['query_a'] == 'part' else ''}" href="?m=transactions&amp;a=part">
				<img src="/images/icon_linear.png" alt="Tree" class="img-fluid" style="width:70%;" />
				<span class="method_menu_text">CUMULATIVES</span>
			</a>
		</div>
	</div>
</div>
