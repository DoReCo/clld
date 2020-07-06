## Language-specific page
## Should load a description and a 'contribution' table (texts)

<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">${_('Language')} ${ctx.name}</%block>

<h2>${_('Language')} ${ctx.name}</h2>

<br/><br/><br/><br/><br/><br/>
<br/><br/><br/><br/><br/><br/>

${request.get_datatable('contributions', h.models.Contribution, glottocode=ctx.id).render()}

<%def name="sidebar()">
    ${util.codes()}
    ${util.language_meta()}
</%def>
