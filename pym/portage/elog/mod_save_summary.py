# elog/mod_save_summary.py - elog dispatch module
# Copyright 2006-2007 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Id$

import codecs
import time
from portage import os
from portage import _encodings
from portage import _unicode_decode
from portage import _unicode_encode
from portage.data import portage_uid, portage_gid
from portage.localization import _
from portage.util import ensure_dirs, apply_permissions
from portage.const import EPREFIX

def process(mysettings, key, logentries, fulltext):
	if mysettings["PORT_LOGDIR"] != "":
		elogdir = os.path.join(mysettings["PORT_LOGDIR"], "elog")
	else:
		elogdir = os.path.join(EPREFIX, "var", "log", "portage", "elog")
	ensure_dirs(elogdir, uid=portage_uid, gid=portage_gid, mode=02770)

	# TODO: Locking
	elogfilename = elogdir+"/summary.log"
	elogfile = codecs.open(_unicode_encode(elogfilename,
		encoding=_encodings['fs'], errors='strict'),
		mode='a', encoding=_encodings['content'], errors='backslashreplace')
	apply_permissions(elogfilename, mode=060, mask=0)
	time_str = time.strftime("%Y-%m-%d %H:%M:%S %Z",
		time.localtime(time.time()))
	# Avoid potential UnicodeDecodeError later.
	time_str = _unicode_decode(time_str,
		encoding=_encodings['content'], errors='replace')
	elogfile.write(_(">>> Messages generated by process %(pid)d on %(time)s for package %(pkg)s:\n\n") %
			{"pid": os.getpid(), "time": time_str, "pkg": key})
	elogfile.write(fulltext)
	elogfile.write("\n")
	elogfile.close()

	return elogfilename
