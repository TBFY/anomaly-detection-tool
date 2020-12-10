## -*- coding: utf-8 -*-
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <meta name='description' content='' />
		<meta name='keywords' content='' />
		<meta name="author" content="Matej Posinković" />
		<meta name="design" content="Ana Fabjan" />
        <link rel="stylesheet" type="text/css" href="/include/css/bootstrap/bootstrap.min.css"></link>
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto+Mono:400,400i,700,700i&display=swap&subset=latin-ext" />
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Rubik:wght@300;400&display=swap" />
		<link rel="stylesheet" type="text/css" href="/include/css/tbfy.basic.css?v=3.0"/>
		<link rel="stylesheet" type="text/css" href="/include/css/tbfy.classes.css?v=3.0"/>


        <script type="text/javascript" src="/include/javascript/bootstrap/bootstrap.min.js"></script>
        <script type="text/javascript" src="/include/javascript/jquery-3.3.1.min.js"></script>
        <script type="text/javascript" src="/include/javascript/d3/d3.min.js"></script>
        <script type="text/javascript" src="/include/javascript/functions.js"></script>

        <title>TBFY</title>
    </head>

    <body>
        <script type="text/javascript">
            $(document).ready(function()
            {
            });
        </script>


        <div class="glava_spletna_stran container-fluid">
            <div class="row no-gutters">
                <div class="col-md-3 col-12 logo_align">
                    <span><a href="/" style="display:inline-block;"><img src="images/tbfy_logo.svg" alt="TBFY" width="200" class="pull-left" /></a></span>
                </div>
                <div class="col-md-9 col-sm-12 switch_menu_box">
                        <div class="row no-gutters w-100">
                            <div class="col-md-7 col-6 switch_menu_btn_align">
                                <a href="?m=transactions" id="menu_link_transactions" class="switch_menu switch_menu${'_active' if data['query_m'] == 'transactions' else '_passive'}">Transactions</a>
                            </div>
                            <div class="col-md-5 col-6 switch_menu_btn_align">
                                <a href="?m=tenders" id="menu_link_tenders" class="switch_menu switch_menu${'_active' if data['query_m'] == 'tenders' else '_passive'}">Tenders</a>
                            </div>
                        </div>
                    <div class="clearfix"></div>
                </div>
                <div class="clearfix"></div>
            </div>
        </div>

        <div class="telo_spletna_stran">
            ${contentHtml}
            <!--
            <div id="menu_div_transactions" class="menu menu_div_content text-center" style="display:none;">
                <a class="btn btn-secondary btn_base" href="/">Data visualisation</a>
                <a class="btn btn-primary btn_base" href="/?m=transactions&amp;a=stddev">Average Deviation</a>
                <a href="?m=search&amp;a=towners">Tender owners</a> &nbsp;|&nbsp;
                <a href="?m=search&amp;a=contractors">Contractors</a>
                <a class="btn btn-primary btn_base" href="/?m=transactions&amp;a=jnks">Jenks Natural Breaks</a>
                <a class="btn btn-primary btn_base" href="/?m=transactions&amp;a=periods">Period Margin</a>
                <a class="btn btn-primary btn_base" href="/?m=transactions&amp;a=deriv">Local Extremes</a>
                <a class="btn btn-primary btn_base" href="/?m=transactions&amp;a=part">Time Periods</a>
            </div>
            <div class="clearfix"></div>
            -->
        </div>


        <div class="noga_spletna_stran text_bel">
            <div class="container-fluid">
                <div class="row no-gutters">
                    <div class="col-sm-4">
                        CONTACT
                        <br /><br />
                        Jožef Stefan Institute<br />
                        Jamova cesta 39<br />
                        1000 Ljubljana
                        <br /><br /><br />
                    </div>
                    <div class="col-sm-8">
                        CREDITS
                        <br /><br />
                        <div class="noga_eu_flag">
                            TheyBuyForYou has received funding from the European Union's Horizon 2020 research and innovation programme under grant agreement No 780247.
                        </div>
                        <br />

                        <div class="noga_flaticons">
                            Icons made by Becris from <a href="https://www.flaticon.com/" class="link_bel" target="_blank">www.flaticon.com</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
</html>
