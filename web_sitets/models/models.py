# -*- coding: utf-8 -*-

from odoo import models, fields, api

class TodoTask(models.Model):
     _name = 'todo.task'

     name = fields.Char('Descrip', required=True)
     is_done = fields.Boolean('Done')
     active = fields.Boolean('Active', default=True)

     note = fields.Text('Note')

     note_uno = fields.Text('Test1')
     
     note_dos = fields.Text('Test2')
     
     note_tres = fields.Text('Test3')      

class BudgetProjection(models.Model):
     _name = 'budget_projection'
     name = fields.Char('Descripcion', required=True)
     is_done = fields.Boolean('Done')
     active = fields.Boolean('Active', default=True)
     note = fields.Text('Note')

