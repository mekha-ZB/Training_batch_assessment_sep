# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
##############################################
#
# ZestyBeanz Technologies Pvt. Ltd

# Website1 : http://www.zbeanztech.com
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs.
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly advised to contract a Free Software
# Service Company.
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/> or
# write to the Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
###############################################
# 1. Security groups
# 2. Security rules
# 3. Access rights (CSV)
# 4. Data files
# 5. Wizards
# 6. Views
# 7. Reports
# 8. Demo data
{
    'name': 'library_management1',
    "summary": "Summery",
    "version": "19.0.0.0",
    "author": "Susmitha",
    "license": "LGPL-3",
    "website": "http://www.zbeanztech.com",
    "description": """Library books management""",
    'depends': ['base','contacts','mail'],
    'data': [
        'security/security.xml',

        'security/ir.model.access.csv',
        'security/record_rules.xml',

        'data/sequence_data.xml',
        'data/mail_template_data.xml',

        'wizard/library_book_issue_wizard_views.xml',

        'views/library_book_views.xml',
        'views/library_book_issue_views.xml',
        'views/res_partner_views.xml',

        'views/menu_views.xml',

        'report/library_book_issue_report.xml',
    ],
    'test': [],
    'demo': [],
    'installation': True,
    'auto_install': False,
    'application': True,
}
