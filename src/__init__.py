# Copyright (C) 2020 Hyun Woo Park
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# -*- coding: utf-8 -*-
#
# img_paste_fix v25.6.14i59
#
# Copyright: trgk (phu54321@naver.com)
# License: GNU AGPL, version 3 or later;
# See http://www.gnu.org/licenses/agpl.html

from aqt.editor import EditorWebView
from aqt.qt import QMimeData
from aqt import gui_hooks


from .utils import openChangelog
from .utils import uuid  # duplicate UUID checked here
from .utils.debugLog import log  # debug log registered here

from .html_parser.single_image_html_parse import single_image_html_parse

from typing import Optional
import re


def _extractSingleImageFragment(html: str) -> Optional[str]:
    # Windows MIME uses fragment
    try:
        html_stripped = html[
            html.index("<!--StartFragment-->") + 20 : html.rindex("<!--EndFragment-->")
        ]
        if not html_stripped:
            # maybe malformed html?
            return None
        return html_stripped
    except ValueError:
        pass

    # macOS MIME uses single <img> tag followed by <meta>
    # <meta charset='utf-8'><img src="....">
    macOS_single_image_regex = (
        r"""^<meta charset=["']utf-8['"]>(<img\b(?:[^>"']+|"[^"]*"|'[^']*')*?>)$"""
    )
    m = re.match(macOS_single_image_regex, html)
    if m:
        return m.group(1)


def processSingleImageHtml(
    original_mime: QMimeData, self: EditorWebView, _internal, extended, _drop_event
):
    if not original_mime.hasHtml():
        return original_mime

    html_content = original_mime.html()

    # Unwraps fragment data.
    html_content = _extractSingleImageFragment(html_content)
    if not html_content:
        return original_mime

    img_tag = single_image_html_parse(html_content)
    if img_tag:
        try:
            src = img_tag["src"]
        except KeyError:
            return original_mime

        if self.editor.isURL(src):
            fname = self.editor._retrieveURL(src)
            if fname:
                img_tag["src"] = fname
                mime = QMimeData()
                mime.setHtml(str(img_tag))
                return mime

            else:
                image_html = self._processImage(original_mime, extended)
                if image_html:
                    img_tag_2 = single_image_html_parse(image_html)
                    if img_tag_2:
                        img_tag["src"] = img_tag_2["src"]
                        mime = QMimeData()
                        mime.setHtml(str(img_tag))

                    else:
                        mime = QMimeData()
                        mime.setHtml(image_html)
                    return mime

    return original_mime


gui_hooks.editor_will_process_mime.append(processSingleImageHtml)
