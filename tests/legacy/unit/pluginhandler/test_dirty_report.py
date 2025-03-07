# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
# Copyright (C) 2018 Canonical Ltd
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

from testscenarios import multiply_scenarios

from snapcraft_legacy.internal import steps
from snapcraft_legacy.internal.pluginhandler._dirty_report import (
    Dependency,
    DirtyReport,
)


class TestDirtyReportGetReport:

    property_scenarios = [
        ("no properties", dict(dirty_properties=None, properties_report="")),
        (
            "single property",
            dict(
                dirty_properties=["prop1"],
                properties_report="The 'prop1' part property appears to have "
                "changed.",
            ),
        ),
        (
            "multiple properties",
            dict(
                dirty_properties=["prop1", "prop2"],
                properties_report="The 'prop1' and 'prop2' part properties appear "
                "to have changed.",
            ),
        ),
    ]

    option_scenarios = [
        ("no project options", dict(dirty_project_options=None, options_report="")),
        (
            "single project option",
            dict(
                dirty_project_options=["op1"],
                options_report="The 'op1' project option appears to have changed.",
            ),
        ),
        (
            "multiple properties",
            dict(
                dirty_project_options=["op1", "op2"],
                options_report="The 'op1' and 'op2' project options appear to "
                "have changed.",
            ),
        ),
    ]

    dependencies_scenarios = [
        (
            "no changed dependencies",
            dict(changed_dependencies=None, dependencies_report=""),
        ),
        (
            "single changed dependency",
            dict(
                changed_dependencies=[Dependency(part_name="dep1", step=steps.PULL)],
                dependencies_report="A dependency has changed: 'dep1'",
            ),
        ),
        (
            "multiple changed dependency",
            dict(
                changed_dependencies=[
                    Dependency(part_name="dep1", step=steps.PULL),
                    Dependency(part_name="dep2", step=steps.PULL),
                ],
                dependencies_report="Some dependencies have changed: 'dep1' and "
                "'dep2'",
            ),
        ),
    ]

    scenarios = multiply_scenarios(
        property_scenarios, option_scenarios, dependencies_scenarios
    )

    def test_get_report(
        self,
        dirty_properties,
        properties_report,
        dirty_project_options,
        options_report,
        changed_dependencies,
        dependencies_report,
    ):
        dirty_report = DirtyReport(
            dirty_properties=dirty_properties,
            dirty_project_options=dirty_project_options,
            changed_dependencies=changed_dependencies,
        )

        expected_report = []
        if properties_report:
            expected_report.append(properties_report)
        if options_report:
            expected_report.append(options_report)
        if dependencies_report:
            expected_report.append(dependencies_report)
        if expected_report:
            expected_report.append("")

        assert dirty_report.get_report() == "\n".join(expected_report)


class TestDirtyReportGetSummary:

    scenarios = [
        (
            "single property",
            dict(
                dirty_properties=["foo"],
                dirty_project_options=None,
                changed_dependencies=None,
                expected_summary="'foo' property changed",
            ),
        ),
        (
            "multiple properties",
            dict(
                dirty_properties=["foo", "bar"],
                dirty_project_options=None,
                changed_dependencies=None,
                expected_summary="properties changed",
            ),
        ),
        (
            "single option",
            dict(
                dirty_properties=None,
                dirty_project_options=["foo"],
                changed_dependencies=None,
                expected_summary="'foo' option changed",
            ),
        ),
        (
            "multiple options",
            dict(
                dirty_properties=None,
                dirty_project_options=["foo", "bar"],
                changed_dependencies=None,
                expected_summary="options changed",
            ),
        ),
        (
            "single dependency",
            dict(
                dirty_properties=None,
                dirty_project_options=None,
                changed_dependencies=[Dependency(part_name="foo", step=steps.PULL)],
                expected_summary="'foo' changed",
            ),
        ),
        (
            "multiple dependencies",
            dict(
                dirty_properties=None,
                dirty_project_options=None,
                changed_dependencies=[
                    Dependency(part_name="foo", step=steps.PULL),
                    Dependency(part_name="bar", step=steps.PULL),
                ],
                expected_summary="dependencies changed",
            ),
        ),
        (
            "property and option",
            dict(
                dirty_properties=["foo"],
                dirty_project_options=["bar"],
                changed_dependencies=None,
                expected_summary="options and properties changed",
            ),
        ),
        (
            "property and dependencies",
            dict(
                dirty_properties=["foo"],
                dirty_project_options=None,
                changed_dependencies=[Dependency(part_name="bar", step=steps.PULL)],
                expected_summary="dependencies and properties changed",
            ),
        ),
        (
            "options and dependencies",
            dict(
                dirty_properties=None,
                dirty_project_options=["foo"],
                changed_dependencies=[Dependency(part_name="bar", step=steps.PULL)],
                expected_summary="dependencies and options changed",
            ),
        ),
    ]

    def test_get_summary(
        self,
        dirty_properties,
        dirty_project_options,
        changed_dependencies,
        expected_summary,
    ):
        dirty_report = DirtyReport(
            dirty_properties=dirty_properties,
            dirty_project_options=dirty_project_options,
            changed_dependencies=changed_dependencies,
        )

        assert dirty_report.get_summary() == expected_summary
