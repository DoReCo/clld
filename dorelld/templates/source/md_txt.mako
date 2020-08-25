<%
from dorelld.util import get_author
from datetime import datetime

    # author
auth = get_author(ctx.author,'txt') 
    # access date
access = datetime.now().strftime("%m/%d/%Y")
#access = datetime.now().strftime("%m/%d/%Y") # US
%>

${auth}. ${ctx.year}. ${ctx.title}.
In Seifart, Frank, Ludger Paschen & Matthew Stave (eds.).
Language Documentation Reference Corpus (DoReCo) 1.0.
Berlin & Lyon: Leibniz-Zentrum Allgemeine Sprachwissenschaft & Université de Lyon/CNRS-DDL.
<%text filter="h"><</%text>${ctx.url}<%text filter="h">></%text> (Accessed on ${access}).
