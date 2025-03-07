# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
# Copyright 2022 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Snapcraft commands."""

from .account import (
    StoreExportLoginCommand,
    StoreLoginCommand,
    StoreLogoutCommand,
    StoreWhoAmICommand,
)
from .discovery import ListPluginsCommand, PluginsCommand
from .extensions import (
    ExpandExtensionsCommand,
    ExtensionsCommand,
    ListExtensionsCommand,
)
from .legacy import (
    StoreLegacyCreateKeyCommand,
    StoreLegacyGatedCommand,
    StoreLegacyListKeysCommand,
    StoreLegacyListValidationSetsCommand,
    StoreLegacyMetricsCommand,
    StoreLegacyPromoteCommand,
    StoreLegacyRegisterKeyCommand,
    StoreLegacySetDefaultTrackCommand,
    StoreLegacySignBuildCommand,
    StoreLegacyUploadMetadataCommand,
    StoreLegacyValidateCommand,
)
from .lifecycle import (
    BuildCommand,
    CleanCommand,
    PackCommand,
    PrimeCommand,
    PullCommand,
    SnapCommand,
    StageCommand,
)
from .manage import StoreCloseCommand, StoreReleaseCommand
from .names import (
    StoreLegacyListCommand,
    StoreLegacyListRegisteredCommand,
    StoreNamesCommand,
    StoreRegisterCommand,
)
from .remote import RemoteBuildCommand
from .status import (
    StoreListRevisionsCommand,
    StoreListTracksCommand,
    StoreRevisionsCommand,
    StoreStatusCommand,
    StoreTracksCommand,
)
from .upload import StoreLegacyPushCommand, StoreUploadCommand
from .validation_sets import StoreEditValidationSetsCommand
from .version import VersionCommand

__all__ = [
    "BuildCommand",
    "CleanCommand",
    "ExpandExtensionsCommand",
    "ExtensionsCommand",
    "ListExtensionsCommand",
    "ListPluginsCommand",
    "PackCommand",
    "PluginsCommand",
    "PrimeCommand",
    "PullCommand",
    "RemoteBuildCommand",
    "SnapCommand",
    "StageCommand",
    "StoreCloseCommand",
    "StoreEditValidationSetsCommand",
    "StoreExportLoginCommand",
    "StoreLegacyCreateKeyCommand",
    "StoreLegacyGatedCommand",
    "StoreLegacyListCommand",
    "StoreLegacyListRegisteredCommand",
    "StoreLegacyListValidationSetsCommand",
    "StoreLegacyMetricsCommand",
    "StoreLegacyPromoteCommand",
    "StoreLegacyPushCommand",
    "StoreLegacyRegisterKeyCommand",
    "StoreLegacySetDefaultTrackCommand",
    "StoreLegacySignBuildCommand",
    "StoreLegacyUploadMetadataCommand",
    "StoreLegacyValidateCommand",
    "StoreLegacyListKeysCommand",
    "StoreListTracksCommand",
    "StoreListRevisionsCommand",
    "StoreLoginCommand",
    "StoreLogoutCommand",
    "StoreNamesCommand",
    "StoreRegisterCommand",
    "StoreReleaseCommand",
    "StoreRevisionsCommand",
    "StoreStatusCommand",
    "StoreTracksCommand",
    "StoreUploadCommand",
    "StoreWhoAmICommand",
    "VersionCommand",
]
