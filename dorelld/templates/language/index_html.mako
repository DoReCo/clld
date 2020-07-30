## List of all languages

<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">${_('Languages')}</%block>

<h2>${_('Languages')}</h2>

<div class="accordion" id="lang" style="margin-top: 1em; clear: right;">
    % if map_ or request.map:
    <%util:accordion_group eid="lang_map" parent="lang" title="Map" open="True">
        ${(map_ or request.map).render()}
    </%util:accordion_group>
    % endif
</div>

<div class="tabbable">
    <ul class="nav nav-tabs">
        <li class="active"><a href="#cor" data-toggle="tab">Core</a></li>
        <li><a href="#ext" data-toggle="tab">Extended</a></li>
    </ul>
    <div class="tab-content">
        <div id="cor" class="tab-pane active">
            ${u.get_form("languages")}
            ${request.get_datatable('languages',h.models.Language).render()}
        </div>
        <div id="ext" class="tab-pane">
            ${u.get_form("languages",True)}
            ${request.get_datatable('languages',h.models.Language, extended="True").render()}
        </div>
    </div>
</div>
