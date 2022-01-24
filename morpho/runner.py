#!/usr/bin/env python3

import morpho.cmd as cmd


def _main():
    cfg = cmd.Config()
    cmd.loop(cfg)


if __name__ == "__main__":
    _main()
