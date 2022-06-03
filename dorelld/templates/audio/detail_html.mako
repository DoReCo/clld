<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<%block name="title">${_('Parameter')} ${ctx.name}</%block>



##<h2>${_('Parameter')} ${ctx.name}</h2>

% if ctx.description:
##<p>${_("ceci n'est pas traduit dans PO")} ${ctx.description}</p>
% endif

##<p>${ctx}</p>

<ul>
% for a in ['GET']:
##   <li>Item ${loop.index}: ${a}</li>
% endfor
</ul>

<div style="clear: both"/>
% if map_ or request.map:
${(map_ or request.map).render()}
% endif

<%
from dorelld.util import get_audio
%>

<p>${get_audio(ctx)}</p>

##<p> End of static page </p>
