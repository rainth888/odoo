#!/bin/bash

# docker start pg170
#sleep 5

source .venv/bin/activate

# python odoo-bin -c odoo.conf
# nohup python odoo-bin -c odoo.conf 2>&1 &
python odoo-bin -c odoo.conf


