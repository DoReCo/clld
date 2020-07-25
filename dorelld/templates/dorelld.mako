<%inherit file="app.mako"/>

##
## define app-level blocks:
##
<%block name="header">
    <a href="${request.route_url('dataset')}">
        <img src="${request.static_url('dorelld:static/header.gif')}"/>
    </a>
</%block>

<%block name="footer">
	<div class="row-fluid" style="padding-top: 15px; border-top: 1px solid black;">
		<div class="span3"></div>
		<div class="span6" style="text-align: center;">
		    <style>.logo {display:inline-block; max-height:60px; padding:5px;}</style>
		    <a href="http://www.cnrs.fr/">
		        <img class="logo" alt="CNRS" src="${request.static_url("dorelld:static/logos/CNRS_logo.png")}" />
		    </a>
		    <a href="https://anr.fr/">
		        <img class="logo" alt="ANR" src="${request.static_url("dorelld:static/logos/ANR_logo.png")}" />
		    </a>
		    <a href="https://www.dfg.de/">
		        <img class="logo" alt="DFG" src="${request.static_url("dorelld:static/logos/DFG_logo.png")}" />
		    </a>
		    <a href="https://www.leibniz-gemeinschaft.de/">
		        <img class="logo" alt="Leibniz" src="${request.static_url("dorelld:static/logos/LEIBNIZ_logo.png")}" />
		    </a>
		    <a href="https://www.univ-lyon2.fr/">
		        <img class="logo" alt="Lyon" src="${request.static_url("dorelld:static/logos/LYON_logo.png")}" />
		    </a>
		    <a href="http://www.ddl.cnrs.fr/">
		        <img class="logo" alt="DDL" src="${request.static_url("dorelld:static/logos/DDL_logo.png")}" />
		    </a>
		    <a href="https://www.leibniz-zas.de/">
		        <img class="logo" alt="ZAS" src="${request.static_url("dorelld:static/logos/ZAS_logo.png")}" />
		    </a>
		    <a href="https://www.bas.uni-muenchen.de/Bas/BasHomeeng.html">
		        <img class="logo" alt="BAS" src="${request.static_url("dorelld:static/logos/BAS_logo.png")}" />
		    </a>
		</div>
		<%doc><div class="span6" style="text-align: center;">
			<% license_icon = h.format_license_icon_url(request) %>
			% if license_icon:
			<a rel="license" href="${request.dataset.license}">
				<img alt="License" style="border-width:0" src="${license_icon}" />
			</a>
			<br />
			% endif
			<%block name="footer_citation">
			${request.dataset.formatted_name()}
			edited by
			<span xmlns:cc="https://creativecommons.org/ns#"
				  property="cc:attributionName"
				  rel="cc:attributionURL">
				${request.dataset.formatted_editors()}
		   </span>
			</%block>
			<br />
			is licensed under a
			<a rel="license" href="${request.dataset.license}">
				${request.dataset.jsondata.get('license_name', request.dataset.license)}</a>.
		</div></%doc>
		<div class="span3" style="float: right; text-align: right;">
			% if request.registry.settings.get('clld.privacy_policy_url'):
				<a class="clld-privacy-policy" href="${request.registry.settings['clld.privacy_policy_url']}">${_('Privacy Policy')}</a><br/>
			% endif
			<a class="clld-disclaimer" href="${request.route_url('legal')}">${_('Disclaimer')}</a>
			<br/>
			% if request.registry.settings.get('clld.github_repos'):
			<a href="https://github.com/${request.registry.settings['clld.github_repos']}">
				<i class="icon-share">&nbsp;</i>
				Application source
				% if request.registry.settings['clld.git_tag']:
					(${request.registry.settings['clld.git_tag']})
				% endif
				on<br/>
				<img height="25" src="${request.static_url('clld:web/static/images/GitHub_Logo.png')}" />
			</a>
			% endif
		</div>
	</div>
</%block>

${next.body()}
