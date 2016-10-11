# -*- coding: utf-8 -*-
# @author: ShuLong Hu
# Created on 2016-09-09
#
import os
import time

import datetime

from dxb.libs.utils import get_root_path
from dxb.libs.utils import options
from dxb.libs import utils
from bson import ObjectId
from tornado.template import Template, Loader
import sys
import trml2pdf
import reportlab.rl_config
reportlab.rl_config.warnOnMissingFontGlyphs = 0
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('song',os.path.join(get_root_path(),'static','font','SURSONG.TTF')))
pdfmetrics.registerFont(TTFont('hei',os.path.join(get_root_path(),'static','font','SIMHEI.TTF')))

from reportlab.lib import fonts
fonts.addMapping('song',0,0,'song')
fonts.addMapping('song',0,1,'song')
fonts.addMapping('song',1,0,'hei')
fonts.addMapping('song',1,1,'hei')

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding('utf-8')

def get_pdf(coll_model,ent_id):
    res = coll_model.find_one({"_id":utils.create_objectid(ent_id)})
    t = Template(open(os.path.join(get_root_path(),'static','rml.rml')).read())
    add_time = res["add_time"].split(".")[0].replace("-",".")

    report_time = datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')
    _rml = t.generate(item=res,time=report_time,add_time=add_time)
    rml = _rml.encode('utf-8')
    name = str(time.time()).replace('.','') + "-1" + '.pdf'
    uri = os.path.join(get_root_path(),'static','report',time.strftime('%Y'),time.strftime('%m-%d'),name)
    if not os.path.exists(os.path.dirname(uri)):
                os.makedirs(os.path.dirname(uri), mode=0777)
    trml2pdf.parseString(rml,uri)
    return "http://"+options.domain+uri.split("dxb")[1]
