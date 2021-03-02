# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
# Copyright (C) 2020 Canonical Ltd
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

from textwrap import dedent

from snapcraft.plugins.v2.python import PythonPlugin


def test_schema():
    assert PythonPlugin.get_schema() == {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "constraints": {
                "default": [],
                "items": {"type": "string"},
                "type": "array",
                "uniqueItems": True,
            },
            "python-packages": {
                "default": ["pip", "setuptools", "wheel"],
                "items": {"type": "string"},
                "type": "array",
                "uniqueItems": True,
            },
            "requirements": {
                "default": [],
                "items": {"type": "string"},
                "type": "array",
                "uniqueItems": True,
            },
        },
        "type": "object",
    }


def test_get_build_packages():
    plugin = PythonPlugin(part_name="my-part", options=lambda: None)

    assert plugin.get_build_packages() == {"findutils", "python3-venv", "python3-dev"}


def test_get_build_environment():
    plugin = PythonPlugin(part_name="my-part", options=lambda: None)

    assert plugin.get_build_environment() == {
        "PATH": "${SNAPCRAFT_PART_INSTALL}/bin:${PATH}",
        "SNAPCRAFT_PYTHON_INTERPRETER": "python3",
        "SNAPCRAFT_PYTHON_VENV_ARGS": "",
    }


_FIXUP_BUILD_COMMANDS = [
    dedent(
        """\
            find "${SNAPCRAFT_PART_INSTALL}" -type f -executable -print0 | xargs -0 \
                sed -i "1 s|^#\\!${SNAPCRAFT_PYTHON_VENV_INTERP_PATH}.*$|#\\!/usr/bin/env ${SNAPCRAFT_PYTHON_INTERPRETER}|"
            """
    ),
    dedent(
        """\
            determine_link_target() {
                opts_state="$(set +o +x | grep xtrace)"
                interp_dir="$(dirname "${SNAPCRAFT_PYTHON_VENV_INTERP_PATH}")"
                target="${SNAPCRAFT_PYTHON_PATH}"
                for dir in "${SNAPCRAFT_PART_INSTALL}" "${SNAPCRAFT_STAGE}"; do
                    if  echo "${SNAPCRAFT_PYTHON_PATH}" | grep -q "${dir}"; then
                        target="$(realpath --strip --relative-to="${interp_dir}" \\
                                "${SNAPCRAFT_PYTHON_PATH}")"
                        break
                    fi
                done
                echo "${target}"
                eval "${opts_state}"
            }

            target="$(determine_link_target)"
            ln -sf "${target}" "${SNAPCRAFT_PYTHON_VENV_INTERP_PATH}"


        """
    ),
]


def test_get_build_commands():
    class Options:
        constraints = list()
        requirements = list()
        python_packages = list()

    plugin = PythonPlugin(part_name="my-part", options=Options())

    assert (
        plugin.get_build_commands()
        == [
            'SNAPCRAFT_PYTHON_PATH="${SNAPCRAFT_PYTHON_PATH:-$(which "${SNAPCRAFT_PYTHON_INTERPRETER}")}"',
            'SNAPCRAFT_PYTHON_PATH="$(readlink -e "${SNAPCRAFT_PYTHON_PATH}")"',
            '"${SNAPCRAFT_PYTHON_PATH}" -m venv ${SNAPCRAFT_PYTHON_VENV_ARGS} "${SNAPCRAFT_PART_INSTALL}"',
            'SNAPCRAFT_PYTHON_VENV_INTERP_PATH="${SNAPCRAFT_PART_INSTALL}/bin/${SNAPCRAFT_PYTHON_INTERPRETER}"',
            "[ -f setup.py ] && pip install  -U .",
        ]
        + _FIXUP_BUILD_COMMANDS
    )


def test_get_build_commands_with_all_properties():
    class Options:
        constraints = ["constraints.txt"]
        requirements = ["requirements.txt"]
        python_packages = ["pip", "some-pkg; sys_platform != 'win32'"]

    plugin = PythonPlugin(part_name="my-part", options=Options())

    assert (
        plugin.get_build_commands()
        == [
            'SNAPCRAFT_PYTHON_PATH="${SNAPCRAFT_PYTHON_PATH:-$(which "${SNAPCRAFT_PYTHON_INTERPRETER}")}"',
            'SNAPCRAFT_PYTHON_PATH="$(readlink -e "${SNAPCRAFT_PYTHON_PATH}")"',
            '"${SNAPCRAFT_PYTHON_PATH}" -m venv ${SNAPCRAFT_PYTHON_VENV_ARGS} "${SNAPCRAFT_PART_INSTALL}"',
            'SNAPCRAFT_PYTHON_VENV_INTERP_PATH="${SNAPCRAFT_PART_INSTALL}/bin/${SNAPCRAFT_PYTHON_INTERPRETER}"',
            "pip install -c 'constraints.txt' -U pip 'some-pkg; sys_platform != '\"'\"'win32'\"'\"''",
            "pip install -c 'constraints.txt' -U -r 'requirements.txt'",
            "[ -f setup.py ] && pip install -c 'constraints.txt' -U .",
        ]
        + _FIXUP_BUILD_COMMANDS
    )
