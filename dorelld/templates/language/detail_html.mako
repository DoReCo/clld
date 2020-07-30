## Language-specific page

    ## load stuff
<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">${_('Language')} ${ctx.name}</%block>
    ## get the description file
<%
import os
d = os.path.join(os.path.abspath(os.path.dirname(u.__file__)),
                 "templates","descriptions")
%>

    ## we'll need jquery
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jequery.min.js"></script>


    ## ## Now we can start writing ## ##


    ## title
<h2>${_('Language')} ${ctx.name}</h2>

    ## Accordion
<div class="accordion" id="acc" style="margin-top: 1em; clear: right;">
        ## Information
    <%util:accordion_group eid="acc_info" parent="acc" title="Information" open="True">
		<style>td {text-indent: 10px;}</style>
		<table>
			<tr>
				% if ctx.fam_glottocode == "na":
					<td align="left"> <b>Family:</b></td>
					<td align="left"> ${ctx.family}</td>
				% else:
					<td align="left"> <b>Family:</b></td>
					<td align="left"> ${ctx.fam_link()} 
					                  (${ctx.fam_glottocode})</td>
				% endif
			</tr>
			<tr>
				<td align="left"> <b>Macro-area:</b></td>
				<td align="left"> ${ctx.area}</td>
			</tr>
            <tr>
				<td align="left"> <b>Corpus owner(s):</b></td>
				<td align="left"> ${ctx.creator}</td>
            </tr>
            % if not ctx.archive == "na":
                <tr>
                    <td align="left"> <b>Archive:</b></td>
                    <td align="left"> ${ctx.arc_link()}</td>
                </tr>
            % endif
            <tr>
                <td align="left"> <b>Translation:</b></td>
                <td align="left"> ${ctx.transl}</td>
            </tr>
        </table>
    </%util:accordion_group>
        ## Description
    <%util:accordion_group eid="acc_desc" parent="acc" title="Description">
        <%include file="${d}/${ctx.id}.html"/>
    </%util:accordion_group>
</div>

    ## Datatable
</br>
    ## core vs extended tabs
<div class="tabbable">
    <ul class="nav nav-tabs">
        <li class="active"><a href="#cor" data-toggle="tab">Core</a></li>
        <li><a href="#ext" data-toggle="tab">Extended</a></li>
    </ul>
    <div class="tab-content">
		<div id="cor" class="tab-pane active">
		    ${u.get_form(ctx.id)}
		    ${request.get_datatable('contributions', h.models.Contribution, glottocode=ctx.id).render()}
		</div>
		<div id="ext" class="tab-pane">
			${u.get_form(ctx.id,True)}
		    ${request.get_datatable('contributions', h.models.Contribution, glottocode=ctx.id, extended="True").render()}
		</div>
    </div>
</div>

    ## sidebar
<%def name="sidebar()">
    ${util.codes()}
    ${util.language_meta()}
</%def>
