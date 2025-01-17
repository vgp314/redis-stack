#
# Copyright Redis Ltd. [2022] - present
# Licensed under your choice of the Redis Source Available License 2.0 (RSALv2) or
# the Server Side Public License v1 (SSPLv1).
#
import subprocess

import pytest
from env import VagrantTestEnv
from mixins import RedisPackagingMixin, RedisTestMixin


class VagrantBase(VagrantTestEnv, RedisPackagingMixin, RedisTestMixin):
    """Tests inside a vagrant, to simulate machines, rather than dockers"""


class DebVagrant(VagrantBase):
    def install(self):

        res = subprocess.run(
            ["vagrant", "ssh", "-c", "sudo apt-get update"], cwd=self.workdir
        )
        assert res.returncode == 0

        res = subprocess.run(
            ["vagrant", "ssh", "-c", "sudo apt install -y gdebi-core"],
            cwd=self.workdir,
        )
        assert res.returncode == 0

        cmd = [
            "vagrant",
            "ssh",
            "-c",
            "sudo gdebi -n /data/redis-stack/redis-stack-server*.deb",
        ]
        res = subprocess.run(cmd, cwd=self.workdir)
        assert res.returncode == 0

    def uninstall(self):
        cmd = [
            "vagrant",
            "ssh",
            "-c",
            "sudo apt remove -y redis-stack-server",
        ]
        res = subprocess.run(cmd, cwd=self.workdir)
        assert res.returncode == 0


class RPMVagrant(VagrantBase):
    def install(self):
        cmd = [
            "vagrant",
            "ssh",
            "-c",
            "sudo yum install -y /data/redis-stack/redis-stack-server*.rpm",
        ]
        res = subprocess.run(cmd, cwd=self.workdir)
        assert res.returncode in [0, 1]

    def uninstall(self):
        cmd = ["vagrant", "ssh", "-c", "sudo yum remove -y redis-stack-server"]
        res = subprocess.run(cmd, cwd=self.workdir)
        assert res.returncode == 0


@pytest.mark.focal
@pytest.mark.physical
class TestFocal(DebVagrant):

    OSNICK = "focal"


@pytest.mark.jammy
@pytest.mark.physical
class TestJammy(DebVagrant):

    OSNICK = "jammy"


@pytest.mark.bionic
@pytest.mark.physical
class TestBionic(DebVagrant):

    OSNICK = "bionic"


@pytest.mark.xenial
@pytest.mark.physical
class TestXenial(DebVagrant):

    OSNICK = "xenial"


@pytest.mark.bullseye
@pytest.mark.physical
class TestBullseye(DebVagrant):

    OSNICK = "bullseye"


@pytest.mark.rhel7
@pytest.mark.physical
class TestCentos7(RPMVagrant):

    OSNICK = "centos7"


@pytest.mark.rhel8
@pytest.mark.physical
class TestCentos8(RPMVagrant):

    OSNICK = "centos8"
