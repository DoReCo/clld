<%inherit file="dorelld.mako"/>
<%namespace name="util" file="util.mako"/>
<%! active_menu_item = "about" %>

<%
from dorelld.models import dorEditor
d = request.db.query(dorEditor)
ddl = d.filter(dorEditor.team == "DDL").all(); ld = len(ddl)
zas = d.filter(dorEditor.team == "ZAS").all(); lz = len(zas)
bas = d.filter(dorEditor.team == "BAS").all(); lb = len(bas)
l = ld
if lz > l:
    l = lz
if lb > l:
    l = lb
%>
<style>.int {border: 1px solid #CCCCCC; border-radius: 5px; margin: 5px; padding: 10px;}</style>

<%def name="contextnav()">
    % for name in request.registry.settings['home_comp']:
    ${util.contextnavitem(name)}
    % endfor
</%def>

<div class="int">
    <h2>Project</h2><a href="#project"></a>
    <p>Speech rate and pauses provide us with a window into the cognitive-neural and physiological-articulatory bases of the human language production system, but cross-linguistic variation in this domain remain understudied. This project fills this gap by comparative studies of spontaneously spoken language in a diverse sample of 50 languages. For this purpose, we create a multilingual reference corpus of language documentation data (DoReCo) consisting of annotations and associated audio recordings that are archived at repositories such as The Language Archive (TLA), especially from the DOBES collection. DoReCo will be built from data that are already transcribed, translated into a major language, and time-aligned at the level of discourse units with audio files.</p>
    <p>Within the current project, these data will be time-aligned at the phoneme level. We have identified at least 50 languages, from which corpora of at least 10,000 words can be included in DoReCo, and a subset of at least 30 of these, which are additionally already annotated for morpheme breaks and morpheme glosses. In DoReCo, subcorpora and annotations are treated as citable publications, provided with a permanent identifier and associated with a CC BY 4.0 license. DoReCo will have a lasting effect beyond the specific research goals of the DoReCo project, as a platform for easy access to over one million words of annotated corpus data from over 50 languages for cross-linguistic research on spoken language. This represents an unprecedented contribution to open, reproducible science regarding global linguistic diversity and cultural heritage. Both of DoReCo’s two specific research goals address the universality of constraints on human language arising from species-wide articulatory and cognitive properties:</p>
    <ul>
        <li>Firstly, we investigate patterns of phonetic lengthening with the aim towards establishing universal vs. language-specific patterns in
			<ul>
				<li>(i) the degree to which different types of phonological segments undergo variation in duration (e.g. vowels vs. different types of consonants)–reflecting articulatory and perceptual constraints–and</li>
				<li>(ii) word-final lengthening as indicative of major vs. minor prosodic boundaries–reflecting cognitive constraints on planning and potentially signalling discourse units.</li>
			</ul>
		</li>
        <li>Secondly, we investigate universal vs. language-specific patterns in the temporal distribution of morphemes reflecting cognitive constraints on language use:
			<ul>
				<li>(i) information rate in terms of morphemes per second and</li>
				<li>(ii) the number of morphemes in inter-pausal units</li>
			</ul>
        </li>
    </ul>
<p>The project will be carried out by an interdisciplinary team bringing together expertise on documentary linguistics, phonetics, typology, and quantitative linguistics, with strong institutional support from two leading research centres in Germany and France.</p>
</div>

<div class="int">
	<h2>Team</h2><a href="#team"></a>

	<style>table {}
		   tr {}
		   th {text-align: left; padding-right: 60px;}
		   td.sec {padding-right: 60px;}</style>
	<div class="int">
		<table>
			<tr>
				<th colspan="2">
					<h4><a href="http://www.ddl.cnrs.fr/index.asp" target="_blank" rel="noreferrer noopener" aria-label=" (opens in a new tab)">Laboratoire Dynamique Du Langage</a></h4>
				</th>
				<th colspan="2">
					<h4><a href="http://www.zas.gwz-berlin.de/" target="_blank" rel="noreferrer noopener" aria-label="Leibniz-Zentrum Allgemeine Sprachwissenschaft (opens in a new tab)">Leibniz-Zentrum Allgemeine Sprachwissenschaft</a></h4>
				</th>
				<th colspan="2">
					<h4><a href="https://www.bas.uni-muenchen.de/Bas/BasHomedeu.html" target="_blank" rel="noreferrer noopener" aria-label="Bayerisches Archiv für Sprachsignale (opens in a new tab)">Bayerisches Archiv für Sprachsignale</a></h4>
				</th>
			</tr>
			% for a in range(l):
				<tr>
					% if a >= ld:
						<td></td><td></td>
					% else:
						<td>${ddl[a].name_link()}</td>
						<td class="sec">(${ddl[a].function})</td>
					% endif
					% if a >= lz:
						<td></td><td></td>
					% else:
						<td>${zas[a].name_link()}</td>
						<td class="sec">(${zas[a].function})</td>
					% endif
					% if a >= lb:
						<td></td><td></td>
					% else:
						<td>${bas[a].name_link()}</td>
						<td class="sec">(${bas[a].function})</td>
					% endif
				</tr>
			% endfor
		</table>
	</div>
	<div class="int">
		<h4>Advisory Board</h4>
		<ul>
			<li>Martin  Haspelmath (Universität Leipzig/MPI for the Science of Human History) </li>
			<li>Nikolaus P. Himmelmann (University of Cologne/LAC) </li>
			<li>Uwe Reichel (University of Munich, Munich)</li>
			<li>Paul Trilsbeek (MPI for Psycholinguistics/TLA,  Nijmegen)</li>
		</ul>
	</div>
	<div class="int">
	<h4>Former project members</h4>
		<ul>
		    <li>Celia Birle (Student Assistant)</li>
			<li>Cheslie Klein (Student Assistant)</li>
			<li>Runzhi Lou (Student Assistant)</li>
			<li>François Delafontaine (Assistant Engineer)</li>
		</ul>
	</div>
</div>
