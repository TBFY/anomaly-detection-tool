## -*- coding: utf-8 -*-

<div class="te_menu">
	<div class="container-fluid">
		<div class="row no-gutters justify-content-center">
			<div class="col-lg-2 col-sm-3 col-6">
				<a class="method_menu ${'method_menu_active' if data['query_a'] == 'dtree' else ''}" href="?m=tenders&amp;a=dtree">
					<img src="/images/icon_dtree.png" alt="Tree" class="img-fluid" style="width:70%;" />
					<br />
					<span class="method_menu_text">D-TREE</span>
				</a>
			</div>
			<div class="col-lg-2 col-sm-3 col-6">
				<a class="method_menu ${'method_menu_active' if data['query_a'] == 'cluster' else ''}" href="?m=tenders&amp;a=cluster">
					<img src="/images/icon_cluster.png" alt="clusters" class="img-fluid" style="width:70%;" />
					<br />
					<span class="method_menu_text">CLUSTERS</span>
				</a>
			</div>
			<div class="col-lg-2 col-sm-3 col-6">
				<a class="method_menu ${'method_menu_active' if data['query_a'] == 'ratios' else ''}" href="?m=tenders&amp;a=ratios&amp;t=rev_per_employee">
					<img src="/images/icon_relations.png" alt="revenue" class="img-fluid" style="width:70%;" />
					<br />
					<span class="method_menu_text">RATIOS</span>
				</a>
			</div>

			<div class="col-lg-2 col-sm-3 col-6">
				<a class="method_menu ${'method_menu_active' if data['query_a'] == 'distributions' else ''}" href="?m=tenders&amp;a=distributions&amp;t=num_of_offers">
					<img src="/images/icon_bar.png" alt="Distributions" class="img-fluid" style="width:70%;" />
					<br />
					<span class="method_menu_text">DISTRIBUTIONS</span>
				</a>
			</div>

			<div class="col-lg-2 col-sm-3 col-6">
				<a class="method_menu ${'method_menu_active' if data['query_a'] == 'dependencies' else ''}" href="?m=tenders&amp;a=dependencies&amp;t=buyer2bidder">
					<img src="/images/icon_pie.png" alt="Dependencies" class="img-fluid" style="width:70%;" />
					<br />
					<span class="method_menu_text">DEPENDENCIES</span>
				</a>
			</div>

			<div class="col-lg-2 col-sm-3 col-6">
				<a class="method_menu ${'method_menu_active' if data['query_a'] == 'stream_story' else ''}" href="?m=tenders&amp;a=stream_story">
					<img src="/images/icon_nodes.png" alt="stream story" class="img-fluid" style="width:70%;" />
					<br />
					<span class="method_menu_text">STREAMS</span>
				</a>
			</div>
		</div>
	</div>

	%if data['query_a'] == 'ratios':
		<br /><br />
		<div class="tab_section">
			<div class="container-fluid" style="padding:0;">
				<a class="tab_common ${'tab_active' if data['query_t'] == 'rev_per_employee' else 'tab_passive'}" href="?m=tenders&amp;a=ratios&amp;t=rev_per_employee">
					Revenue/employee
				</a>
				<a class="tab_common ${'tab_active' if data['query_t'] == 'budget_assesment' else 'tab_passive'}" href="?m=tenders&amp;a=ratios&amp;t=budget_assesment">
					Budget assess
				</a>
				<!--
				<a class="tab_common ${'tab_active' if data['query_t'] == 'custom' else 'tab_passive'}" href="?m=tenders&amp;a=ratios&amp;t=custom">
					Custom
				</a>
				-->
				<div class="clearfix"></div>
			</div>
		</div>
	%endif

	%if data['query_a'] == 'distributions':
		<br /><br />
		<div class="tab_section">
			<div class="container-fluid" style="padding:0;">
				<a class="tab_common ${'tab_active' if data['query_t'] == 'num_of_offers' else 'tab_passive'}" href="?m=tenders&amp;a=distributions&amp;t=num_of_offers">
					Offers received
				</a>
				<a class="tab_common ${'tab_active' if data['query_t'] == 'budget_assessment' else 'tab_passive'}" href="?m=tenders&amp;a=distributions&amp;t=budget_assessment">
					Budget assess
				</a>
				<!--
				<a class="tab_common ${'tab_active' if data['query_t'] == 'custom' else 'tab_passive'}" href="?m=tenders&amp;a=distributions&amp;t=custom">
					Custom
				</a>
				-->
				<div class="clearfix"></div>
			</div>
		</div>
	%endif

	%if data['query_a'] == 'dependencies':
		<br /><br />
		<div class="tab_section">
			<div class="container-fluid" style="padding:0;">
				<a class="tab_common ${'tab_active' if data['query_t'] == 'buyer2bidder' else 'tab_passive'}" href="?m=tenders&amp;a=dependencies&amp;t=buyer2bidder">
					Buyers
				</a>
				<a class="tab_common ${'tab_active' if data['query_t'] == 'bidder2buyer' else 'tab_passive'}" href="?m=tenders&amp;a=dependencies&amp;t=bidder2buyer">
					Bidders
				</a>
				<a class="tab_common ${'tab_active' if data['query_t'] == 'mutual' else 'tab_passive'}" href="?m=tenders&amp;a=dependencies&amp;t=mutual">
					Mutual
				</a>
				<div class="clearfix"></div>
			</div>
		</div>
	%endif

</div>

