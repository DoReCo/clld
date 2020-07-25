## Language-specific page
## Should load a description and a 'contribution' table (texts)

    ## load stuff
<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">${_('Language')} ${ctx.name}</%block>
    ## Download form
<style>
	form {display: inline; float: left; margin: 0px; padding: 0px;}
	input {float: left; margin-right: 10px;}
	select {float: left; margin-right: 10px;}
	label {float: left; margin-right: 10px;}
	p.form {float:left; margin-right: 10px; padding: 3px;}
</style>
<%def name="form(ext)">
	<form method="post" action="/doreLoad">
	    % if ext:
	        <input type="hidden" id="f_core" name="core" value=True>
	    % else:
	        <input type="hidden" id="f_core" name="core" value=False>
	    % endif
		<input type="hidden" id="f_id" name="id" value=${ctx.id}>
		<input type="checkbox" id="f_wav" name="WAV" value="WAV" style="">
		<label for="f_wav">WAV</label>
		<select id="f_format" name="format">
			<option value="all">All types</option>
			<option value="praat">Praat (.TextGrid)</option>
			<option value="elan">Elan (.eaf)</option>
			<option value="tabular">Tabular (.csv)</option>
			<option value="tei">TEI (.xml)</option>
			<option value="cross1">Crosstable_1</option>
			<option value="cross2">Crosstable_2</option>
			<option value="cross3">Crosstable_3</option>
		</select>
		<input type="submit" value="Download">
	</form>
</%def>
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
		    <p class="form"><b>Download all core files:</b></p>
		    <%self:form ext="${False}"></%self:form>
		    ${request.get_datatable('contributions', h.models.Contribution, glottocode=ctx.id).render()}
		</div>
		<div id="ext" class="tab-pane">
			<p class="form"><b>Download all files:</b></p>
		    <%self:form ext="${True}"></%self:form>
		</div>
    </div>
</div>

    ## sidebar
<%def name="sidebar()">
    ${util.codes()}
    ${util.language_meta()}
</%def>
