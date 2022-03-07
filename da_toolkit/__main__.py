#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from da_toolkit.config import Config


def main():
    cnf = Config()
    cnf.get_redshift_creds()
    cnf.get_bq_creds()
    # cwd = os.getcwd()
    cnf.load()


if __name__ == "__main__":
    main()
