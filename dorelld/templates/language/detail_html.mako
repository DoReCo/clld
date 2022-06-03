## Language-specific page

    ## load stuff
<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">${_('Language')} ${ctx.name}</%block>
    ## style
<style>td {text-indent: 10px;}
.popover {top: 0px !important;}</style>
    ## get the description file (+ source object)
<%
import os
d = os.path.join(os.path.abspath(os.path.dirname(u.__file__)),
                 "templates")
desc = os.path.join(d,"descriptions","information_"+ctx.id+".html"); d_ch = False
pres = os.path.join(d,"presentations",ctx.id+".html"); p_ch = False
if os.path.isfile(desc):
    d_ch = True
if os.path.isfile(pres):
    p_ch = True
result = request.db.query(h.models.Source).filter(h.models.Source.id==ctx.id).all()
if result :
    print('languages/detail_html.mako', result, result[0])
    s = result[0]
else:
    print('no result', ctx.id)
    s = ctx

%>

    ## ## Now we can start writing ## ##
    ## title
    <h2>${_('Language')} ${ctx.name}</h2>

    <div class="span8" style="margin-left:0px;">
            ## Accordion
        <div class="accordion" id="acc" style="margin-top: 1em; clear: right;">
                ## Information
            <%util:accordion_group eid="acc_info" parent="acc" title="Information" open="True">
                    ## metadata
                <table>
                    <tr>
                        <td align="left"> <b>Corpus creator(s):</b></td>
                        <td align="left"> ${ctx.creator}</td>
                    </tr>
                    % if not ctx.archive == "na":
                        <tr>
                            <td align="left"> <b>Archive:</b></td>
                            <td align="left"> ${ctx.arc_link()}</td>
                        </tr>
                    % endif
                    <tr>
                        <td align="left"> <b>Annotation files license:</b></td>
                        <td align="left"> ${ctx.get_lic()}</td>
                    </tr>
                    <tr>
                        <td align="left"> <b>Audio files license:</b></td>
                        <td align="left"> ${ctx.get_alic()}</td>
                    </tr>
                    <tr>
                        <td align="left"> <b>Translation:</b></td>
                        <td align="left"> ${ctx.transl}</td>
                    </tr>
                </table>
                    ## custom description
                % if d_ch:
                    <%include file="${desc}"/>
                % endif

        ##<p>${desc} ${pres}</p>

        <%
        from dorelld.util import get_desc, get_cite, get_source, get_nak
        sour = s
        %>
            <p>${get_desc(ctx, sour=sour)}</p>
            ##<p>${get_nak(ctx, sour=sour)}</p>
                ## cite button
                ${h.cite_button(request, s)}
            </%util:accordion_group>
                ## Description
            % if p_ch:
                <%util:accordion_group eid="acc_desc" parent="acc" title="Description">
                    <%include file="${pres}"/>
                </%util:accordion_group>
            % endif
        </div>
    </div>

    ## sidebar
    <div id="sidebar" class="span4" style="margin-left:1%">
            ## glottocode/isocode
        ${util.codes()}
            ## map
        ${util.language_meta()}
            ## language information
        <div class="accordion" id="side" style="margin-top: 1em; clear: right;">
             <%util:accordion_group eid="side_info" parent="side" title="Language Information" open="True">
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
                </table>
            </%util:accordion_group>
        </div>
    </div>
</div>


    ## Datatable

    ## core vs extended tabs
<div class="tabbable span12" style="margin-left:0px;">
    <ul class="nav nav-tabs">
        <li class="active"><a href="#cor" data-toggle="tab">Core set</a></li>
        <li><a href="#ext" data-toggle="tab">Extended set</a></li>
    </ul>
    <div class="tab-content">
		<div id="cor" class="tab-pane active" style="width:99%">
		    ${u.get_button(ctx.id)}
		    ${u.Handle2Nakala(request.get_datatable('contributions', h.models.Contribution, glottocode=ctx.id)).render()}
		</div>
		<div id="ext" class="tab-pane" style="width:99%">
			${u.get_button(ctx.id,True)}
		    ${request.get_datatable('contributions', h.models.Contribution, glottocode=ctx.id, extended="True").render()}
		</div>
    </div>
</div>