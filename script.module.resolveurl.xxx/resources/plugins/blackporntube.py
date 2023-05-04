"""
    Plugin for ResolveURL
    Copyright (C) 2023 ErosVece

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import re
from resolveurl import common
from resolveurl.lib import helpers
from resolveurl.resolver import ResolveUrl, ResolverError

class BlackPornTubeResolver(ResolveUrl):
    name = 'blackporntube'
    domains = ['blackporn.tube']
    pattern = r'(?://|\.)(blackporn\.tube)/video/([a-zA-Z0-9]+)'

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        headers = {
            'User-Agent': common.RAND_UA,
            'Referer': 'https://{0}/'.format(host)
        }
        html = self.net.http_GET(web_url, headers=headers).content
        r = re.search('video_url":"([^"]+)', html)
        if r:
            videourl = helpers.Tdecode(r.group(1))
            if not videourl.startswith('http'):
                videourl = 'https://{0}{1}'.format(host, videourl)
            return videourl + helpers.append_headers(headers)

        raise ResolverError('File not found')

    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, template='http://{host}/api/videofile.php?video_id={media_id}&lifetime=8640000')

    @classmethod
    def _is_enabled(cls):
        return True