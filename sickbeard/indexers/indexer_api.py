# Author: Nic Wolfe <nic@wolfeden.ca>
# URL: http://code.google.com/p/sickbeard/
#
# This file is part of SickGear.
#
# SickGear is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SickGear is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SickGear.  If not, see <http://www.gnu.org/licenses/>.
import os
import sickbeard

from indexer_config import initConfig, indexerConfig
from sickbeard.helpers import proxy_setting

class indexerApi(object):
    def __init__(self, indexerID=None):
        self.indexerID = int(indexerID) if indexerID else None

    def __del__(self):
        pass

    def indexer(self, *args, **kwargs):
        if self.indexerID:
            return indexerConfig[self.indexerID]['module'](*args, **kwargs)

    @property
    def config(self):
        if self.indexerID:
            return indexerConfig[self.indexerID]
        return initConfig

    @property
    def name(self):
        if self.indexerID:
            return indexerConfig[self.indexerID]['name']

    @property
    def api_params(self):
        if self.indexerID:
            if sickbeard.CACHE_DIR:
                indexerConfig[self.indexerID]['api_params']['cache'] = os.path.join(sickbeard.CACHE_DIR, 'indexers', self.name)
            if sickbeard.PROXY_SETTING and sickbeard.PROXY_INDEXERS:
                (proxy_address, pac_found) = proxy_setting(sickbeard.PROXY_SETTING, indexerConfig[self.indexerID]['base_url'], force=True)
                if proxy_address:
                    indexerConfig[self.indexerID]['api_params']['proxy'] = proxy_address

            return indexerConfig[self.indexerID]['api_params']

    @property
    def cache(self):
        if sickbeard.CACHE_DIR:
            return self.api_params['cache']

    @property
    def indexers(self):
        return dict((int(x['id']), x['name']) for x in indexerConfig.values())
