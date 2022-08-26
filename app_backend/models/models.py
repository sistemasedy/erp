# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class TodoTask(models.Model):
#      _name = 'todo.task'

#      name = fields.Char('Descrip', required=True)
#      is_done = fields.Boolean('Done')
#      active = fields.Boolean('Active', default=True)

#      note = fields.Text('Note')

#      note_uno = fields.Text('Test1')
     
#      note_dos = fields.Text('Test2')
     
#      note_tres = fields.Text('Test3')      



#      #@api.multi
#      def do_toggle_done(self):
#          self.is_done = not self.is_done
#          return True
#      #@api.multi
#      def do_clear_done(self):
#          done_recs = self.search([('is_done', '=', True)])
#          done_recs.write({'active': False})
#          return True


     #value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

